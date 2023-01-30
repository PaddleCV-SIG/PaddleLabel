# 实例分割手动标注

<!-- TOC -->

- [数据结构](#%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)
    - [掩膜格式](#%E6%8E%A9%E8%86%9C%E6%A0%BC%E5%BC%8F)
    - [多边形格式](#%E5%A4%9A%E8%BE%B9%E5%BD%A2%E6%A0%BC%E5%BC%8F)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
    - [多边形标注](#%E5%A4%9A%E8%BE%B9%E5%BD%A2%E6%A0%87%E6%B3%A8)
    - [掩膜标注](#%E6%8E%A9%E8%86%9C%E6%A0%87%E6%B3%A8)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

![image](https://user-images.githubusercontent.com/35907364/204429739-408e67c3-2748-434c-ba73-258d9602fe91.png)

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

PaddleLabel 将语义分割和实例分割视为两种项目类型，目前二者之间不支持转换。在语义分割项目中，每个像素将有一个分类，表示其为背景或前景中的某一类别。实例分割项目在逐像素分类的基础上给每个像素一个实例 id，即不仅区分像素所属类别，而且区分同一类别下像素属于哪个实例。

PaddleLabel 支持多种分割数据集格式，各种类型的数据集导入后都可以使用多边形和笔刷两种标注工具。数据集导出时

- 如果导出掩膜格式，多边形标注会被转换成掩模格式
- 如果导出多边形格式，会跳过所有掩膜格式标注

## 数据结构

### 掩膜格式

{: .label }
v0.1.0+

样例格式如下：

```shell
数据集路径
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
optic_disk - 128 0 0 // 对于伪彩色掩膜，需要按此结构提供每个类别的颜色。灰度掩膜的id默认为从0开始依次递增
```
<!-- TODO: 丰富 -->
### 多边形格式

{: .label }
v0.1.0+

样例格式如下：

```shell
数据集路径
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
<!-- TODO: 丰富 -->

## 数据标注

### 多边形标注

1. 点击右侧“添加标签”，填写信息并创建标签
2. 选择一个标签，点击左侧工具栏的“多边形”，在图像界面上点击需要标注的物体轮廓，形成多边形包围物体，实例分割可以反复选择同一标签标注不同的实例，需要修改多边形可以点击左侧工具栏的“编辑”进行修改
3. **标注完成一个实例后，点击右上角"确定轮廓"进行实例确认**
4. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
5. 下方进度展示可以查看标注进度

### 掩膜标注

1. 点击右侧“添加标签”，填写信息并创建标签
2. 选择一个标签，点击左侧工具栏的“笔刷”（鼠标悬浮可以修改笔刷大小），在图像界面上按住鼠标左键绘制需要标注的物体内部，实例分割可以反复选择同一标签标注不同的实例，，需要删除掩膜可以点击左侧工具栏的“橡皮擦”进行修改
3. **标注完成一个实例后，点击右上角"确定轮廓"进行实例确认**
4. 点击左右按钮切换图像，重复上述操作，直到所有数据标注完毕
5. 下方进度展示可以查看标注进度

<!-- _注意：① 在 PaddleLabel 中，右侧标签栏有标签和标注两种。在图像分割中，标签对应的是类别，而标注对应的是该类别的一个实例。实例分割每一个类别可以创建多个实例。② 多边形模式和掩膜模式不可同时使用，请在创建项目时确定使用某种格式。_ -->

## 下一步

您可以继续浏览[交互式分割使用方法](/doc/CN/ML/interactive_segmentation.md)了解如何使用 PaddleLabel-ML 提高语义分割标注效率。
