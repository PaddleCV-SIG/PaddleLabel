# 语义分割手动标注

<!-- TOC -->

- [数据结构](#%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)
    - [掩膜格式](#%E6%8E%A9%E8%86%9C%E6%A0%BC%E5%BC%8F)
    - [COCO 格式](#coco-%E6%A0%BC%E5%BC%8F)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
    - [多边形标注](#%E5%A4%9A%E8%BE%B9%E5%BD%A2%E6%A0%87%E6%B3%A8)
    - [掩膜标注](#%E6%8E%A9%E8%86%9C%E6%A0%87%E6%B3%A8)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

![image](https://user-images.githubusercontent.com/29757093/182841499-85b9df06-f793-4831-b3f5-54c013ce531c.png)

PaddleLabel 支持多种语义分割数据集格式，各种类型的数据集导入后都可以使用多边形和笔刷两种标注工具。数据集导出时间，如果导出掩膜格式，多边形标注会被转换成掩模格式。但如果导出多边形格式，会跳过所有掩膜格式标注。

## 数据结构

### 掩膜格式

掩膜格式数据集的待标注图片和掩膜一般都是图片文件，所以二者需要通过所在文件夹进行区分。**创建此类型标注项目时，请将待标注图片放在`JPEGImages`文件夹中，将已有标签放在`Annotations`文件夹中，数据集路径请填写二者的上层目录（下方示例中的`数据集路径`）。**

此类型项目可以导入 EISeg 保存的灰度和伪彩色掩膜。不过 EISeg 保存伪彩色掩膜时文件名格式为 `图片名_pseudo.png` ，导入前需要将伪彩色掩膜重命名为 `图片名.png`。

示例格式如下：

```shell
数据集路径
├── Annotations
│   ├── A0001.png
│   ├── B0001.png
│   ├── H0002.png
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

### COCO 格式

样例数据集格式如下

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

## 数据标注

完成后进入标注界面，PaddleLabel 的界面分为五个区域，上方为可以切换的标签页，下方为标注进度展示，左侧包含图像显示区域与工具栏，右侧为标签列表，用于添加不同的标签和标注。在分割任务的标注中，可以按以下步骤进行使用：

### 多边形标注

1. 点击右侧“添加标签”，填写信息并创建标签
1. 选择一个标签，点击左侧工具栏的“多边形”，在图像界面上点击需要标注的物体轮廓，形成多边形包围物体，语义分割每一个标签只能标注一个对应的实例，需要修改多边形可以点击左侧工具栏的“编辑”进行修改
1. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
1. 下方进度展示可以查看标注进度

### 掩膜标注

1. 点击右侧“添加标签”，填写信息并创建标签
1. 选择一个标签，点击左侧工具栏的“笔刷”（鼠标悬浮可以修改笔刷大小），在图像界面上按住鼠标左键绘制需要标注的物体内部，语义分割每一个标签只能标注一个对应的实例，需要删除掩膜可以点击左侧工具栏的“橡皮擦”进行修改
1. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
1. 下方进度展示可以查看标注进度

_注意：① 在 PaddleLabel 中，右侧标签栏有标签和标注两种。在图像分割中，标签对应的是类别，而标注对应的是该类别的一个实例。语义分割每一个类别只能创建一个实例。② 多边形模式和掩膜模式不可同时使用，请在创建项目时确定使用某种格式。_

## 下一步

您可以继续浏览[交互式分割使用方法](/PaddleLabel/CN/ML/interactive_segmentation.md)了解如何使用 PaddleLabel-ML 提高标注效率。
