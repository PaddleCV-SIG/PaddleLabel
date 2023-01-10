<!-- TOC -->

- [快速体验](#%E5%BF%AB%E9%80%9F%E4%BD%93%E9%AA%8C)
    - [创建样例项目](#%E5%88%9B%E5%BB%BA%E6%A0%B7%E4%BE%8B%E9%A1%B9%E7%9B%AE)
    - [项目总览](#%E9%A1%B9%E7%9B%AE%E6%80%BB%E8%A7%88)
    - [进行标注](#%E8%BF%9B%E8%A1%8C%E6%A0%87%E6%B3%A8)
    - [数据集划分](#%E6%95%B0%E6%8D%AE%E9%9B%86%E5%88%92%E5%88%86)
    - [导出数据集](#%E5%AF%BC%E5%87%BA%E6%95%B0%E6%8D%AE%E9%9B%86)
    - [导入数据集](#%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE%E9%9B%86)

<!-- /TOC -->

# 快速体验

本文档将带领您快速了解 PaddleLabel 的主要功能及使用流程。

## 创建样例项目

为了方便您快速体验 PaddleLabel 功能，我们内置了一些样例项目。当 PaddleLabel 网页打开后，点击首页左上角“项目样例”按钮，即可进入样例选择界面。

![image](/doc/CN/assets/sample_button.png)

样例界面提供了分类、检测、实例分割、语义分割和 OCR 五种类型的样例项目，点击卡片即可进入相应样例项目的总览。

![image](/doc/CN/assets/sample_page.png)

## 项目总览

项目总览页面如下

![image](/doc/CN/assets/project_overview.png)

总览页面上方提供了一些数据集管理功能

<details> <summary markdown="span">点此查看详细介绍</summary>

- 去标注：跳转到标注页面
- 项目设置：修改项目名称和描述
  ![1](https://user-images.githubusercontent.com/29757093/206072481-318551ce-69fb-40bb-9f2a-076d076f72c1.png)
- 划分数据集：对数据集进行训练/验证/测试子集的划分
  ![1](https://user-images.githubusercontent.com/29757093/206072638-187a0c1a-d6c6-4389-b5c7-0faa08cd646e.png)
- 导入额外数据：向当前数据集中导入更多数据
  ![1](https://user-images.githubusercontent.com/29757093/206072742-34c19214-463b-455e-bc46-25de0bf81096.png)
- 导出数据集：将数据集中的图片和标注信息导出
  ![1](https://user-images.githubusercontent.com/29757093/206072833-18ebcfe7-e67f-4ff6-ae0a-91de56ba647a.png)
- 自动推理设置：配置 PaddleLabel-ML 选项，使用自动推理模型在项目中进行预标注
![image](/doc/CN/assets/auto_inference.png)
</details>

## 进行标注

在项目总览页面中，点击页面上方或任务右侧的去标注按钮可以跳转到标注页面。

![image](/doc/CN/assets/project_overview_to_label.png)

标注页面的介绍以实例分割为例，页面和功能区如下

![image](/doc/CN/assets/label_page.png)

<details> <summary markdown="span">点此查看各功能区详细介绍</summary>

- **标注工具**区域可以选择多边形，笔刷，橡皮擦，移动/缩放图片等工具。大多数标注操作支持撤销/重做。每步标注操作完成后都会自动向后端进行保存。最下方清空标注工具可以清除当前图片中的所有标注。
- **上一张/下一张**按钮在画布两侧，点击可以切换图片
- **标注进度**在页面最下方，显示标注进度和当前图片编号
- **展示/推理设置**工具栏主要包括对画布中标注元素展示的设置和基于深度学习的自动/交互式模型推理设置。顶部的项目总览按钮可以返回项目总览页面。
- **标签/标注列表**区域展示当前项目的标签（标注的类别，如分类项目中的类别）和当前图片中的标注（如实例分割中每个实例都是一条标注）。不同项目这一区域的展示的元素有所不同，如分类项目中没有标注列表，OCR 项目中这一区域没有标签列表，标注列表中添加了文字内容编辑功能。

</details>

<!-- TODO: 标注过程-->

## 数据集划分
<!-- TODO: 数据集划分 -->

## 导出数据集

完成标注后您可以将数据集导出用于模型训练。导出步骤如下：

1. 首先点击标注页面右侧工具栏顶部“项目总览”按钮跳转到总览页面
   ![image](/doc/CN/assets/to_overview.png)

2. 点击总览页面顶部“导出数据集”按钮
   ![image](/doc/CN/assets/export.png)

3. 填写导出路径（需要是绝对路径），根据需要选择导出格式，点击导出
   ![image](/doc/CN/assets/export_detail.png)

## 导入数据集

样例数据集主要是为了展示 PaddleLabel 功能，大多数情况下需要导入自己的数据集进行标注和管理。导入的主要流程如下

1. 访问项目首页，PaddleLabel默认的首页地址是[http://localhost:17995](http://localhost:17995)。或者您可以在任意页面点击左上角点击飞桨Logo返回首页。
![image](/doc/CN/assets/to_home.png)
2. 点击创建项目区域的任一卡片，创建对应类型的项目。这里以分类项目为例，导入刚才导出的项目
![image](/doc/CN/assets/create.png)
3. 在创建项目页面填写项目名称，注意不能和其他项目重复。
4. 选择一个跟待导入数据集最接近的项目类型/数据集格式。右侧区域会显示示例数据集文件排布作为参考。
![image](/doc/CN/assets/sample_structure.png)
5. 填写“数据集路径”，该路径是到一个文件夹的绝对路径，为了避免导入过程中遇到问题，请将文件夹中的文件尽可能按右侧示例进行排布。点击右侧示例中的文件可以查看文件内容
6. 点击创建，成功后会跳转到项目总览页面。
