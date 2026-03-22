# Plan2Scene

## About the Module
Plan2Scene is a framework for converting 2D floorplans and associated images into fully textured 3D indoor scenes. It generates structured 3D meshes by combining layout understanding, texture synthesis, and texture propagation techniques.

## Dataset Source

### Rent3D++ Dataset
- https://forms.gle/mKAmnrzAm3LCK9ua6  

Place dataset in:
```
[PROJECT_ROOT]/data
```

### Optional Datasets
- Stationary Textures Dataset  
- Substance Mapped Textures Dataset  


## Software and Hardware Requirements

### Software
- Python (Conda environment)  
- Project dependencies  
- Embark texture-synthesis CLI  

### Hardware
- GPU recommended  
- Adequate storage  

## Execution Instructions

### 1. Environment Setup
```
export PYTHONPATH=./code/src
```

Download texture synthesis binary:
https://github.com/EmbarkStudios/texture-synthesis/releases  

Download seam mask:
https://github.com/EmbarkStudios/texture-synthesis/blob/main/imgs/masks/1_tile.jpg  

Rename config:
```
./conf/plan2scene/seam_correct-example.json → seam_correct.json
```


### 2. Data Preparation
```
python code/scripts/plan2scene/preprocessing/generate_reference_crops.py ./data/processed/gt_reference/train ./data/input/photo_assignments/train train
python code/scripts/plan2scene/preprocessing/generate_reference_crops.py ./data/processed/gt_reference/val ./data/input/photo_assignments/val val
python code/scripts/plan2scene/preprocessing/generate_reference_crops.py ./data/processed/gt_reference/test ./data/input/photo_assignments/test test
```


### 3. Inference
```
python code/scripts/plan2scene/preprocessing/fill_room_embeddings.py ./data/processed/texture_gen/test/drop_0.0 test --drop 0.0
python code/scripts/plan2scene/crop_select/vgg_crop_selector.py ./data/processed/vgg_crop_select/test/drop_0.0 ./data/processed/texture_gen/test/drop_0.0 test --drop 0.0
```

```
python code/scripts/plan2scene/texture_prop/gnn_texture_prop.py ./data/processed/gnn_prop/test/drop_0.0 ./data/processed/vgg_crop_select/test/drop_0.0 test GNN_PROP_CONF_PATH GNN_PROP_CHECKPOINT_PATH --keep-existing-predictions --drop 0.0
```


### 4. Post-processing
```
python code/scripts/plan2scene/postprocessing/seam_correct_textures.py ./data/processed/gnn_prop/test/drop_0.0/tileable_texture_crops ./data/processed/gnn_prop/test/drop_0.0/texture_crops test --drop 0.0
```

```
python code/scripts/plan2scene/postprocessing/embed_textures.py ./data/processed/gnn_prop/test/drop_0.0/archs ./data/processed/gnn_prop/test/drop_0.0/tileable_texture_crops test --drop 0.0
```

```
CUDA_VISIBLE_DEVICES=0 python code/scripts/plan2scene/render_house_jsons.py ./data/processed/gnn_prop/test/drop_0.0/archs --scene-json
```


### 5. Evaluation
```
python code/scripts/plan2scene/test.py ./data/processed/gnn_prop/test/drop_0.6/tileable_texture_crops ./data/processed/gt_reference/test/texture_crops test
```
