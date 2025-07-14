import random
import numpy as np
from sps_mat import sps
# from SPSgpt import sps
import pandas as pd


  # GLOBAL VARIABLES


# total_RBs = 30000000                         # total RB available per 10mins = 30mil i.e., 50/msec, (calculation in notes)
# NumSubFrames = 600000
# NumSubChannels = 10
# min_res_per_slice = 3000000

epoch = 324                    # these are the number of epochs based on the entries in dataset


gamingPDR = []
smartphonePDR = []
industryPDR = []
transportPDR = []
safetyPDR = []


time_in_msec = 2000                     # this is the recording time interval of requests from each slice
NumSubChannels = 10
NumSubFrames = time_in_msec
total_RBs = 50*NumSubFrames             # total RB available per sec = 50k i.e., 50RBs/msec, (calculation in notes)
min_res_per_slice = total_RBs/(NumSubChannels)
print('Time: ', time_in_msec, 'msecs')
print('NumSubFrames:', NumSubFrames)
print('NumSubChannels', NumSubChannels)
print('total RBs', total_RBs)
print('min_res_per_slice:', min_res_per_slice)

num_slices = 5
packet_szie = [800, 190, 200, 400, 300]  # gaming, smartphone, industry, transport, safety
bbu = [20, 4, 8, 12, 8]                    # gaming, smartphone, industry, transport, safety
#190 bytes pkr needs 4 RBs

# packet_szie = [600, 190, 300, 400, 300]  # gaming, smartphone, industry, transport, safety
# bbu = [4, 1, 2, 3, 2]                    # gaming, smartphone, industry, transport, safety
periodicity = [200, 50, 100, 200, 100]   # pkt generation rate in msec
periodicityHz = [(1/(x/1000)) for x in periodicity]
periodicityHz = [int(x) for x in periodicityHz]
# print('periodicityHz', periodicityHz)
RC_gaming = (random.randint(5,10))         # reselection counter is dependent on periodicity (see more in code notes file)
RC_smartphone = random.randint(15,25)
RC_industry = random.randint(5,15)
RC_transport = random.randint(5,10)
RC_safety = random.randint(5,15)

traffic = []
required_BW = np.zeros(5)
allocated = []
# lat = [1, 2, 3]
# thresh = 10
# PDR = np.zeros((epoch,num_slices))
PDR_list = []

def users(num_slices, total_users):             # (random) num of users of each slice
    # Generate a list of random numbers for each slice
    users_per_slice = [random.randint(1, total_users) for _ in range(num_slices)]
    users_per_slice.sort(reverse=True)
    return users_per_slice

def required_BW_per_slice(num_slices):                    # BW required by each slice
    for slice in range(num_slices):
        res_required = traffic[slice]*((bbu[slice]*time_in_msec)/periodicity[slice])     
        # required_BW.append(res_required)
        required_BW[slice] = res_required
    return required_BW                                    # returns BW required by 
                                                        # gaming, smartphone, industry, transport, safety slices


def allocate_resources_proportionally(total_resources, slice_users):
    # Calculate the total number of users
    total_users = sum(slice_users)

    # Calculate the resources proportionally based on the number of users in each slice
    resources_per_slice = [int(total_resources * (users / total_users)) for users in slice_users]

    # Ensure the total resources allocated do not exceed the available resources
    total_allocated = sum(resources_per_slice)
    if total_allocated > total_resources:
        # If the adjustments result in exceeding the available resources, distribute the remaining resources
        remaining_resources = total_resources - total_allocated
        remaining_slices = [i for i in range(len(slice_users)) if resources_per_slice[i] < slice_users[i]]
        for i in range(remaining_resources):
            resources_per_slice[remaining_slices[i % len(remaining_slices)]] += 1

    return resources_per_slice




