# 实例分割手动标注

<!-- TOC -->

- [数据结构](#%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)
        - [掩膜格式](#%E6%8E%A9%E8%86%9C%E6%A0%BC%E5%BC%8F)
        - [多边形格式](#%E5%A4%9A%E8%BE%B9%E5%BD%A2%E6%A0%BC%E5%BC%8F)
    - [新项目创建](#%E6%96%B0%E9%A1%B9%E7%9B%AE%E5%88%9B%E5%BB%BA)
    - [数据导入](#%E6%95%B0%E6%8D%AE%E5%AF%BC%E5%85%A5)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
    - [多边形标注](#%E5%A4%9A%E8%BE%B9%E5%BD%A2%E6%A0%87%E6%B3%A8)
    - [掩膜标注](#%E6%8E%A9%E8%86%9C%E6%A0%87%E6%B3%A8)
- [完成标注](#%E5%AE%8C%E6%88%90%E6%A0%87%E6%B3%A8)
    - [数据划分](#%E6%95%B0%E6%8D%AE%E5%88%92%E5%88%86)
    - [数据导出](#%E6%95%B0%E6%8D%AE%E5%AF%BC%E5%87%BA)
- [\*交互式分割标注](#%5C%E4%BA%A4%E4%BA%92%E5%BC%8F%E5%88%86%E5%89%B2%E6%A0%87%E6%B3%A8)

<!-- /TOC -->

![image](https://user-images.githubusercontent.com/35907364/204429739-408e67c3-2748-434c-ba73-258d9602fe91.png)

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

PaddleLabel 支持多边形和掩膜两种实例分割标注任务。

## 数据结构

#### 掩膜格式

新建掩膜格式标注任务时，填写待标注图片所在文件夹绝对路径即可，可以直接通过复制路径并粘贴得到。
标注完成后，导出示例格式如下：

```shell
Dataset Path
├── Annotations
│   ├── A0001.tif
│   ├── B0001.tif
│   ├── H0002.tif
│   └── ...
├── JPEGImages
│   ├── A0001.jpg
│   ├── B0001.png
│   ├── H0002.bmp
│   └── ...
├── labels.txt
├── test_list.txt
├── train_list.txt
└── val_list.txt

# labels.txt
background -
optic_disk - 128 0 0 // for pseudo color mask, color for each label must be specified
```

#### 多边形格式

新建多边形格式标注任务时，填写待标注图片所在文件夹绝对路径即可，可以直接通过复制路径并粘贴得到。
标注完成后，导出示例格式如下：

```shell
Dataset Path
├── image
│   ├── 0001.jpg
│   ├── 0002.jpg
│   ├── 0003.jpg
│   └── ...
├── train.json
├── val.json
└── test.json
```

COCO 文件的格式如下：

```text
{
    "info": info,
    "images": [image],
    "annotations": [annotation],
    "licenses": [license],
    "categories": [category],
}

image{
    "id": int,
    "width": int,
    "height": int,
    "file_name": str,
    "license": int,
    "flickr_url": str,
    "coco_url": str,
    "date_captured": datetime,
}

annotation{
    "id": int,
    "image_id": int,
    "category_id": int,
    "segmentation": RLE or [polygon],
    "area": float,
    "bbox": [x,y,width,height],
    "iscrowd": 0 or 1,
}

category{
 "id": int,
 "name": str,
 "supercategory": str,
 "color": str // this feature is specific to PP Label. It's not in the coco spec.
}
```

### 新项目创建

浏览器打开 PaddleLabel 后，可以通过创建项目下的“实例分割”卡片创建一个新的图像分割标注项目（如果已经创建，可以通过下方“我的项目”找到对应名称的项目，点击“标注”继续标注）。

项目创建选项卡有如下选项需要填写：

- 项目名称（必填）：填写该分类标注项目的项目名
- 数据地址（必填）：填写待标注图片所在文件夹绝对路径即可，可以直接通过复制路径并粘贴得到。
- 数据集描述（选填）：填写该分类标注项目的使用的数据集的描述文字
- 标注类型（必选）：选择该任务为多边形标注任务还是掩膜标注任务

### 数据导入

在创建项目时需要填写数据地址，该地址对应的是数据集的文件夹，为了使 PaddleLabel 能够正确的识别和处理数据集，请参考数据结构组织数据集，对于 txt 文件的详细组织方式，请参考[数据集文件结构说明](dataset_file_structure.html)整理待标注数据的文件结构。同时 PaddleLabel 提供了参考数据集，实例分割的参考数据集位于`~/.paddlelabel/sample/instance_seg`路径下，也可参考该数据集文件结构组织数据。

## 数据标注

完成后进入标注界面，PaddleLabel 的界面分为五个区域，上方为可以切换的标签页，下方为标注进度展示，左侧包含图像显示区域与工具栏，右侧为标签列表，用于添加不同的标签和标注。在分割任务的标注中，可以按以下步骤进行使用：

### 多边形标注

1. 点击右侧“添加标签”，填写信息并创建标签
1. 选择一个标签，点击左侧工具栏的“多边形”，在图像界面上点击需要标注的物体轮廓，形成多边形包围物体，实例分割可以反复选择同一标签标注不同的实例，需要修改多边形可以点击左侧工具栏的“编辑”进行修改
1. **标注完成一个实例后，点击右上角"确定轮廓"进行实例确认**
1. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
1. 下方进度展示可以查看标注进度

### 掩膜标注

1. 点击右侧“添加标签”，填写信息并创建标签
1. 选择一个标签，点击左侧工具栏的“笔刷”（鼠标悬浮可以修改笔刷大小），在图像界面上按住鼠标左键绘制需要标注的物体内部，实例分割可以反复选择同一标签标注不同的实例，，需要删除掩膜可以点击左侧工具栏的“橡皮擦”进行修改
1. **标注完成一个实例后，点击右上角"确定轮廓"进行实例确认**
1. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
1. 下方进度展示可以查看标注进度

_注意：① 在 PaddleLabel 中，右侧标签栏有标签和标注两种。在图像分割中，标签对应的是类别，而标注对应的是该类别的一个实例。实例分割每一个类别可以创建多个实例。② 多边形模式和掩膜模式不可同时使用，请在创建项目时确定使用某种格式。_

## 完成标注

完成数据标注后，PaddleLabel 提供了方便的数据划分功能，以便与 Paddle 其他工具套件（如 PaddleSeg 和 PaddleDetection）进行快速衔接。点击右侧工具栏的“项目总览”按钮，来到该项目的总览界面，这里可以看到数据以及标注状态。通过上方的快捷按钮可以进行指定操作。

### 数据划分

点击**划分数据集**按钮弹出划分比例的设置，分别填入对应训练集、验证集和测试集的占比，点击确定即可完成数据集的划分。

### 数据导出

点击**导出数据集**，输入需要导出到的文件夹路径，点击确认，即可导出标注完成的数据到指定路径。

## \*交互式分割标注

PaddleLabel 带有基于 PaddlePaddle 的机器学习标注功能，可以通过加载模型实现交互式数据标注，使用方法参考[交互式分割标注](interactive_segmentation.html)。
