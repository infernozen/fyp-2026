# MASt3R-SLAM

## About the Module
MASt3R-SLAM is a real-time dense SLAM system that leverages 3D reconstruction priors to perform accurate tracking and mapping from RGB or RGB-D inputs. It supports video input, image sequences, and live camera streams.

## Dataset Source

### TUM-RGBD
```
bash ./scripts/download_tum.sh
```

### 7-Scenes
```
bash ./scripts/download_7_scenes.sh
```

### EuRoC
```
bash ./scripts/download_euroc.sh
```

### ETH3D
```
bash ./scripts/download_eth3d.sh
```


## Software and Hardware Requirements

### Software
- Python 3.11
- PyTorch 2.5.1
- CUDA (11.8 / 12.1 / 12.4)

### Hardware
- GPU required (RTX recommended)


## Execution Instructions

### 1. Environment Setup
```
conda create -n mast3r-slam python=3.11
conda activate mast3r-slam
```

### 2. Install PyTorch (match CUDA)
```
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. Installation
```
git clone [https://github.com/rmurai0610/MASt3R-SLAM.git](https://github.com/infernozen/fyp-2026.git --recursive
cd MASt3R-SLAM

pip install -e thirdparty/mast3r
pip install -e thirdparty/in3d
pip install --no-build-isolation -e .
```

### 4. Setup Checkpoints
```
mkdir -p checkpoints/

wget https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth -P checkpoints/
```

### 5. Run Example
```
python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room/ --config config/calib.yaml
```

### 6. Evaluation
```
bash ./scripts/eval_tum.sh
```
