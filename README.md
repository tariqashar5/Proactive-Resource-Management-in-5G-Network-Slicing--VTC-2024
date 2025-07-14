# 📘 Proactive Resource Management for Seamless Service: A Transition from 5G-Basic to 5G-Advanced Network Slicing

This repository contains the code and supporting files for the research paper:

**Title:** *Proactive Resource Management for Seamless Service: A Transition from 5G-Basic to 5G-Advanced Network Slicing*  
**Authors:** Muhammad Ashar Tariq, Malik Muhammad Saad, Mahnoor Ajmal, Donghyun Jeon, Jinhong Kim, Dongkyun Kim  
**Affiliations:**  
- School of Computer Science and Engineering, Kyungpook National University, Republic of Korea  
- Electronics and Telecommunications Research Institute (ETRI), Daegu, Republic of Korea  

📄 This work proposes an intelligent slice traffic demand prediction and resource reallocation scheme to reduce service interruption in 5G-Advanced networks.

> If you use this code, methodology, or data in your work, **please cite our paper** (see citation section below).

 ---
 
> ## 📌 Overview

As 5G evolves toward 5G-Advanced, network slicing has become a critical enabler of service-specific connectivity. However, service interruptions due to **non-uniform slice deployment** and lack of **predictive resource management** remain major challenges — especially when User Equipment (UE) moves between Tracking Areas (TAs) within a Registration Area (RA).

This work provides:
- A comprehensive analysis of network slicing evolution from 4G-LTE to 5G-Advanced (3GPP Releases 13–18)
- Identification of key **Release 18 challenges**, such as slice unavailability and limited UE control
- A proposed solution that combines:
  - **Long Short-Term Memory (LSTM)** for predicting slice-specific traffic demand
  - **Dynamic Proportional Resource Allocation (DPRA)** for proactively reconfiguring slice resources based on predictions

By forecasting slice demands in advance and reallocating resources accordingly, the proposed scheme aims to **minimize service interruptions** and enable **seamless service continuity** for mobile users in future 5G deployments.

---

## 🧠 Key Contributions

This work bridges the gap between 5G network slicing theory and real-world deployment challenges by offering both a survey of standardization progress and a practical ML-based solution. The key contributions include:

- 📚 **Evolutionary Review**: A detailed summary of network slicing enhancements across 3GPP Releases 13 to 18, from DECOR in LTE to advanced slicing features in 5G-Advanced.

- 🚧 **Challenge Identification**: Highlights critical 5G-Advanced issues such as:
  - Non-uniform slice deployment within a Registration Area (RA)
  - Service interruption during inter-TA UE mobility
  - Limited operator control over UE slice registration
  - Inefficient slice utilization

- 🔍 **Prediction-Based Solution**: Introduces an **LSTM-based traffic demand prediction model** that forecasts per-slice service requests at the TA level.

- ⚙️ **Dynamic Resource Reallocation**: Implements **Dynamic Proportional Resource Allocation (DPRA)** to adjust resource distribution among slices proactively, based on predicted demands and SLA requirements.

- 📊 **Performance Gains**: Demonstrates, via simulation, improved:
  - Service continuity
  - Resource utilization
  - Packet Delivery Ratio (PDR) compared to baseline methods (fixed/random allocation)

---

## 📁 Project Structure

The repository is organized as follows:

```bash
.
├── data/                          # Contains input slice traffic data used for prediction
│   ├── test.csv
│   ├── train.csv
│   └── data.py                        # Data Preprocessing
├── sps_mat/                       # Implementation of SPS (Semi-Persistent Scheduling) algorithm
├── traffic_per_hour_original.csv  # Combined ground truth traffic demand across slices
├── traffic_per_hour_predicted.csv # LSTM-predicted traffic demand per slice
├── main                           # Main script for running prediction + DPRA
└── README.md                      # Project documentation (you’re here!)
```

---

## 📊 Results & Evaluation

The effectiveness of the proposed LSTM + DPRA approach is evaluated in terms of:

- **Prediction Accuracy**: LSTM forecasts slice-wise traffic demand with rapid convergence and low training loss (near-zero within 100 epochs).
- **Proactive Resource Allocation**: DPRA dynamically reconfigures slice resources based on predicted demand and SLA requirements.
- **Improved Service Delivery**: The approach significantly reduces service interruption and increases Packet Delivery Ratio (PDR) across slices compared to baseline fixed and random allocation schemes.

### 🔍 Evaluation Highlights:
- Average traffic demand and PDR improvements are shown in comparison plots.
- The predicted demand triggered the creation or remapping of slices (e.g., Industry 4.0) in Tracking Areas with no prior allocation.
- Results demonstrate clear gains in slice utilization and QoS consistency.

📄 **For detailed simulation settings, figures, and quantitative results, please refer to the published manuscript.**

---

## 📚 Citation

If you use this codebase, dataset, or methodology in your research, please cite the following paper:
https://ieeexplore.ieee.org/document/10757954 (DOI: 10.1109/VTC2024-Fall63153.2024.10757954)

```bibtex
@inproceedings{tariq2024proactive,
  title={Proactive Resource Management for Seamless Service: A Transition from 5G-Basic to 5G-Advanced Network Slicing},
  author={Tariq, Muhammad Ashar and Saad, Malik Muhammad and Ajmal, Mahnoor and Jeon, Donghyun and Kim, Jinhong and Kim, Dongkyun},
  booktitle={2024 IEEE 100th Vehicular Technology Conference (VTC2024-Fall)},
  pages={1--7},
  year={2024},
  organization={IEEE}
}
```

---

## 📬 Contact

For questions, collaborations, or further information, feel free to reach out:

- 📧 Muhammad Ashar Tariq — [tariqashar5@gmail.com](mailto:tariqashar5@gmail.com)

---

## 🔒 License

This repository is intended for **academic and research purposes only**.  
Please contact the authors for permission regarding commercial use or redistribution.

---