def BW_allocation(type, resources, numOfSlices, sliceUsers, min_res_per_slice):  # (random) BW allocation to each slice
    # if type == 'random':
    #     # Generate random allocations for each slice
    #     allocations = [random.randint(0, resources) for _ in range(numOfSlices - 1)]
    #     # Sort the allocations in ascending order
    #     allocations.sort()
    #     # Calculate the resources for each slice
    #     resources_per_slice = [allocations[0]] + [allocations[i] - allocations[i - 1] for i in range(1, num_slices - 1)] + [resources - allocations[-1]]
    #     return resources_per_slice
    
    if type == 'random':
        # Ensure that each slice gets at least min_res_per_slice resources
        base_allocation = numOfSlices * min_res_per_slice
        if resources < base_allocation:
            raise ValueError(f"Not enough resources for {numOfSlices} slices with a minimum of {min_res_per_slice} resources each.")
        # Distribute resources randomly, ensuring divisibility by min_res_per_slice and positivity
        allocations = [random.randint(0, (resources - base_allocation) // (numOfSlices - i)) for i in range(numOfSlices - 1)]
        allocations.append(resources - sum(allocations))  # Ensure the total sums up to resources
        # Adjust allocations to be divisible by min_res_per_slice
        allocations = [allocation + min_res_per_slice - allocation % min_res_per_slice for allocation in allocations]
        # Ensure the total allocations do not exceed the given resources
        if sum(allocations) > resources:
            diff = sum(allocations) - resources
            allocations[-1] -= diff  # Adjust the last allocation
        return allocations


    elif type == 'fixed':
        # Calculate the resources for each slice
        resources_per_slice = [resources // numOfSlices] * numOfSlices
        # Adjust the resources to ensure the total matches the original total_resources
        resources_per_slice[0] += resources % numOfSlices
        return resources_per_slice
    
    elif type == 'proportional':
        # # Calculate the total number of users
        # total_users = sum(sliceUsers)
        # # Calculate the resources proportionally based on the number of users in each slice
        # resources_per_slice = [int(resources * (users / total_users)) for users in sliceUsers]
        # # Adjust the resources to ensure the total matches the original total_resources
        # resources_per_slice[0] += resources - sum(resources_per_slice)
        # return resources_per_slice

        # total_ratio = sliceUsers[0] + sliceUsers[1] 
        # slice_A_RB = (sliceUsers[0]/total_ratio) * resources
        # slice_B_RB = (sliceUsers[1]/total_ratio) * resources
        # slice_C_RB = 0
        # return slice_A_RB, slice_B_RB, slice_C_RB

        # Calculate the total number of users
        total_users = sum(sliceUsers)
        # Calculate the resources proportionally based on the number of users in each slice
        resources_per_slice = [int(NumSubChannels * (users / total_users)) * min_res_per_slice for users in sliceUsers]
        # Ensure each slice gets at least 1 subchannel
        resources_per_slice = [max(min_res_per_slice, allocation) for allocation in resources_per_slice]
        # Adjust each slice's allocation to be a multiple of min_res_per_slice
        resources_per_slice = [allocation - (allocation % min_res_per_slice) for allocation in resources_per_slice]
        # Ensure the total resources allocated do not exceed the available resources
        total_allocated = sum(resources_per_slice)
        if total_allocated > NumSubChannels * min_res_per_slice:
            # If the adjustments result in exceeding the available resources, distribute the remaining resources
            remaining_resources = NumSubChannels * min_res_per_slice - total_allocated
            remaining_slices = [i for i in range(num_slices) if resources_per_slice[i] < min_res_per_slice]
            remaining_slices.sort(key=lambda x: resources_per_slice[x], reverse=True)
            for i in range(int(remaining_resources)):
                # Stop if negative allocation is about to happen
                if not remaining_slices or resources_per_slice[remaining_slices[i % len(remaining_slices)]] + min_res_per_slice <= 0:
                    break
                resources_per_slice[remaining_slices[i % len(remaining_slices)]] += min_res_per_slice
        # Map resources to subchannels
        subchannels_per_slice = [allocation // min_res_per_slice for allocation in resources_per_slice]
        # Adjust the subchannels to ensure each slice gets at least 1 subchannel
        subchannels_per_slice = [max(1, subchannels) for subchannels in subchannels_per_slice]
        # Ensure the total sum of subchannels is equal to NumSubChannels
        subchannels_sum = sum(subchannels_per_slice)
        if subchannels_sum > NumSubChannels:
            remaining_slices = [i for i in range(num_slices) if subchannels_per_slice[i] > 1]
            remaining_slices.sort(key=lambda x: resources_per_slice[x], reverse=True)
            for i in range(int(subchannels_sum - NumSubChannels)):
                if not remaining_slices:
                    break
                slice_index = remaining_slices[i % len(remaining_slices)]
                subchannels_per_slice[slice_index] -= 1
        return subchannels_per_slice

########################################################   MAIN

data = 'C:\\Users\ku\\Downloads\\pimrc\\traffic_per_hour_original.xlsx'
sheet_name = 'Sheet1'

input = input('ENTER \n1 for RANDOM allocation, \n2 for FIXED allocation, \n3 for PROPORTIONAL allocation\n')

for i in range(epoch):                                  # for ORIGINAL traffic data
    print('EPOCH=====', i)
    df = pd.read_excel(data, sheet_name, header=None)
    # traffic per 10mins for each slice (gaming, smartphone, industry, transport, safety)    
    traffic = (df.iloc[i+1, 0:5].values)*1          
    traffic = [int(x) for x in traffic]
    gamingU, smartphoneU, industryU, transportU, safetyU = traffic

    print("Number of users in each slice:")
    print('gaming, smartphone, industry, transport, safety', traffic)

    required_BW  = required_BW_per_slice(num_slices)    # gives required BW for each slice based on number of users per slice
    required_BW = [int(x) for x in required_BW]
    print("\n RBs required for each slice:")
    print('gaming, smartphone, industry, transport, safety', required_BW)

    # required_BW = [int(x/10) for x in required_BW]                      # divided users by 10
    # gamingU1, smartphoneU1, industryU1, transportU1, safetyU1 = required_BW

########## RANDOM BW ALLOCATION TO EACH SLICE
    if input == '1':
        allocation_type = 'random'
# assumption: industry slice does not exist.But users exist.
# num of slices = 4, allocation to industry slice = 0
        num_slices = 4
        allocatedRB  = BW_allocation ('random', total_RBs, num_slices, traffic, min_res_per_slice)      
        gamingRB, smartphoneRB, transportRB, safetyRB = allocatedRB
        industryRB = 0
        # gamingRB, smartphoneRB, industryRB, transportRB, safetyRB = allocatedRB
        print("\n RBs allocated for each slice (randomly):")
        print('gaming, smartphone, industry, transport, safety', allocatedRB)

        allocatedRB = [value / min_res_per_slice for value in allocatedRB]
        allocatedRB = [int(x) for x in allocatedRB]
        # gamingSC, smartphoneSC, industrySC, transportSC, safetySC = allocatedRB
        gamingSC, smartphoneSC, transportSC, safetySC = allocatedRB
        industrySC = 0

        print("\n No. of subchannels allocated for each slice (randomly):")
        print('gaming, smartphone, industry, transport, safety:', gamingSC, smartphoneSC, industrySC, transportSC, safetySC, '\n')

        #################
        # Running SPS for each slice given the number of SCs and SFs
        gamingSPS = sps(gamingU, gamingSC, NumSubFrames, RC_gaming, periodicityHz[0])
        gamingPDR = 1- gamingSPS
        print('PDR of gaming slice:', gamingPDR, '\n')

        smartphoneSPS = sps(smartphoneU, smartphoneSC, NumSubFrames, RC_smartphone, periodicityHz[1])
        smartphonePDR = 1- smartphoneSPS
        print('PDR of smartphone slice:', smartphonePDR, '\n')

        # industrySPS = sps(industryU, industrySC, NumSubFrames, RC_industry, periodicityHz[2])
        # industryPDR = 1- industrySPS
        industryPDR = 0
        print('PDR of industry slice:', industryPDR, '\n')

        transportSPS = sps(transportU, transportSC, NumSubFrames, RC_transport, periodicityHz[3])
        transportPDR = 1- transportSPS
        print('PDR of transport slice:', transportPDR, '\n')

        safetySPS = sps(safetyU, safetySC, NumSubFrames, RC_safety, periodicityHz[4])
        safetyPDR = 1- safetySPS
        print('PDR of safety slice:', safetyPDR, '\n')

########## FIXED BW ALLOCATION TO EACH SLICE
    if input == '2':
        allocation_type = 'fixed'
# assumption: industry slice does not exist.But users exist.
# num of slices = 4, allocation to industry slice = 0
        num_slices = 4
        allocatedRB  = BW_allocation ('fixed', total_RBs, num_slices, traffic, min_res_per_slice)
        gamingRB, smartphoneRB, transportRB, safetyRB = allocatedRB
        industryRB = 0
        # gamingRB, smartphoneRB, industryRB, transportRB, safetyRB = allocatedRB
        print("\n RBs allocated for each slice (equally):")
        print('gaming, smartphone, industry, transport, safety', allocatedRB)

        allocatedRB = [value / min_res_per_slice for value in allocatedRB]
        allocatedRB = [int(x) for x in allocatedRB]
        # gamingSC, smartphoneSC, industrySC, transportSC, safetySC = allocatedRB
        gamingSC, smartphoneSC, transportSC, safetySC = allocatedRB
        industrySC = 0

        # gamingSC, smartphoneSC, industrySC, transportSC, safetySC  = int(gamingSC), int(smartphoneSC), int(industrySC), int(transportSC), int(safetySC)
        print("\n No. of subchannels allocated for each slice (randomly):")
        print('gaming, smartphone, industry, transport, safety:', gamingSC, smartphoneSC, industrySC, transportSC, safetySC, '\n')

        #################
        # Running SPS for each slice given the number of SCs and SFs
        gamingSPS = sps(gamingU, gamingSC, NumSubFrames, RC_gaming, periodicityHz[0])
        gamingPDR = 1- gamingSPS
        print('PDR of gaming slice:', gamingPDR, '\n')

        smartphoneSPS = sps(smartphoneU, smartphoneSC, NumSubFrames, RC_smartphone, periodicityHz[1])
        smartphonePDR = 1- smartphoneSPS
        print('PDR of smartphone slice:', smartphonePDR, '\n')

        # industrySPS = sps(industryU, industrySC, NumSubFrames, RC_industry, periodicityHz[2])
        # industryPDR = 1- industrySPS
        industryPDR = 0
        print('PDR of industry slice:', industryPDR, '\n')

        transportSPS = sps(transportU, transportSC, NumSubFrames, RC_transport, periodicityHz[3])
        transportPDR = 1- transportSPS
        print('PDR of transport slice:', transportPDR, '\n')

        safetySPS = sps(safetyU, safetySC, NumSubFrames, RC_safety, periodicityHz[4])
        safetyPDR = 1- safetySPS
        print('PDR of safety slice:', safetyPDR, '\n')

########## PROPORTIONAL BW ALLOCATION TO EACH SLICE
    if input == '3':
        allocation_type = 'proportional'
        allocatedRB = allocate_resources_proportionally(total_RBs, [gamingU, smartphoneU, 0, transportU, safetyU])
        # allocatedRB = allocate_resources_proportionally(total_RBs, traffic)
        allocatedRB = [int(x) for x in allocatedRB]
        gamingRB, smartphoneRB, industryRB, transportRB, safetyRB = allocatedRB
        print("\n RBs allocated for each slice (proportionally):")
        print('gaming, smartphone, industry, transport, safety', allocatedRB)
        allocatedSC = [int(np.round(x/NumSubFrames)) for x in allocatedRB]
        gamingSC, smartphoneSC, industrySC, transportSC, safetySC = allocatedSC
        print("\n No. of subchannels allocated for each slice (proportionally):")
        print('gaming, smartphone, industry, transport, safety', allocatedSC)

        # allocatedSC  = BW_allocation ('proportional', total_RBs, num_slices, traffic, min_res_per_slice)
        # allocatedSC = [int(x) for x in allocatedSC]
        # gamingSC, smartphoneSC, industrySC, transportSC, safetySC = allocatedSC
        # print("\n No. of subchannels allocated for each slice (proportionally):")
        # print('gaming, smartphone, industry, transport, safety:',allocatedSC, '\n')

        #################
        # Running SPS for each slice given the number of SCs and SFs
        gamingSPS = sps(gamingU, gamingSC, NumSubFrames, RC_gaming, periodicityHz[0])
        gamingPDR = 1- gamingSPS
        print('PDR of gaming slice:', gamingPDR, '\n')

        smartphoneSPS = sps(smartphoneU, smartphoneSC, NumSubFrames, RC_smartphone, periodicityHz[1])
        smartphonePDR = 1- smartphoneSPS
        print('PDR of smartphone slice:', smartphonePDR, '\n')

        # industrySPS = sps(industryU, industrySC, NumSubFrames, RC_industry, periodicityHz[2])
        # industryPDR = 1- industrySPS
        industryPDR = 0
        print('PDR of industry slice:', industryPDR, '\n')

        transportSPS = sps(transportU, transportSC, NumSubFrames, RC_transport, periodicityHz[3])
        transportPDR = 1- transportSPS
        print('PDR of transport slice:', transportPDR, '\n')

        safetySPS = sps(safetyU, safetySC, NumSubFrames, RC_safety, periodicityHz[4])
        safetyPDR = 1- safetySPS
        print('PDR of safety slice:', safetyPDR, '\n')


###################################### Saving data for plot
    
    PDR_list.append([gamingPDR, smartphonePDR, industryPDR, transportPDR, safetyPDR])
    # print(PDR_list)
    # PDR[i] = [gamingPDR, smartphonePDR, industryPDR, transportPDR, safetyPDR]
    # print(PDR[i])
    print('[',[gamingPDR, smartphonePDR, industryPDR, transportPDR, safetyPDR],']')
    print('********************************************')

    PDR = np.array(PDR_list)
    df0 = pd.DataFrame(PDR)
    df0.to_excel('C:\\Users\ku\\Downloads\\pimrc\\PDR_' + allocation_type + '_allocation_LOOP.xlsx', index=False, header=['AR/VR/Gaming', 'Smartphone', 'Industry 4.0', 'Smart Transportation', 'Traffic Safety'])


PDR = np.array(PDR_list)
df1 = pd.DataFrame(PDR)
df1.to_excel('C:\\Users\ku\\Downloads\\pimrc\\PDR_' + allocation_type + '_allocation.xlsx', index=False, header=['AR/VR/Gaming', 'Smartphone', 'Industry 4.0', 'Smart Transportation', 'Traffic Safety'])


