# Orchestrator

## About the Module
Orchestrator is a framework for compositional visual planning and generation using large language models. It generates structured 2D layouts and 3D indoor scenes from textual prompts, supporting downstream image and scene synthesis.


## Dataset Source

### 2D Layout Dataset (NSR-1K)
- Provided in ./dataset/NSR-1K/

### 3D Scene Dataset
- 3D-FUTURE: https://tianchi.aliyun.com/dataset/98063  
- Preprocessed data: https://drive.google.com/file/d/1NV3pmRpWcehPO5iKJPmShsRp_lNbxJuK/view  

Place data in:
```
./ATISS/
```


## Software and Hardware Requirements

### Software
- Python 3.8  
- Conda  
- PyTorch  
- Dependencies from requirements.txt  
- GLIGEN, GLIP, ATISS modules  

### Hardware
- RTX GPU recommended for generation and rendering  

## Execution Instructions

### 1. Installation
```
conda create -n layoutgpt python=3.8 -y
pip install -r requirements.txt
```

Download checkpoints:
```
wget https://huggingface.co/gligen/gligen-generation-text-box/resolve/main/diffusion_pytorch_model.bin -O gligen/gligen_checkpoints/checkpoint_generation_text.pth
```

Setup GLIP:
```
cd eval_models/GLIP
python setup.py build develop --user
```

Setup ATISS:
```
cd ATISS
python setup.py build_ext --inplace
pip install -e .
```


### 2. Data Preparation
```
cd ATISS
unzip 3D-FUTURE-model.zip -d 3D-FUTURE
unzip data_output.zip
```

### 3. 2D Layout Generation
```
python run_layoutgpt_2d.py --icl_type k-similar --K 8 --setting counting --llm_type gpt4 --n_iter 5
```

Generate images:
```
cd gligen
python gligen_layout_counting.py --file ../llm_output/counting/output.json --batch_size 5
```


### 4. 2D Evaluation
```
python eval_counting_layout.py --file output.json
```

```
cd eval_models/GLIP
python eval_counting.py --dir path_to_generated_images
```


### 5. 3D Scene Generation
```
python run_layoutgpt_3d.py --dataset_dir ./ATISS/data_output --icl_type k-similar --K 8 --room bedroom --llm_type gpt4 --unit px --normalize --regular_floor_plan
```


### 6. 3D Evaluation
```
python eval_scene_layout.py --dataset_dir ./ATISS/data_output --file ./llm_output/3D/output.json --room bedroom
```


### 7. Visualization (Blender)
```
cd ATISS/scripts
python render_from_files.py config.yaml visualization data.pkl textures output.json --export_scene
```

```
blender -b -P render_with_blender.py -- --input_dir scene_dir --output_dir output.png --camera_position 0 0 5
```
