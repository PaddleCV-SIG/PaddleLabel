简体中文 | [English](README_EN.md)
<div align="center">

<p align="center">
  <img src="https://user-images.githubusercontent.com/35907364/182084617-ea94f744-3a34-4193-98fe-5d6869a118fc.png" align="middle" alt="LOGO" width = "500" />
</p>

**An Effective and Flexible Tool for Data Annotation based on [PaddlePaddle](https://github.com/paddlepaddle/paddle).**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/) ![PyPI](https://img.shields.io/pypi/v/paddlelabel?color=blue) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE) [![Start](https://img.shields.io/github/stars/PaddleCV-SIG/PaddleLabel?color=orange)]() [![Fork](https://img.shields.io/github/forks/PaddleCV-SIG/PaddleLabel?color=orange)]() ![PyPI - Downloads](https://img.shields.io/pypi/dm/paddlelabel?color=orange) [![OS](https://img.shields.io/badge/os-linux%2C%20windows%2C%20macos-green.svg)]() 
</div>


## 最新动态

* 【2020-08-01】 :fire: PaddleLabel 0.1版本发布！
    * 【分类】支持单分类与多分类标注及标签的导入导出。简单灵活实现自定义数据集分类标注任务并迁移到[PaddleClas](https://github.com/PaddlePaddle/PaddleClas)进行训练。
    * 【检测】支持检测框标注及标签的导入导出。快速上手生成自己的检测数据集并应用到到[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)。
    * 【分割】支持多边形、笔刷及交互式等多种标注方式，支持标注语义分割与实例分割等不同场景。多种分割标注方式可灵活选择，方便将导出数据应用在[PaddleSeg](https://github.com/PaddlePaddle/PaddleSeg)获取个性化定制模型。


## 简介

PaddleLabel是基于飞桨PaddlePaddle各个套件的特性提供的配套标注工具。它涵盖分类、检测、分割三种常见的计算机视觉任务的标注能力，具有手动标注和交互式标注相结合的能力。用户可以使用PaddleLabel方便快捷的标注自定义数据集并将导出数据用于飞桨提供的其他套件的训练预测流程中。
整个PaddleLabel包括三部分，本项目包含PaddleLabel的后端实现。 [PaddleLabel-Frontend](https://github.com/PaddleCV-SIG/PP-Label-Frontend)是基于React和Ant Design构建的PaddleLabel前端，[PaddleLabel-ML](https://github.com/PaddleCV-SIG/PaddleLabel-ML)包含基于PaddlePaddle的自动和交互式标注的机器学习后端。

![demo](https://user-images.githubusercontent.com/71769312/181277273-0c1d6189-4a84-44c7-a0ae-f9816dcc32ae.png)

## 特性


* **简单** 手动标注能力直观易操作，方便用户快速上手。
* **高效** 支持交互式分割功能，分割精度及效率提升显著。
* **灵活** 分类支持单分类和多分类的标注，分割支持多边形、笔刷及交互式分割等多种功能，方便用户根据场景需求切换标注方式。
* **全流程** 与其他飞桨套件密切配合，方便用户完成数据标注、模型训练、模型导出等全流程操作。


## 技术交流

* 如果大家有使用问题、产品建议、功能需求, 可以通过[GitHub Issues](https://github.com/PaddlePaddle/PaddleSeg/issues)提issues。
* 欢迎大家扫码加入PaddleLabel微信群，和小伙伴们一起交流学习。

<div align="center">
<img src="https://user-images.githubusercontent.com/48433081/163670184-43cfb3ae-2047-4ba3-8dae-6c02090dd177.png"  width = "200" />  
</div>

## 使用教程

**文档**

* [安装说明](doc/install.md)
* [分类标注](doc/classification.md)
* [检测标注](doc/detection.md)
* [分割标注](doc/segmentation.md)

**教程**

* [快速体验](doc/quick_experience.md)
* [如何用PaddleClas进行训练](doc/PPLabel_PaddleClas.md)
* [如何用PaddleDet进行训练](doc/PPLabel_PaddleDet.md)
* [如何使用PaddleSeg进行训练](doc/PPLabel_PaddleSeg.md)
* [如何使用PaddleX进行训练](doc/PPLabel_PaddleX.md)

## 社区贡献

### 贡献者

感谢下列开发者参与或协助PaddleLabel的开发、维护、测试等：[linhandev](https://github.com/linhandev)、[cheneyveron](https://github.com/cheneyveron)、[Youssef-Harby](https://github.com/Youssef-Harby)、[geoyee](https://github.com/geoyee)、[yzl19940819](https://github.com/yzl19940819)、[haoyuying](https://github.com/haoyuying)

### 如何参与开源项目

如果你有任何好的想法或发现了任何问题，欢迎参与到我们的开发和维护中。有关后端实现的详细信息，请参阅[开发者指南](doc/developers_guide.md)。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- quote-->

## 学术引用

```
@misc{paddlelabel2022,
    title={PaddleLabel, An effective and flexible tool for data annotation},
    author={PaddlePaddle Authors},
    howpublished = {\url{https://github.com/PaddleCV-SIG/PaddleLabel}},
    year={2022}
}
```



