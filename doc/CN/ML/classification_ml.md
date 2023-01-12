# 图像分类自动标注

<!-- TOC -->

- [前置步骤](#%E5%89%8D%E7%BD%AE%E6%AD%A5%E9%AA%A4)
- [进行自动预标注设置](#%E8%BF%9B%E8%A1%8C%E8%87%AA%E5%8A%A8%E9%A2%84%E6%A0%87%E6%B3%A8%E8%AE%BE%E7%BD%AE)
- [使用预标注](#%E4%BD%BF%E7%94%A8%E9%A2%84%E6%A0%87%E6%B3%A8)

<!-- /TOC -->

PaddleLabel-ML 基于[PaddleClas 套件](https://github.com/PaddlePaddle/PaddleClas)中的预训练模型提供图像分类自动标注能力，您只需在“自动推理设置”中进行简单配置，即可启用自动预标注功能。

![](https://user-images.githubusercontent.com/35907364/204250596-061d8193-b011-44b4-9b25-83efc77fef04.gif)

<!-- <div align="center">

<p align="center">
  <img src="https://user-images.githubusercontent.com/35907364/204250596-061d8193-b011-44b4-9b25-83efc77fef04.gif" align="middle" alt="LOGO" width = "500" />
</p>
</div> -->

## 前置步骤

1. 在使用辅助标注功能前请先按照 [机器学习后端安装](/doc/CN/ML/install_ml.md) 文档中介绍的步骤安装并启动 PaddleLabel-ML 后端

2. 启动 PaddleLabel 和 PaddleLabel-ML

   打开两个命令行终端，第一个输入 `paddlelabel` 并回车，第二个输入 `paddlelabel-ml` 并回车，分别启动项目的 web 部分和辅助标注部分
   ![](/doc/CN/assets/start_two.png)

3. 新建分类项目

   可以参考快速体验文档[创建分类样例项目](/doc/CN/quick_start.md#创建样例项目)或[导入一个分类数据集](/doc/CN/quick_start.md#导入数据集)

## 进行自动预标注设置

1. 点击“项目总览”页面上方“自动推理设置”按钮进入设置页面
   ![](/doc/CN/assets/to_auto_inference.png)
2. 填写机器学习后端网址。
   默认网址为`http://127.0.0.1:1234`。这一网址可以通过观察 paddlelabel-ml 启动时命令行输出确定
   ![](/doc/CN/assets/ml_backend_url.png)
3. 点击模型选择下拉菜单选择一个模型。目前支持 [PPLCNetV2](https://github.com/PaddlePaddle/PaddleClas/blob/release/2.5/docs/zh_CN/models/ImageNet1k/PP-LCNetV2.md)
4. 选择是否使用预标注标签

- 此处如果选择是
  - 预训练模型的推理结果类别将被原样添加到项目中
  - 如果模型返回了一个项目中尚不存在的类别，会自动向项目中添加该类别标签。
    ![](/doc/CN/assets/accept_model_label.png)
- 此处如果选择否，即不直接使用预标注标签
  - 您需要提供预训练模型标签与项目中标签的对应关系。比如指定预训练模型的标签“咖啡杯”对应项目中的标签“杯子”，之后如果模型对一张图片模型推理结果为“咖啡杯”，则会向该图片添加“杯子”类别。
  - 多个模型标签可以对应同一个项目中的标签，比如下图中“咖啡壶”和“咖啡杯”类别的推理结果都会向项目中添加“咖啡用具”标签。
  - 一个模型标签只能对应到一个项目中的标签。
  - 注意在这个模式下，辅助标注流程会忽略所有未提供对应关系的模型标签。
    ![](/doc/CN/assets/dont_accept_model_label.png)

5. 完成设置后，点击`确定`保存，跳转回项目总览页面

## 使用预标注

- 预标注模型会在您进入标注页面时自动加载。
- 每当您翻到一张之前没有进行过预标注的图片时都会自动进行推理。您也可以点击右侧工具栏的“自动推理”按钮手动触发一次推理。
- 您可以通过调节右侧工具栏中的“推理阈值”控制预标注结果的数量
