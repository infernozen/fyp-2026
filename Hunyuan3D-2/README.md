# Hunyuan3D

## About the Module
Hunyuan3D is a large-scale 3D generation framework for creating high-quality textured 3D assets from images. It consists of two main components:
- Shape generation model (Hunyuan3D-DiT)  
- Texture synthesis model (Hunyuan3D-Paint)  

The system follows a two-stage pipeline: first generating a base mesh, then applying texture synthesis.


## Dataset / Model Sources

Pretrained models are available from:
- https://huggingface.co/tencent/Hunyuan3D-2  
- https://huggingface.co/tencent/Hunyuan3D-2mini  
- https://huggingface.co/tencent/Hunyuan3D-2mv  

Demo and usage:
- https://huggingface.co/spaces/tencent/Hunyuan3D-2  
- https://3d.hunyuan.tencent.com  


## Software and Hardware Requirements

### Software
- Python 3.8+  
- PyTorch  
- pip / virtual environment  
- Additional dependencies from `requirements.txt`  

### Hardware
- GPU required  
- Minimum 6GB VRAM (shape generation)  
- ~16GB VRAM for full pipeline (shape + texture)  



## Execution Instructions

### 1. Installation
```bash
pip install -r requirements.txt
pip install -e .

cd hy3dgen/texgen/custom_rasterizer
python setup.py install

cd ../differentiable_renderer
python setup.py install
```

### 2. Basic Usage (Image → 3D Shape)
```bash
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(image='assets/demo.png')[0]
```

### 3. Texture Generation
```bash
from hy3dgen.texgen import Hunyuan3DPaintPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(image='assets/demo.png')[0]

pipeline = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')
mesh = pipeline(mesh, image='assets/demo.png')
```

### 4. Run Gradio Interface
```bash
python3 gradio_app.py --model_path tencent/Hunyuan3D-2 --subfolder hunyuan3d-dit-v2-0 --texgen_model_path tencent/Hunyuan3D-2 --low_vram_mode
```

### 5. Run API Server
```bash
python api_server.py --host 0.0.0.0 --port 8080
```

Example request:

```bash
img_b64_str=$(base64 -i assets/demo.png)

curl -X POST "http://localhost:8080/generate" \
  -H "Content-Type: application/json" \
  -d '{
        "image": "'"$img_b64_str"'"
      }' \
  -o output.glb
```
