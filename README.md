# AIstinct

This is the course project from School of Future Technology in SCUT

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/YinBo0927/AI_interior_decoration_design_assistant/">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <strong><h4 align="center">AIstinct</h4></strong>
  <p align="center">
    <h3 align="center">Design spaces. Get creative.</h3>
    <strong><h3 align="center">Elevate your living.</h3></strong>
    <p align="center">Easy to explore. Friendly to use. Just ask and AIstinct can <br />
    assist with interior design, Q&A, brainstroming, and more.
    </p>
    <p align="center">
      <a href="http://8.138.90.231:8503/">View Demo</a>
      ·
      <a href="https://github.com/YinBo0927/AI_interior_decoration_design_assistant/issues">Report Bugs</a>
      ·
      <a href="https://github.com/YinBo0927/AI_interior_decoration_design_assistant/issues">Propose New Features</a>
    </p>
  </p>
</p>

 
## Catalogue

- [AIstinct](#aistinct)
  - [Catalogue](#catalogue)
  - [Getting Started Guide](#getting-started-guide)
    - [Reference Configuration](#reference-configuration)
      - [Deployment and Startup](#deployment-and-startup)
          - [1.Front-end applications](#1front-end-applications)
          - [2.back-end applications](#2back-end-applications)
  - [Copyright Notice](#copyright-notice)
  - [Thanks](#thanks)

## Getting Started Guide


###### Reference Configuration

PyTorch: 2.1.0 <br />
Python: 3.10(ubuntu22.04) <br />
Cuda: 12.1<br />
GPU: RTX 4090(24GB) * 1<br />
CPU: 12 vCPU Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz<br />
Memory: 90GB<br />
Hard disk: 50GB<br />

#### Deployment and Startup

###### 1.Front-end applications
Step 1: Install front-end project dependencies

```sh
git pip install -r requirements.txt
```
Step 2: Start the front-end project process


```sh
streamlit run start.py
```

###### 2.back-end applications 

Step 1: Deploy [3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting/tree/master?tab=readme-ov-file)
```sh
git clone https://github.com/vt-vl-lab/3d-photo-inpainting.git
cd 3d-photo-inpainting
sh download.sh
pip install -r requirements.txt
cd ..
```
Replacing and Adding Project Files
```sh
cp -r ./3d/* ./3d-photo-inpainting
```
Step 2: Deploy [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui.git)
```sh
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
pip install -r requirements_versions.txt
pip install -r requirements.txt
cd ..
```
Download the Lora model and basic model
```sh
cd stable-diffusion-webui/models/Lora
wget https://huggingface.co/CreeperCatcher/AIstinct/resolve/main/FT_lora.safetensors?download=true
cd ../Stable-diffusion
wget https://civitai.com/api/download/models/50722
cd ../../..
```

Install sd-extension [controlnet](https://github.com/Mikubill/sd-webui-controlnet) and download the controllnet model
```sh
cd stable-diffusion-webui/extensions
git clone https://github.com/Mikubill/sd-webui-controlnet.git
cd sd-webui-controlnet/models

wget https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors?download=true
wget https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_canny_fp16.safetensors?download=true
wget https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors?download=true
wget https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors?download=true
cd ../../..
```
Step 3: Start the backend project process
Start the 3D-photo-painting process
```sh
python 3d-photo-inpainting/api.py
``` 
Launching the stable-diffusion-webui process without an interface
```sh
python stable-diffusion-webui/launch.py --port 6006 --nowebui
```

## Copyright Notice

This project has signed a MIT authorization license, please refer to  [LICENSE.txt](https://github.com/YinBo0927/AI_interior_decoration_design_assistant/LICENSE.txt) for details

## Thanks


- [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui.git)
- [3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting/tree/master?tab=readme-ov-file)
- [streamlit](https://streamlit.io/)
- [XSarchitectural](https://civitai.com/models/28112/xsarchitectural-interiordesign-forxslora)

<!-- links -->
[your-project-path]:https://github.com/YinBo0927/AI_interior_decoration_design_assistant
[contributors-shield]: https://img.shields.io/github/contributors/YinBo0927/AI_interior_decoration_design_assistant.svg?style=flat-square
[contributors-url]: https://github.com/YinBo0927/AI_interior_decoration_design_assistant/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/YinBo0927/AI_interior_decoration_design_assistant.svg?style=flat-square
[forks-url]: https://github.com/YinBo0927/AI_interior_decoration_design_assistant/network/members
[stars-shield]: https://img.shields.io/github/stars/YinBo0927/AI_interior_decoration_design_assistant.svg?style=flat-square
[stars-url]: https://github.com/YinBo0927/AI_interior_decoration_design_assistant/stargazers
[issues-shield]: https://img.shields.io/github/issues/YinBo0927/AI_interior_decoration_design_assistant.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/YinBo0927/AI_interior_decoration_design_assistant.svg
[license-shield]: https://img.shields.io/github/license/YinBo0927/AI_interior_decoration_design_assistant.svg?style=flat-square
[license-url]: https://github.com/YinBo0927/AI_interior_decoration_design_assistant/blob/master/LICENSE.txt

