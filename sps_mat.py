# Generated with SMOP  0.41
# from libsmop import *
import numpy as np
import random

def sps(vehicles, subChannels, subFrames, reselectionCounter, periodicity):

    #Input Parameter One and Code for Validation of Input
    # print('Input the number of sub-frames:')
    # NumSubframes=input()                                      # user defines number of subframes. In the matrix, this is the row
    NumSubframes = subFrames
    print('\nNo. of subframnes = ', NumSubframes)
        
    #The following code is important in controlling the user parameters. It reduces system errors by ensuring that the user input the right data
        
    #if the user press return without entering any value
    # while (NumSubframes==0):
    #     print('Error! You can not leave this field bank! Please enter the number of sub-frames again.   ')
    #     print('Input the number of sub-frames:  ')
    #     NumSubframes=input()
    
    # #if the user enter a value beyond the limit
    # while NumSubframes < 2000 or NumSubframes > 200000:
    #     print('Error! The number of subframes should be an absolute integer number, greater than 2000 but not greater than 200 000 for this simulation.   ')
    #     print('Input the number of sub-frames:  ')
    #     NumSubframes=input()

    #     # In case the user enters a zero again, i.e leave it blank
    #     while (NumSubframes==0):
    #         print('Error! You can not leave this field bank! Please enter the number of sub-frames again.   ')
    #         print('Input the number of sub-frames:  ')
    #         NumSubframes=input()
        




    #Input Parameter Two and Code for Validation of Input
    # print('Input the number of sub-channels:')
    # NumSubChannels=input()                        # user defines number of subchannels. In the matrix, this is the column
    NumSubChannels=subChannels
    print('No. of subchannels = ', NumSubChannels)

    #The following code is important in controlling the user parameters. It reduces system errors by ensuring that the user input the right data
        
    #if the user press return without entering any value
    # while (NumSubChannels==0):
    #     print('Error! You can not leave this field bank! Please enter the number of sub-channels again.   ')
    #     print('Input the number of sub-channels:  ')
    #     NumSubChannels=input()
        
    # #if the user enter a value beyond the limit
    # while NumSubChannels < 0 or NumSubChannels > 4:
    #     print('Error! The number of sub-channels should be an absolute integer number and not greater than 4 for this simulation.   ')
    #     print('Input the number of sub-channels:  ')
    #     NumSubChannels=input()
        
    #     # In case the user enters a zero again, i.e leave it blank
    #     while (NumSubChannels==0):
    #         print('Error! You can not leave this field bank! Please enter the number of sub-channels again.   ')
    #         print('Input the number of sub-channels:  ')
    #         NumSubChannels=input()





    #Input Parameter Three and Code for Validation of Input
    # print('Input the number of vehicles:')
    # NumVehicles=input()                          # user defines number of vehicles. In the matrix, this is the 3rd dimension
    NumVehicles=vehicles
    print('No. of vehicles = ', NumVehicles)
        
    # if the user press return without entering any value
    # while (NumVehicles==0):
    #     print('Error! You can not leave this field bank! Please enter the number of vehicles again.   ')
    #     print('Input the number of vehicles:  ')
    #     NumVehicles=input()

    # #if the user enter a value beyond the limit
    # while NumVehicles < 0 or NumVehicles > 10000:
    #     print('Error! The number of vehicles should be an absolute integer number and not greater than 10 000 for this simulation.   ')
    #     print('Input the number of vehicles:  ')
    #     NumVehicles=input()
        
    #     # In case the user enters a zero again, i.e leave it blank
    #     while (NumVehicles==0):
    #         print('Error! You can not leave this field bank! Please enter the number of vehicles again.   ')
    #         print('Input the number of vehicles:  ')
    #         NumVehicles=input()




        
    #Code That define the V2X Pool
    V2Xpool=np.zeros([NumVehicles,NumSubChannels,NumSubframes])
    # V2Xpool=np.zeros((NumSubChannels,NumSubframes))
        
    #CODE FOR THE SENSING WINDOW
    sensing_vehicles=random.randint(5,20)

    #Loop for giving giving TBs to the subframes in the sensing window
    #The history should be the same and so this code is maintained for each vehicle
    for sensing_analyzer in range(0,sensing_vehicles):
        sensing_subframes=random.randint(1,100)                   #select subframe
        sensing_subchannels=random.randint(1,NumSubChannels)      #select subchannel
        # sensing_periodicity=100                                     #sensing_periodicity
        sensing_periodicity=periodicity                                     #sensing_periodicity
        sensing_reselections=random.randint(5,25)                 #Number of reselections

        check_sensing_subframes = sensing_subframes + (sensing_periodicity * sensing_reselections)  #Maximum number of subframes selected by the previous vehicles
        # print('sensing_subframes', sensing_subframes)
        # print('sensing_periodicity', sensing_periodicity)
        # print('sensing_reselections', sensing_reselections)
        # print('check_sensing_subframes=', check_sensing_subframes)

        while check_sensing_subframes > (1500):         #If the number of subframes chosen is bigger than 1500, reselect again.
        # while check_sensing_subframes > (NumSubframes/10):         #If the number of subframes chosen is bigger than given subframes, reselect again.
            sensing_subframes=random.randint(1,100)                   #select subframe 
            # sensing_periodicity=random.randint(0,50)                  #sensing_periodicity
            if periodicity ==50:
                sensing_periodicity=random.randint(0,50)                  #sensing_periodicity
            elif periodicity ==10:
                sensing_periodicity=random.randint(0,100)                  #sensing_periodicity
            sensing_reselections=random.randint(5,40)                 #Number of reselections
            check_sensing_subframes = sensing_subframes + (sensing_periodicity * sensing_reselections)
            # print('check-sensing...')
        # print('check-sensing...a gya bahar')


        V2Xpool[:,sensing_subchannels-1,sensing_subframes-1]=777     # 777 denotes the selection of a RB
        # V2Xpool[sensing_subchannels-1,sensing_subframes-1]=777     # 777 denotes the selection of a RB
        # print('V2Xpool\n', V2Xpool)
        #This code then make sure that each
        for sensing_counter in range(0,sensing_reselections):
            # print('index ====', sensing_subframes + (sensing_periodicity*sensing_counter)-1)
            V2Xpool[:, sensing_subchannels-1,sensing_subframes + (sensing_periodicity*sensing_counter)-1]=666    #This also selects a 777 in the reserved spots
        
    # debug=1     # cool for debugging the sensing window.


        
        
    # The following FOR LOOP does the selection. What a good code!!! Tested!
    for vehic_select in range(0,NumVehicles):

    ########### Variables for the selection window  ##################
        sel_trig=random.randint(1003,1100)                # This represents the time the selection trigger is given
        # sel_trig=random.randint(500,510)                # This represents the time the selection trigger is given
        start_select=random.randint(0,20)                 # This represents the time the selection window starts. maximum delay from the trigger is like 20ms
        end_select=0                                        # Initialization

        selection_window_size=random.randint(20,100)      # This together with the following code allows the selection window to be either 20, 50 or 100 subframes in size.
        
        if selection_window_size < 50:
            end_select=20

        elif selection_window_size >= 50 or selection_window_size <= 75:
            end_select=50            

        elif selection_window_size > 75:
            end_select=100


        sel_window_start = sel_trig + start_select        # These two statements highlight the time from which the selection will be made
        sel_window_end = sel_window_start + end_select    # End of selection window. The length of the selection window is less than 100 subframes.


    ####### Variables for selection within the selection window  ###########
        # period_select=100                               # This is for periodicity. can reserve a subframe
        period_select=periodicity                               # This is for periodicity. can reserve a subframe
        # mult_Periodicity=random.randint(5,15)            # These are the number of times the vehicle can reserve.
        mult_Periodicity= reselectionCounter            # These are the number of times the vehicle can reserve.

        sf_select=random.randint(sel_window_start,sel_window_end) # This randomly chooses the subframe from which the RB will be selected from the selection window
        sc_select=random.randint(1,NumSubChannels)                # This randomly chooses the subchannel from which the RB will be selected.


        #The above two lines allows the vehicle to select its resource's SF
        #and Sub-Channel WITHIN THE SELECTION WINDOW.


        # at the same time the number of subframes chosen should not exceed the number of subframes the user defined. the vehicles should not select outside the subframe range
        check_selected_subframes = sf_select + (period_select * mult_Periodicity)
        # print('check-000')

        # print('index==>',vehic_select, sc_select-1,sf_select-1)
        while V2Xpool[vehic_select, sc_select-1,sf_select-1] == 777:             # This is to avoid selecting what previous vehicles already reserved
        # while (V2Xpool[sc_select,sf_select] == 777):             # This is to avoid selecting what previous vehicles already reserved
            sf_select=random.randint(sel_window_start,sel_window_end)     # This randomly chooses the subframe from which the RB will be selected from the selection window
            sc_select=random.randint(1,NumSubChannels)                    # This randomly chooses the subchannel from which the RB will be selected.
            # print('check-0')

        # print('check-1')
        #to avoid subframes already selected by other vehicles. If you avaoid selecting what other vehicles selected then you automatically avoid colliding with their reservations
        if vehic_select > 1:
            while V2X_collision_detector[sc_select-1,sf_select-1] == 1:         # This is to avoid selecting what previous vehicles already reserved
                sf_select=random.randint(sel_window_start,sel_window_end) # This randomly chooses the subframe from which the RB will be selected from the selection window
                sc_select=random.randint(1,NumSubChannels)                # This randomly chooses the subchannel from which the RB will be selected.


        #NOTE: OUTSIDE THE SELECTION WINDOW, WE CAN NOT AVOID COLLISION WITH
        #THE SUBFRAMES PREVIOUSLY SELECTED BY THE PREVIOUS VEHICLES. WE WILL
        #REPRESENT THEM IN THE COLLISION WINDOWS BY THE NUMBER (NumVehicles +1)

        while check_selected_subframes > NumSubframes:
            while (V2Xpool[vehic_select,sc_select-1,sf_select-1] == NumVehicles):     # This is to avoid selecting what previous vehicles already reserved
            # while (V2Xpool[sc_select,sf_select] == NumVehicles):     # This is to avoid selecting what previous vehicles already reserved
                sf_select=random.randint(sel_window_start,sel_window_end)     # This randomly chooses the subframe from which the RB will be selected from the selection window
                sc_select=random.randint(1,NumSubChannels)                    # This randomly chooses the subchannel from which the RB will be selected.
                # print('check-2')
            # print('check-3')

            # mult_Periodicity=random.randint(3,15)                             # The Number of times the vehicle reserves multiplied by the Periodicity should be less than Number of subframes
            mult_Periodicity=reselectionCounter                             # The Number of times the vehicle reserves multiplied by the Periodicity should be less than Number of subframes
            # period_select=random.randint(0,100)
            if periodicity ==50:
                period_select=random.randint(0,50)
            elif periodicity ==100:
                period_select=random.randint(0,100)
            check_selected_subframes=sf_select + (period_select * mult_Periodicity)



        V2Xpool[vehic_select,sc_select-1,sf_select-1]=1             # 1 denotes the selection of a RB
        # V2Xpool[sc_select,sf_select]=1             # 1 denotes the selection of a RB
    
        #to select other resources because of Periodicity and Reselection, We use the
        #following function. We have to make sure that when the device
        #reserve some resources, it wont select the resource that are within
        #the defined number of subframes.
    
        for reservation_counter in range(0,mult_Periodicity):                                # We should not have more subframes than the predefined
            if (sf_select + (period_select * reservation_counter)) < NumSubframes:
                V2Xpool[vehic_select,sc_select-1,sf_select + (period_select * reservation_counter)-1]=1     # This also selects a 1 in the reserved spots
                # V2Xpool[sc_select,sf_select + (period_select * reservation_counter)]=1     # This also selects a 1 in the reserved spots

        # results_yessir=np.argwhere(V2Xpool == 1)     # Cool for debugging


        ######## Now onto the code that tests to see if there are any collisions .########
        # We are going to use these parameters to control the addition of
        # Matrices within the Multidimensional Matrix. I will add elements in the
        # matrix that are on the same position at the same time and move up until
        # i add for the whole matrix. Places where the matrix is more than 1
        # represent a collision.

        V2X_collision_detector=np.zeros([NumSubChannels,NumSubframes])
        
        for vehicle_num_collision in range(0,(NumVehicles - 1)):
            if vehicle_num_collision == 1:
                V2X_collision_detector=V2X_collision_detector + V2Xpool[vehicle_num_collision,:,:] + V2Xpool[vehicle_num_collision + 1,:,:]
                # V2X_collision_detector=V2X_collision_detector + V2Xpool(np.arange(),np.arange(),vehicle_num_collision) + V2Xpool(np.arange(),np.arange(),vehicle_num_collision + 1)

            elif vehicle_num_collision > 1:
                V2X_collision_detector=V2X_collision_detector + V2Xpool[vehicle_num_collision + 1,:,:]

            collision_greater_than_one=np.argwhere(V2X_collision_detector > 1)  # shows the places in the collision detection matrix where the number is greater than one
            results_yeah3=np.argwhere(V2X_collision_detector > 1)   # Cool for debugging


        # results_yeah=np.argwhere(V2Xpool == 1)          # Cool for debugging


        #Reselection Loop
        #Selection of the selection window
        last_subframe=sf_select + (period_select * reservation_counter)
        infinity_duckin=0
        
        while last_subframe < NumSubframes:
        # if last_subframe < NumSubframes:
            prob_reselection=random.uniform(0,1)       #f rand is greater than 0.8 then we keep the pattern we had before reselection. If less than, we have to select with a new pattern
            
            if prob_reselection <= 0.8:                                 # Keep the same pattern
                # period_select=100                                       # This is for periodicity. can reserve a subframe
                period_select=periodicity                                       # This is for periodicity. can reserve a subframe
                # mult_Periodicity=random.randint(5,15)                 # These are the number of times the vehicle can reserve.
                mult_Periodicity=reselectionCounter                 # These are the number of times the vehicle can reserve.
                sc_select=sc_select + 1 - 1                             # The position of the subchannel remain the same
                sf_select=last_subframe + period_select
                if sf_select < NumSubframes:
                    while V2X_collision_detector[sc_select-1,sf_select-1] == 1:
                            while infinity_duckin < 1000:
                                sf_select=last_subframe + period_select + random.randint(1,100) # Select another resource that is just near the one you were supposed to occupy BUT is unoccuped
                                sc_select=random.randint(1,NumSubChannels)
                                infinity_duckin=infinity_duckin + 1

                            if infinity_duckin >= 100:
                                # print('sc_select: ', sc_select)
                                # print('sf_select: ', sf_select)
                                if sf_select>2000:
                                    sf_select=2000
                                # print('indexxxx===>', sc_select-1,sf_select-1)
                                V2X_collision_detector[sc_select-1,sf_select-1]=0           # Cheating the infinity loop. I will make V2X_collision_detector( sc_select, sf_select) = 1 again just after the loop is terminated


                    while V2X_collision_detector[sc_select-1,sf_select-1] >= 777:       # If the resource has been selected already
                        while infinity_duckin < 100:                                # to avoid infinity loop
                            sf_select=last_subframe + period_select + random.randint(1,100)     # Select another resource that is just near the one you were supposed to occupy BUT is unoccuped
                            sc_select=random.randint(1,NumSubChannels)
                            infinity_duckin=infinity_duckin + 1
                        if infinity_duckin >= 100:
                            V2X_collision_detector[sc_select-1,sf_select-1]=0           # Cheating the infinity loop. I will make V2X_collision_detector( sc_select, sf_select) = 1 again just after the loop is terminated

                    if infinity_duckin >= 100:
                        V2X_collision_detector[sc_select-1,sf_select-1]=1               # Letting the pool remain as it was. The last sf_select will be automatically chosen even though a collision will happen

                    for reservation_counter in range(1,mult_Periodicity):
                        if (sf_select + (period_select*reservation_counter)) < NumSubframes:                    # We should not have more subframes than the predefined
                            V2Xpool[vehic_select,sc_select-1,sf_select + (period_select*reservation_counter)-1]=1   # This also selects a 1 in the reserved spots

            if prob_reselection > 0.8:                                          # Find a new pattern for transmission
                # period_select=100                                       # This is for periodicity. can reserve a subframe
                period_select=periodicity                                       # This is for periodicity. can reserve a subframe
                # mult_Periodicity=random.randint(5,15)                         # These are the number of times the vehicle can reserve.
                mult_Periodicity=reselectionCounter                         # These are the number of times the vehicle can reserve.
                sc_select=random.randint(1,NumSubChannels)                    # This randomly chooses the subchannel from which the RB will be selected
                sf_select=last_subframe + random.randint(3,100)               # select another subframe
                if sf_select < NumSubframes:
                    while V2X_collision_detector[sc_select-1,sf_select-1] == 1:
                        while infinity_duckin < 100:
                            sf_select=sf_select + random.randint(1,100)         # Select another resource that is just near the one you were supposed to occupy BUT is unoccuped
                            while sf_select > NumSubframes:
                                sf_select=sf_select - random.randint(1,100)
                            sc_select=random.randint(1,NumSubChannels)
                            infinity_duckin=infinity_duckin + 1

                        if infinity_duckin >= 100:
                            V2X_collision_detector[sc_select-1,sf_select-1]=0       # Cheating the infinity loop. I will make V2X_collision_detector( sc_select, sf_select) = 1 again just after the loop is terminated

                    while V2X_collision_detector[sc_select-1,sf_select-1] >= 777:   # If the resource has been selected already
                        while infinity_duckin < 100:                            # to avoid infinity loop
                            sf_select=sf_select + random.randint(1,100)         # Select another resource that is just near the one you were supposed to occupy BUT is unoccuped
                            # randi(1,100)
                            while sf_select > NumSubframes:
                                sf_select=sf_select - random.randint(1,100)
                            sc_select=random.randint(1,NumSubChannels)
                            infinity_duckin=infinity_duckin + 1

                        if infinity_duckin >= 100:
                            V2X_collision_detector[sc_select-1,sf_select-1]=0       # Cheating the infinity loop. I will make V2X_collision_detector( sc_select, sf_select) = 1 again just after the loop is terminated

                    if infinity_duckin >= 100:
                        V2X_collision_detector[sc_select-1,sf_select-1]=1           # Letting the pool remain as it was. The last sf_select will be automatically chosen even though a collision will happen

                    for reservation_counter in range(1,mult_Periodicity):
                        if (sf_select + (period_select*reservation_counter)) < NumSubframes:                    # We should not have more subframes than the predefined
                            V2Xpool[vehic_select,sc_select-1,sf_select + (period_select*reservation_counter)-1]=1   # This also selects a 1 in the reserved spots

            last_subframe=sf_select + (period_select*reservation_counter)

        
        
    # Probability Code
    num_of_elements=0               # Initialization: This will add all the elements in the matrix
    
    for m in range(0,NumSubframes):          # rows
        for n in range(0,NumSubChannels):    # colums
            if V2X_collision_detector[n,m] != 0:
                if V2X_collision_detector[n,m] != (NumVehicles*777):
                    if V2X_collision_detector[n,m] < 777:
                        add=V2X_collision_detector[n,m]
                        num_of_elements=num_of_elements + add
                        add=0


    all_selections=np.argwhere(V2X_collision_detector >= 1)         # Finding the total number of selected resources
    all_selections_length=len(all_selections)
    # print('all_selections_length: ', all_selections_length)

    # sensing_selections=np.argwhere(V2X_collision_detector == (NumVehicles*777))
    sensing_selections=np.argwhere(V2X_collision_detector >= (777))
    sensing_selections_length=len(sensing_selections)
    # print('sensing_selections_length: ', sensing_selections_length)
    
    total_selections = all_selections_length - sensing_selections_length  # These are the total number of selections made from the selection window
    # print('total_selections: ', total_selections)
    
    total_collisions = num_of_elements - total_selections
    if total_collisions < 0:
        total_collisions=0
        
    bamm=len(np.argwhere(V2X_collision_detector[:,:] >= 2))
    bamm2=len(np.argwhere(V2X_collision_detector[:,:] >= 100))
    real_collisions=bamm - bamm2

    Probability_of_collision=total_collisions / total_selections
    # print('Probability_of_collision: ', Probability_of_collision)
    Probability_of_real_collision=real_collisions / total_selections
    # print ('Probability_of_real_collision: ', Probability_of_real_collision)
    # print('-----')
    return Probability_of_real_collision