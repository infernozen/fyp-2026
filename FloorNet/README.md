# FloorNet

## Overview
FloorNet is a deep learning framework for reconstructing vector-graphic floorplans from RGBD indoor video sequences. The architecture integrates three branches:
- **PointNet Branch** – processes 3D point clouds  
- **Floorplan Branch** – estimates 2D spatial layouts  
- **Image Branch** – extracts RGB visual features  

A built-in Integer Programming solver (`IP.py`) is provided as a free alternative to Gurobi.

## Dataset
All data must be placed in the `data/` directory before execution.

### Preprocessed Dataset (TFRecords)
- https://drive.google.com/open?id=16lyX_xTiALUzKyst86WJHlhpTDr8XPF_  
- https://mega.nz/#F!5yQy0b5T!ykkR4dqwGO9J5EwnKT_GBw  

### Raw Dataset Components
- Point Clouds: https://drive.google.com/open?id=1JJlD0qsgMpiU5Jq9TNm3uDPjvqi88aZn  
- Annotations: https://drive.google.com/open?id=1hYDE2SXLA8Cq7LEK67xO-UMeTSPJ5rcB  
- Associations: https://drive.google.com/open?id=125TAmYWk22EyzCdlbGIfX4Z4DRMhru_V  

### Custom Data
- Example: https://mega.nz/#!dnohjKZa!I3NJZ806vNK-UYp-ap7OynGnS5E-E5AK_z5WsX8n1Ls  

Custom datasets must be converted into TFRecords following the structure in `RecordWriterTango.py` or `RecordWriterCustom.py`.

Each sample (`tf.train.Example`) should include:
- **Inputs:**  
  - Point cloud (50,000 sampled points)  
  - 3D → 2D mapping indices (256×256 grid)  
  - Optional RGB image features  
- **Labels:**  
  - Corner coordinates and types  
  - Number of corners  
  - Icon segmentation map  
  - Room segmentation map  



## Requirements

### Software
- Python 2.7  
- TensorFlow ≥ 1.3  
- NumPy  
- OpenCV 3  
- CUDA ≥ 8.0  
- Gurobi (optional) or built-in `IP.py`  

### Hardware
- CUDA-enabled GPU (recommended)  
- Minimum 8GB RAM (16GB recommended)  


## Execution

### 1. Data Preparation
Convert dataset into TFRecords format:
```
python RecordWriterTango.py
python RecordWriterCustom.py
```

### Training
### Train from scratch
Train the model from scratch or resume from checkpoint:
```
python train.py --restore=0
```

### Resume training
```
python train.py --restore=1
```

### Evaluation
Evaluate a trained model:
```
python train.py --task=evaluate --separateIconLoss
```
