# 快速体验

## 创建样例项目

为了方便您快速体验 PaddleLabel 功能，我们内置了一些示例项目。当 PaddleLabel 网页打开后，点击首页左上角“项目样例”按钮，即可进入样例选择界面。

![image](/doc/CN/assets/sample_button.png)

样例界面提供了分类、检测、实例分割、语义分割和 OCR 五种类型的样例项目，点击卡片即可进入相应样例项目的总览。

![image](/doc/CN/assets/sample_page.png)

## 项目总览

项目总览页面如下

![image](/doc/CN/assets/project_overview.png)

总览页面上方的按钮提供了一些数据集管理功能

<details> <summary markdown="span">点此查看功能详细介绍</summary>

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

- **标注工具**区域可以选择多边形，笔刷，橡皮擦，移动/缩放图片等工具。大多数标注操作支持撤销/重做。每步标注操作完成后都会自动向后端进行保存。最下方清空标注工具可以清除当前图片中的所有标注。
- **上一张/下一张**按钮在画布两侧，点击可以切换图片
- **标注进度**在页面最下方，显示标注进度和当前图片编号
- **展示/推理设置**工具栏主要包括对画布中标注元素展示的设置和基于深度学习的自动/交互式模型推理设置。顶部的项目总览按钮可以返回项目总览页面。
- **标签/标注列表**区域展示当前项目的标签（标注的类别，如分类项目中的类别）和当前图片中的标注（如实例分割中每个实例都是一条标注）。不同项目这一区域的展示的元素有所不同，如分类项目中没有标注列表，OCR 项目中这一区域没有标签列表，标注列表中添加了文字内容编辑功能。
