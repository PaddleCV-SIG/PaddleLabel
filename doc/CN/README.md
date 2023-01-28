中文 | [English](/doc/EN/)

<div align="center">

<p align="center">
  <img src="https://user-images.githubusercontent.com/35907364/182084617-ea94f744-3a34-4193-98fe-5d6869a118fc.png" align="middle" alt="LOGO" width = "500" />
</p>

<b> 飞桨智能标注，让标注快人一步 </b>

<p>
<img src="https://img.shields.io/badge/python-3.7+-blue.svg">
<img src="https://img.shields.io/badge/os-linux%2C%20windows%2C%20macos-blue.svg"/>
<a href="https://github.com/PaddleCV-SIG/doc/blob/develop/LICENSE"> <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/> </a>
<a href="https://pypi.org/project/paddlelabel/"> <img src="https://img.shields.io/pypi/v/paddlelabel?color=blue"/> </a>
<a href="https://paddlecv-sig.github.io/doc/"><img src="https://img.shields.io/github/stars/PaddleCV-SIG/PaddleLabel?color=blue" /> </a>
<!-- <a href="https://github.com/PaddleCV-SIG/doc/network/members"> <img src="https://img.shields.io/github/forks/PaddleCV-SIG/PaddleLabel?color=blue"/></a> -->
<a href="https://pypistats.org/packages/paddlelabel"><img src="https://img.shields.io/pypi/dm/paddlelabel?color=blue"/> </a>
<a href="https://pepy.tech/project/paddlelabel"><img src="https://static.pepy.tech/personalized-badge/paddlelabel?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20Downloads"/></a>
<a href="https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/build.yml"><img src="https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/build.yml/badge.svg"></a>
</p>
</div>

## 最新动态

- 【2023-01-17】 :fire: PaddleLabel 1.0 版本发布！

  - 【OCR】新增 OCR 项目标注能力，支持 [PP-OCRv3](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/PP-OCRv3_introduction.md) 模型预标注
  - 【导入/导出】新增 EISeg 格式导入，新增大量[自动化测试](https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/cypress.yml)，修复诸多导入导出 bug
  - 【文档】对[文档](https://paddlecv-sig.github.io/PaddleLabel/)进行重新梳理，内容简洁清晰并和软件一同打包发布，进一步降低上手难度

- 【2022-11-30】 :fire: PaddleLabel 0.5 版本发布！

  - 【界面】全面升级分类、检测及分割的前端标注界面体验，显著提升标注流畅度
  - 【分类】新增 PPLCNet 预训练模型，为分类功能提供预标注能力
  - 【检测】新增 PicoDet 预训练模型，为检测功能提供预标注能力
  - 【分割】(1)优化语义分割及实例分割关于实例的区分，实例分割通过'确认轮廓'来区分实例; (2)新增根据类别或根据实例选择颜色显示模式; (3)修复交互式分割 localStorage 超限问题

[更多动态](/doc/CN/release_notes.md)

## 简介

PaddleLabel 是基于飞桨 PaddlePaddle 各个套件功能提供的配套标注工具。目前支持对分类、检测、分割、OCR 四种常见的计算机视觉任务数据集进行标注和管理，除基础的手动标注功能外也支持深度学习辅助标注，可以有效地提升标注效率。您可以使用 PaddleLabel 快捷高效地标注自定义数据集，之后将其导出使用飞桨套件进行模型训练。

PaddleLabel 的代码分布于三个项目中，本项目包含 PaddleLabel 的 Web 后端实现。[PaddleLabel-Frontend](https://github.com/PaddleCV-SIG/PaddleLabel-Frontend) 是基于 React 和 Ant Design 构建的前端，[PaddleLabel-ML](https://github.com/PaddleCV-SIG/PaddleLabel-ML) 是基于飞桨实现的自动和交互式深度学习辅助标注后端。

![demo720](https://user-images.githubusercontent.com/71769312/185099439-3230cf80-798d-4a81-bcae-b88bcb714daa.gif)

## 特性

- **简单** 一行 `pip install` 安装，手动标注直观易操作，机器学习后端安装即用无需复杂配置，极易上手
- **高效** 支持交互式分割和多种预标注，显著提升标注效率和精度
- **灵活** 分类支持单分类和多分类标注，分割支持多边形、笔刷及交互式分割等多种工具，方便您根据场景灵活选择标注方式
- **全流程** 与飞桨其它套件紧密配合，帮助您高效完成数据标注、模型训练与导出等全流程操作

## 技术交流

- 如果您有任何使用问题、产品建议、功能需求, 可以[提交 Issues](https://github.com/PaddleCV-SIG/PaddleLabel/issues/new)与开发团队交流
- 欢迎您扫码加入 PaddleLabel 微信群和小伙伴们一起交流学习。如果二维码过期可以添加开发同学微信 linhandev 进群

<div align="center">
<img src="/doc/CN/assets/group_qr.png"  width = "200" />
</div>

## 使用教程

- [安装指南](/doc/CN/install.md)
- [快速开始](/doc/CN/quick_start.md)

### 进行标注

- [图像分类](/doc/CN/manual/classification.md)
- [目标检测](/doc/CN/manual/detection.md)
- [语义分割](/doc/CN/manual/semantic_segmentation.md)
- [实例分割](/doc/CN/manual/instance_segmentation.md)
- [OCR](/doc/CN/manual/ocr.md)

### 深度学习辅助标注

- [机器学习后端安装指南](/doc/CN/ML/install_ml.md)
- [自动预标注使用方法](/doc/CN/ML/auto_inference.md)
- [交互式分割使用方法](/doc/CN/ML/interactive_segmentation.md)

### 训练教程

- [使用 PaddleClas 进行训练](/doc/CN/training/PdLabel_PdClas.md)
- [使用 PaddleDet 进行训练](/doc/CN/training/PdLabel_PdDet.md)
- [使用 PaddleSeg 进行训练](/doc/CN/training/PdLabel_PdSeg.md)
- [使用 PaddleX 进行训练](/doc/CN/training/PdLabel_PdX.md)

### AI Studio 项目

- [花朵分类](https://aistudio.baidu.com/aistudio/projectdetail/4337003)
- [道路标志检测](https://aistudio.baidu.com/aistudio/projectdetail/4349280)
- [图像分割](https://aistudio.baidu.com/aistudio/projectdetail/4353528)
- [如何使用 PaddleX 进行训练](https://aistudio.baidu.com/aistudio/projectdetail/4383953)

## 社区贡献

### 贡献者

感谢下列开发者参与或协助 PaddleLabel 的开发、维护、测试等：[linhandev](https://github.com/linhandev)、[cheneyveron](https://github.com/cheneyveron)、[RotPublic](https://github.com/xiaoyixin-cmd)、[ztty8888](https://github.com/ztty8888)、[haoyuying](https://github.com/haoyuying)、[monkeycc](https://github.com/monkeycc)、[geoyee](https://github.com/geoyee)、[Youssef-Harby](https://github.com/Youssef-Harby)、[yzl19940819](https://github.com/yzl19940819)

### 参与开发

PaddleLabel项目是团队合作的成果，我们十分欢迎感兴趣的大佬加入项目的开发和维护。如果您对参与项目建设感兴趣，请通过微信交流群联系开发团队。有关后端实现的详细信息，请参阅[开发者指南](/doc/CN/developers_guide.md)。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- quote-->

## 学术引用

```
@misc{paddlelabel2022,
    title={PaddleLabel, an effective and flexible tool for data annotation},
    author={PaddlePaddle Authors},
    howpublished = {\url{https://github.com/PaddleCV-SIG/PaddleLabel}},
    year={2022}
}
```
