# 自动预标注使用方法

<!-- TOC -->

- [模型列表](#%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8)
- [前置步骤](#%E5%89%8D%E7%BD%AE%E6%AD%A5%E9%AA%A4)
- [进行设置](#%E8%BF%9B%E8%A1%8C%E8%AE%BE%E7%BD%AE)
- [使用自动预标注](#%E4%BD%BF%E7%94%A8%E8%87%AA%E5%8A%A8%E9%A2%84%E6%A0%87%E6%B3%A8)

<!-- /TOC -->

PaddleLabel 基于 [PaddleClas](https://github.com/PaddlePaddle/PaddleClas)，[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection) 和 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 中的预训练模型为分类，检测和 OCR 项目提供自动预标注能力。您只需在“自动推理设置”中进行简单配置即可启用这一功能。本文档以分类项目为例介绍自动预标注功能的配置和使用方法，检测和 OCR 项目中的使用流程基本完全相同。

![](https://user-images.githubusercontent.com/35907364/204250596-061d8193-b011-44b4-9b25-83efc77fef04.gif)

<!-- <div align="center">

<p align="center">
  <img src="https://user-images.githubusercontent.com/35907364/204250596-061d8193-b011-44b4-9b25-83efc77fef04.gif" align="middle" alt="LOGO" width = "500" />
</p>
</div> -->

## 模型列表

PaddleLabel 目前支持的模型和使用各模型所需的 PaddleLabel-ML 版本如下

- 分类
  - [PP-LCNetV2](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/docs/zh_CN/models/ImageNet1k/PP-LCNetV2.md) v0.5.0+ {: .label }
- 检测
  - [PP-PicoDet](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.5/configs/picodet) v0.5.0+ {: .label }
- OCR
  - [PP-OCRv3](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/PP-OCRv3_introduction.md) v0.5.0+ {: .label }

## 前置步骤

1. 在使用自动预标注功能前请先参考 [此文档](/doc/CN/ML/install_ml.md) 安装 PaddleLabel-ML 辅助标注后端

2. 启动 PaddleLabel 和 PaddleLabel-ML

   打开两个命令行终端，第一个输入 `paddlelabel` 并回车，第二个输入 `paddlelabel-ml` 并回车，分别启动项目的 web 部分和辅助标注部分
   ![](/doc/CN/assets/start_two.png)

3. 创建项目

   您可以参考快速体验文档[创建内置样例项目](/doc/CN/quick_start.md#创建样例项目)或[导入一个数据集](/doc/CN/quick_start.md#导入数据集)

## 进行设置

1. 点击“项目总览”页面上方“自动推理设置”按钮进入设置页面
   ![](/doc/CN/assets/to_auto_inference.png)
2. 填写机器学习后端网址

   默认网址为`http://127.0.0.1:1234`。这一网址可以通过观察 paddlelabel-ml 启动时的命令行输出确定
   ![](/doc/CN/assets/ml_backend_url.png)

3. 点击模型选择下拉菜单选择一个模型
4. 选择是否使用预标注标签

- 此处如选择`是`
  - 预标注模型的推理结果类别将被原样添加到图像标注中
  - 如果模型推理出了一个项目中没有的类别，会自动向项目中添加该类别标签
    ![](/doc/CN/assets/accept_model_label.png)
- 此处如选择`否`，则不直接使用预标注模型标签
  - 您需要提供预标注模型标签与项目中标签的对应关系。比如指定预标注模型的标签“咖啡杯”对应项目中的标签“杯子”，标注时如果模型对一张图片推理结果为“咖啡杯”，则会向该图片添加“杯子”类别
  - 多个预标注模型的标签可以对应同一个项目中的标签，比如使用下图中的配置，“咖啡壶”和“咖啡杯”类别的推理结果都会向图片中添加“咖啡用具”标签
  - 一个模型标签只能对应到一个项目中的标签
  - 注意在这个模式下，辅助标注流程会忽略所有未提供对应关系的预标注模型标签
    ![](/doc/CN/assets/dont_accept_model_label.png)

5. 完成设置后，点击`确定`保存，跳转回项目总览页面

## 使用自动预标注

- 预标注模型会在您进入标注页面时自动加载
- 当您翻到一张之前没有进行过预标注的图片时会自动触发推理。您也可以点击右侧工具栏中的“自动推理”按钮手动触发一次推理
- 您可以通过调节右侧工具栏中的“推理阈值”控制预标注结果的数量
