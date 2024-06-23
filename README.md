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
    <strong><h3 align="center">Elevate your living.</h3><strong>
    <p align="center">Easy to explore. Friendly to use. Just ask and AIstinct can <br>
    assist with interior design, Q&A, brainstroming, and more.
    </p>
    <p align="center">
    <a href="http://8.138.90.231:8503/">查看Demo</a>
    ·
    <a href="https://github.com/YinBo0927/AI_interior_decoration_design_assistant/issues">报告Bug</a>
    ·
    <a href="https://github.com/YinBo0927/AI_interior_decoration_design_assistant/issues">提出新特性</a>
    </p>
  </p>
</p>

 
## 目录

- [AIstinct](#aistinct)
  - [目录](#目录)
  - [上手指南](#上手指南)
          - [参考配置](#参考配置)
      - [**部署与启动**](#部署与启动)
          - [1.前端应用部署与启动](#1前端应用部署与启动)
          - [2.后端应用部署](#2后端应用部署)
  - [版权说明](#版权说明)
  - [鸣谢](#鸣谢)

## 上手指南


###### 参考配置

PyTorch: 2.1.0 
Python: 3.10(ubuntu22.04) 
Cuda: 12.1
GPU: RTX 4090(24GB) * 1
CPU: 12 vCPU Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
内存: 90GB
硬盘: 50GB

#### **部署与启动**

###### 1.前端应用部署与启动
第一步：安装前端项目依赖

```sh
git pip install -r requirements.txt
```
第二步：启动前端项目进程


```sh
streamlit run start.py
```

###### 2.后端应用部署

第一步：部署3d-photo-inpainting[3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting/tree/master?tab=readme-ov-file)项目
```sh
git clone https://github.com/vt-vl-lab/3d-photo-inpainting.git
cd 3d-photo-inpainting
sh download.sh
pip install -r requirements.txt
cd ..
```
替换与添加项目文件
```sh
cp -r ./3d/* ./3d-photo-inpainting
```
第二步：部署[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui.git)项目
```sh
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
pip install -r requirements_versions.txt
pip install -r requirements.txt
cd ..
```
下载lora模型与基础模型
```sh
cd stable-diffusion-webui/models/Lora
wget https://huggingface.co/CreeperCatcher/AIstinct/resolve/main/FT_lora.safetensors?download=true
cd ../Stable-diffusion
wget https://civitai.com/api/download/models/50722
cd ../../..
```

安装[controlnet](https://github.com/Mikubill/sd-webui-controlnet)拓展,并下载controlnet模型
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
第三步：启动后端项目进程
启动3d-photo-inpainting 进程
```sh
python 3d-photo-inpainting/api.py
``` 
无界面启动stable-diffusion-webui 进程
```sh
python stable-diffusion-webui/launch.py --port 6006 --nowebui
```

## 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/shaojintian/Best_README_template/blob/master/LICENSE.txt)

## 鸣谢


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

