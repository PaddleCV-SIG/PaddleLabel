# 目标检测手动标注

<!-- TOC -->

- [数据集格式](#%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
    - [PASCAL VOC](#pascal-voc)
    - [COCO](#coco)
    - [YOLO](#yolo)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

![image](https://user-images.githubusercontent.com/29757093/182841361-eb53e726-fa98-4e02-88ba-30172efac8eb.png)

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

## 数据集格式

PaddleLabel 目前支持 **PASCAL VOC**，**COCO** 和 **YOLO** 三种目标检测数据集格式。

### PASCAL VOC

v0.1.0+ {: .label }

PASCAL VOC 格式的标注信息存在 xml 格式文件中，每张图片对应一个 xml 文件。您可以通过列表文件，相同文件名或 xml 文件内容三种方式将图片和标注 xml 对应起来，规则细节将在后面描述。

样例格式如下：

```shell
数据集路径
├── Annotations
│   ├── 0001.xml
│   ├── 0002.xml
│   ├── 0003.xml
│   └── ...
├── JPEGImages
│   ├── 0001.jpg
│   ├── 0002.jpg
│   ├── 0003.jpg
│   └── ...
├── labels.txt # 可选
├── test_list.txt # 可选
├── train_list.txt # 可选
└── val_list.txt # 可选
```

PaddleLabel 目前导入/导出用到的 VOC 格式 xml 文件内容如下。

此处没有列出的节点在导入时不会被考虑，导出时不会被导出。{: .note}

```text
<annotation>
 <folder>JPEGImages</folder> # 可选：如果不存在folder节点，将使用默认值 JPEGImages
 <filename></filename> # 如果不存在filename节点，将使用默认值空字符串 ""
 <size> # 目前导入过程中读取开图像确认图像大小，以下三个值不会被考虑
  <width></width>
  <height></height>
  <depth></depth>
 </size>
 <object>
  <name></name>
  <bndbox>
   <xmin></xmin>
   <ymin></ymin>
   <xmax></xmax>
   <ymax></ymax>
  </bndbox>
 </object>
</annotation>
```

train/val/test_list.txt 中每行是一组图像和标注 xml 的对应关系，路径需为相对`数据集路径`的相对路径，以空格为分隔符。

示例格式如下：

```txt

JPEGImages/0001.jpg Annotations/0001.xml
JPEGImages/0002.jpg Annotations/0002.xml
...

```

新建 VOC 格式检测项目时，首先会扫描您填写的`数据集路径`下所有的图片和以 .xml 结尾的标注文件（不考虑大小写）。之后 PaddleLabel 将顺序使用一下三个规则将图片和标注进行匹配。

1. 如果`数据集路径`下存在 train/val/test_list.txt 列表文件，将首先按照列表文件内容确定对应关系
2. 无法通过列表文件内容确定对应的 .xml 文件，将对应到`数据集路径`下文件名相同的图片。如 JPEGImages/0001.xml 对应到 Annotations/0001.jpg（以.分割去除拓展名后二者都是 0001）
3. 依然无法确定对应关系的 .xml 文件将与位于`/数据集路径/folder/filename`的图片对应。上述路径中的`folder`和`filename`从该 xml 文件中解析
   - `folder`：
     - 如果 xml 中没有`folder`节点，将使用默认值 JPEGImages
     - 如果`folder`节点存在，但内容为空，将认为图像文件直接位于`/数据集路径/filename`。
   - `filename`：xml 中 `filename` 节点的内容，如 xml 中不存在`filename`节点将使用默认值空字符串

如果导入图像后发现有 xml 标注信息的图像中没有标注，可以切换到 PaddleLabel 运行的命令行查看是否有报错。

### COCO

v0.1.0+ {: .label }

COCO 格式将整个数据集的所有标注信息存在一个（或少数几个）`json`文件中。这里列出了 COCO 和检测相关的部分格式，更多细节请访问[COCO 官网](https://cocodataset.org/#format-data)查看。

下文没有列出的项不会在导入时被保存到数据库中和最终导出，比如图像的 date_captured 属性。{: .note}

所有 COCO 格式的项目都不支持在导入时以 train/val/test_list.txt 指定数据集划分和使用 labels.txt 文件创建分类 {: .note}

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
    "width": int, // 目前导入时会读取图片获取图片大小
    "height": int, // 不会使用coco json中记录的长宽
    "file_name": str,
}

annotation{
    "id": int,
    "image_id": int,
    "category_id": int,
    "area": float,
    "bbox": [x, y, width, height],
}

category{
 "id": int,
 "name": str,
 "supercategory": str,
 "color": str // PaddleLabel 加入的功能，COCO官方定义中没有这一项。标签颜色会被导出，导入时如果这项存在会给这一类别赋color指定的颜色
}
```

新建 COCO 类型项目时，填写的`数据集路径`下所有图片都将被导入，标签和图像对应规则为：image['file_name']中最后的文件名和盘上图片的文件名相同（大小写敏感）。

这一设计是为了让对应逻辑尽可能简单并保持一定的跨平台兼容性。推荐将所有图片放在同一个文件夹下以避免图片重名，导致 coco 标注信息中的一条图片记录对应到盘上的多张图片。一些标注工具导出的 coco 标注记录中，image['file_name']项可能是完整的文件路径或相对数据集根目录的路径，这种情况下我们用'/'和'\\'分割这个路径，取分割结果最后一段为文件名。因此请避免在文件名中使用'/'和'\\'。

### YOLO

v0.5.0+ {: .label }

YOLO 格式每张图像对应一个 txt 格式的标注信息文件，二者文件名除拓展名部分相同。

样例格式如下：

```shell
数据集路径
├── Annotations
│   ├── 0001.txt
│   ├── 0002.txt
│   ├── 0003.txt
│   └── ...
├── JPEGImages
│   ├── 0001.jpg
│   ├── 0002.jpg
│   ├── 0003.jpg
│   └── ...
├── labels.txt
├── test_list.txt
├── train_list.txt
└── val_list.txt
```

txt 文件内容样例如下：

```txt
0 0.4 0.5 0.7 0.8
```

其格式为：`标签id bb中心宽方向位置/图像宽 bb中心长方向位置/图像长 bb宽/图像宽 bb长/图像长`。其中`标签id` 从 0 开始。导入时没有标注的图像可以不提供标注文件，或提供空文件。PaddleLabel 对没有标注的图像不会导出空 YOLO 标注文件

<!-- TODO: 根据三个列表对应 -->

注意 YOLO 格式的图像和标签完全通过文件名对应，如果有两张图片文件名只有拓展名不同，比如 cat.png 和 cat.jpeg，二者都会和 cat.txt 标签文件对应。为了避免这一情况，PaddleLabel 在导入图像时遇到上述情况会将其中一个文件重命名，如将 cat.png 重命名为 cat-1.png。这可能会导致图像找不到对应标注文件。如果发现有图像提供了标注文件但是导入后没有标注，可以查看 PaddleLabel 运行的命令行输出，对文件名做出调整后重新导入项目。

此外建议将所有图像都放在同一文件夹下，避免重名导致图像标注对应问题。

## 数据标注

创建项目后进入标注界面

1. 您可以点击右侧类别列表下方“添加类别”按钮创建一个新类别
2. 您可以点击一个类别右侧的 x 删除该类别。注：如果有检测框属于该类别，该类别不能被删除
3. 首先点击选中一个类别，之后点击左侧工具栏的“矩形”工具，在画布中按下鼠标左键拖动可以创建一个检测框。每创建一个矩形框，标注信息会自动保存
4. 点击左侧工具栏"编辑"工具，可以修改矩形框两个顶点的位置
5. 点击画布两侧 < > 左右按钮切换图片

## 下一步

您可以继续浏览[自动预标注使用方法](/doc/CN/ML/auto_inference.md)了解如何使用 PaddleLabel-ML 提高标注效率。
