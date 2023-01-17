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

PaddleLabel 将语义分割和实例分割视为为两种项目类型，目前二者之间不支持转换。在语义分割项目中，每个像素将有一个分类，表示其为背景或前景中的某一类别。实例分割项目在逐像素分类的基础上给每个像素一个实例 id，即不仅区分像素所属类别，而且区分同一类别下像素属于哪个实例。

PaddleLabel 支持多种分割数据集格式，各种类型的数据集导入后都可以使用多边形和笔刷两种标注工具。数据集导出时

- 如果导出掩膜格式，多边形标注会被转换成掩模格式
- 如果导出多边形格式，会跳过所有掩膜格式标注

## 数据结构

### 掩膜格式
{: .label }
v0.1.0+

掩膜格式数据集的待标注图片和掩膜一般都是图片文件，所以二者需要通过所在文件夹进行区分。**创建此类型标注项目时，请将待标注图片放在`JPEGImages`文件夹中，将已有标签放在`Annotations`文件夹中，数据集路径请填写二者的上层目录（下方示例中的`数据集路径`）。**

{: .note}
此类型项目可以导入 EISeg 保存的灰度和伪彩色掩膜。不过 EISeg 保存伪彩色掩膜时文件名格式为 `图片名_pseudo.png` ，导入前需要将伪彩色掩膜重命名为 `图片名.png`。

样例格式如下：

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
background
optic_disk - 128 0 0 // 对于伪彩色掩膜，需要按此结构提供每个类别的颜色
```

### COCO 格式

{: .label }
v0.1.0+

样例格式如下：

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

语义分割项目支持多边形和笔刷/橡皮掩膜标注两种标画工具。

### 多边形标注

1. 在右侧“类别列表”中点击选中一个类别，在左侧工具栏中点击“多边形”按钮激活该工具
2. 在图像中沿待标注物体的边缘点击，使用多边形包围该物体。完成后点击鼠标右键结束对该物体的标注，标注结果将自动保存。这一过程可以重复多次，通常一个多边形只框选一个物体
3. 如需要修改多边形顶点可以在左侧工具栏中点击“编辑”，之后拖动顶点位置
4. 完成一张图片标注后点击画布左右 < > 按钮切换图片

### 掩膜标注

1. 在右侧“类别列表”中点击选中一个类别，在左侧工具栏中点击“笔刷”按钮激活该工具
2. 鼠标悬浮在笔刷工具上方时，可以弹出的悬浮框中调整笔刷大小
3. 在图像中使用笔刷标画所有属于该类别的像素。如果标画的过多可以使用橡皮擦工具擦除。每笔标注会自动保存
4. 完成一张图片标注后点击画布左右 < > 按钮切换图片

<!-- _注意：① 在 PaddleLabel 中，右侧标签栏有标签和标注两种。在图像分割中，标签对应的是类别，而标注对应的是该类别的一个实例。语义分割每一个类别只能创建一个实例。② 多边形模式和掩膜模式不可同时使用，请在创建项目时确定使用某种格式。_ -->

## 下一步

您可以继续浏览[交互式分割使用方法](/PaddleLabel/CN/ML/interactive_segmentation.md)了解如何使用 PaddleLabel-ML 提高语义分割标注效率。
