# Instruction
We are honored to participate in the 2024 MMVRAC. This documentation summarizes our results and gives information such as dependencies for the codes, how to train/test, etc. according to the competition requirements.

<!-- ## Participants
+ Wei Liu
+ Xingyu Zhu -->


## Directory Structure

```
MMVRAC
│  ensemble.py # ensemble different mod
│  **environment.yml** # dependencies for the codes
│  KLLoss.py
│  LICENSE
│  **main_multipart_uav.py** # train/eval uav
│  README.md
│  run.sh
│  Text_Prompt.py # tokeniz the prompts
│  tools.py
│  tree.txt
│  utils.py
│  
├─**clip**
│  └─ ---text encoder files---
│          
├─config
│   └─ ---train/test yaml files---    
├─data
│  └─uav
│      │  get_raw_denoised_data.py
│      │  get_raw_skes_data.py
│      │  seq_transformation.py
│      │  [**UAV_XSub_V1.npz**](https://drive.google.com/file/d/1iik6pBTtyCEuBfj6_bU-xa5CE2G3urDB/view?usp=drive_link)
│      │  [**UAV_XSub_V2.npz**](https://drive.google.com/file/d/151I1a1CQ7nRQGqJsBhDOx5T_xQ1RY2hm/view?usp=drive_link)
│      │  
│      └─statistics  # preprocess files
├─feeders
│  └─ ---dataloader files---
├─graph
│  └─ ---adjacency matrix files---
│          
├─**model**
│  └─ ---skeleton encoder files---
│          
├─**text**
│      uav_label_map.txt
│      uav_motion_describe.txt
│      uav_motion_details.txt
│      uav_pasta_openai.txt
│      uav_synonym_openai.txt
│      uav_used_parts-openai.txt
│      
├─torchlight
└─**work_dir**
```


pretrained models can be find at work_dir such as:
 **'[work_dir/uav](https://drive.google.com/drive/folders/1jO65IXbDQuC_1aFIYoEJZGdanS2alB4b?usp=drive_link)/my/lst_joint/xsub_v1/runs-92-15364.pt'**
 



## Dependencies for the codes
The main environment configuration is as follows,
- python=3.8.13
- torch=1.8.1
- torchvision=0.2.1
- PyYAML, tqdm, tensorboardX


We provide the dependency file of our experimental environment [environment.yml](./environment.yml), you can install all dependencies by creating a new anaconda virtual environment and running `conda env create -f environment.yml `
- run `pip install -e torchlight` 



## Data Processing

#### Directory Structure

Put downloaded data into the following directory structure:
```
- data/
  - uav_skeleton_raw/ fr
      ... # raw data of UAV-Human
```

### Generate data.npz
relevant files have been uploaded, so this step isn't necessary.

- Generate uav/statistics
```
cd ./data/uav/statistics
python extract_statistics.py
```

- Generate UAV_XSub_V1.npz & UAV_XSub_V1.npz:
```
 cd ./data/uav
 python get_raw_skes_data.py
 python get_raw_denoised_data.py
 python seq_transformation.py
```


## Training & Testing

### Training

- To train model on UAV-Human

```
# Example1: train model on UAV_XSub_V1(joint modality)
CUDA_VISIBLE_DEVICES=0 python main_multipart_uav.py --config config/uav-cross-subject/lst_joint_v1.yaml --model model.ctrgcn.Model_lst_4part_uav --work-dir work_dir/uav/my/xsub_v1/lst_joint --device 0 --log-interval 5 --save-interval 1
# Example2: train model on UAV_XSub_V1(bone modality)
CUDA_VISIBLE_DEVICES=0 python main_multipart_uav.py --config config/uav-cross-subject/lst_bone_v1.yaml --model model.ctrgcn.Model_lst_4part_uav_bone --work-dir work_dir/uav/my/xsub_v1/lst_bone --device 0 --log-interval 5 --save-interval 1
# Example3: train model on UAV_XSub_V1(joint + motion modality)
CUDA_VISIBLE_DEVICES=0 python main_multipart_uav.py --config config/uav-cross-subject/lst_joint_vel_v1.yaml --model model.ctrgcn.Model_lst_4part_uav --work-dir work_dir/uav/my/xsub_v1/lst_joint_motion --device 0 --log-interval 5 --save-interval 1  
# Example4: train model on UAV_XSub_V1(bone + motion modality)
CUDA_VISIBLE_DEVICES=0 python main_multipart_uav.py --config config/uav-cross-subject/lst_bone_vel_v1.yaml --model model.ctrgcn.Model_lst_4part_uav_bone --work-dir work_dir/uav/my/xsub_v1/lst_bone_motion --device 0 --log-interval 5 --save-interval 1
```


### ensemble joint,motion and bone information
```
# Example: ensemble four modalities on UAV-Human cross subject v1
python ensemble.py --dataset uav/xsub_v1 --joint-dir work_dir/uav/my/xsub_v1/lst_joint --bone-dir work_dir/uav/my/xsub_v1/lst_bone --joint-motion-dir work_dir/uav/my/xsub_v1/lst_joint_motion --bone-motion-dir work_dir/uav/my/xsub_v1/lst_bone_motion
# Example: ensemble four modalities on UAV-Human cross subject v2
python ensemble.py --dataset uav/xsub_v2 --joint-dir work_dir/uav/my/xsub_v2/lst_joint --bone-dir work_dir/uav/my/xsub_v2/lst_bone --joint-motion-dir work_dir/uav/my/xsub_v2/lst_joint_motion --bone-motion-dir work_dir/uav/my/xsub_v2/lst_bone_motion
```


### Testing

- To test the trained models saved in <work_dir>, run the following command:

```
python main_multipart_uav.py --config <work_dir>/config.yaml --work-dir <work_dir> --phase test --save-score True --weights <work_dir>/xxx.pt --device 0
```




#### Evaluation on UAVHuman-Skeleton 


| Methods   | CSv1 - Top1 (%) | CSv1 - Top5 (%) | CSv2 - Top1 (%) | CSv2 - Top5 (%) |
| --------- | --------------- | --------------- | --------------- | --------------- |
| DGNN      |  29.90          |  -              |  -              |  -              |
| ST-GCN    |  30.25          |  -              |  56.14          |  -              |
| 2s-AGCN   |  34.84          |  -              |  66.68          |  -              |
| HARD-Net  |  36.97          |  -              |  36.97          |  -              |
| Shift-GCN |  37.98          |  -              |  67.04          |  -              |
| **Our Experiments** | **45.68**  | **65.28**  |   **74.34**     |   **93.51**     |







## Acknowledgements
The base skeleton-encoder is [CTR-GCN](https://github.com/Uason-Chen/CTR-GCN).We referred to the [LST](https://arxiv.org/abs/2208.05318), including data preprocessing and model training, and modified the data preprocessing file according to the differences between the UAV-Huamn dataset and the NTU data set (such as the number of labels, storage format). We used the LST training idea, And using pre-trained large-scale language models as knowledge engines, several different text prompts are designed for the training on UAV-Human dataset, such as:
+ Understand the action in detail, give which of the following body parts will move when [action]: head, hand, arm, hip, leg, foot
+ Understand the action, suggest 10 synonyms for {category}
+ Provide motion descripitons for the action in detail:{category}
+ Express the action of{category} with the body parts: head, hand, arm, hip, leg, foot.

These generated prompts can be used to reduce useless information and assist training, enrich global features, enhance global features, and learn local features.

Thanks to the original authors for their work! 
Thanks the organizers for giving us this opportunity to improve and test ourselves!


New results will be uploaded soon...




