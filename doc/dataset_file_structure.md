# 数据集文件结构说明

本页面旨在描述PP-Label中可以导入/导出的数据集的文件结构，以帮助您更好的使用PP-Label。 **首先需要注意，PP-Label可能修改数据集文件夹下的文件**。像在`Import Additional Data`期间，新的数据文件将被移动到这个项目的数据集文件夹中，此行为旨在节省磁盘空间。虽然目前PP-Label不会删除任何内容，**但您应该考虑在导入之前复制数据集作为备份**。 使用中PP-Label会在该数据集根文件夹下创建一个名为`pplabel`的文件，用于记录警告。 您应该避免更改文件夹下的任何文件，以避免可能出现的问题。

PP-Label在首页为每种类型的标注项目都提供了样本数据集。 通过单击欢迎页面上的”项目样例“按钮，创建您所需要的类型的标注任务，将会下载该任务的示例数据集到`~/.pplabel/sample folder`文件夹中。 

## 无标注数据集

如果您的数据集不包含任何标注，只需将所有的图像文件放在一个文件夹下。 PP-Label会自动遍历文件夹（以及所有子文件夹）并导入所有**PP-Label支持的文件扩展名**的文件，所有隐藏文件（文件名以`.`开头）将被忽略。 

## 基础支持功能

数据集的文件结构在不同类型的标注项目中有所不同，但大多数类型的项目都支持一些基础的特性。

### labels.txt

除了COCO格式标注外的所有标注项目类型都支持`labels.txt `。 PP-Label在导入期间会在数据集的路径下自动寻找`labels.txt`文件。 您可以在这个文件中列出该项目的所有标签（每行一个）。例如下面这样: 

```text
# labels.txt
Monkey
Mouse
```

PP-Label支持任何字符串作为标签名称，但是标签名称可能被用作数据集导出期间的文件夹名称，所以应该避免任何您的操作系统不支持的字符串，可以参开[这里](https://stackoverflow.com/a/31976060)。 PaddlePaddle生态系统中的其他工具箱（比如[PaddleX](https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/data/format/classification.md)）可能也不支持例如中文字符作为标签名称。  

在导入过程中，`labels.txt`包含比标签名称更多的信息。目前支持4种格式，如下所示。其中 `|`表示分隔符，默认为空格。 

标签长度：

- 1： 标签名
- 2： 标签名 | 标签编号
- 3： 标签名 | 标签编号 | 十六进制颜色或常用颜色名称或灰度值 
- 5： 标签名 | 标签编号 | 红色 | 绿色 | 蓝色

排除：

- `//`： `//`后的字符串作为注释
- `-`： 如果你不想指定标签编号，但想指定标签颜色，请在标签编号字段中输入`-`

一些例子：

```text
dog
monkey 4
mouse - #0000ff // mouse's id will be 5
cat 10 yellow
zibra 11 blue // some common colors are supported
snake 12 255 0 0 // rgb color
```

请参阅[这里](https://github.com/PaddleCV-SIG/PP-Label/blob/develop/pplabel/task/util/color.py#L15)获取所有支持的颜色名称。  

在导入过程中，PP-Label会首先创建`labels.txt`中指定的标签。 因此，您可以保证这个文件中的标签的编号将从**0**开始并递增。 在导出过程中也将生成此文件。 

### xx_list.txt

除了COCO格式标注外的所有标注项目类型都支持`xx_list.txt `。 `xx_list.txt `包括`train_list.txt`，` val_list.txt`和`test_list.txt`。 文件应该放在数据集路径的文件夹中，与`labels.txt`相同。 这三个文件指定了数据集的划分以及标签或数据注释与图像文件的匹配关系（就像voc的标注一样，每一行是图像文件的路径和标签文件的路径）。这三个文件的文件结构是相同的，每一行都以一条数据的路径开始，其路径为相对路径，相对于数据集路径。 后面跟着表示类别的整数/字符串，或者标签文件的路径。 例如: 

```text
# train_list.txt
image/9911.jpg 0 3
image/9932.jpg 4
image/9928.jpg Cat
```

对于整数来说，PP-Label将在`labels.txt`中查找标签，索引从**0**开始。对于一些数据可以有多个类别，用于图像多分类。 要使用数字作为标签名称，您可以将数字写在`labels.txt`中，并在`xx_list.txt`中提供标签索引。 或者您可以为数字标签添加一个前缀，例如将`10`表示为`n10`。

这三个文件都将在导出过程中生成，即使其中一些文件是空的。注意，为了确保这些文件可以被PaddlePaddle生态系统中的其他工具包读取，没有注释的数据**不会**包含在`xx_list.txt`中。

## 图像分类

PP-Label支持单标签分类和多标签分类。 

### 单标签分类

也称为ImageNet格式。 样本数据集：[flowers102](https://paddle-imagenet-models-name.bj.bcebos.com/data/flowers102.zip) [vegetables_cls](https://bj.bcebos.com/paddlex/datasets/vegetables_cls.tar.gz)。

示例格式如下：

```shell
Dataset Path
├── Cat
│   ├── cat-1.jpg
│   ├── cat-2.png
│   ├── cat-3.webp
│   └── ...
├── Dog
│   ├── dog-1.jpg
│   ├── dog-2.jpg
│   ├── dog-3.jpg
│   └── ...
├── monkey.jpg
├── train_list.txt
├── val_list.txt
├── test_list.txt
└── label.txt

# labels.txt
Monkey
Mouse
```

单标签分类中图像所在的文件夹名称将被视为它的类别。所以如上格式导入后，三张猫和三张狗的图片会有注释。而monkey.jpg将不会有任何标注。 如果文件夹名称标签还不存在，则会在导入期间创建它们。

为了避免冲突，PP-Label只使用`xx_list.txt`中的数据集划分信息，**这三个文件中的类别信息将不会被考虑**。 您可以使用[此脚本](../tool/clas/mv_image_acc_split.py)在导入数据之前根据三个`xx_list.txt`文件更改数据的位置。 

### 多标签分类

在多标签分类中，一个数据可以有多个类别的标签。

示例格式如下：

```shell
Dataset Path
├── image
│   ├── 9911.jpg
│   ├── 9932.jpg
│   └── monkey.jpg
├── labels.txt
├── test_list.txt
├── train_list.txt
└── val_list.txt

# labels.txt
cat
dog
yellow
black

# train_list.txt
image/9911.jpg 0 3
image/9932.jpg 4 0
image/9928.jpg monkey
```

在多标签分类中，数据的类别、标签编号和标签名称等仅由`xx_list.txt`决定，不会考虑文件夹名称。

## 目标检测

PP-Label支持PASCAL VOC和COCO两种目标检测的数据集格式。

### PASCAL VOC

PASCAL VOC格式将标注信息存储在xml文件中，每个xml文件对应一个图像文件。 样本数据集：[昆虫检测数据集](https://bj.bcebos.com/paddlex/datasets/insect_det.tar.gz)。

示例格式如下：

```shell
Dataset Path
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
├── labels.txt
├── test_list.txt
├── train_list.txt
└── val_list.txt
```

xml文件的格式如下：

```text
<annotation>
	<folder>JPEGImages</folder>
	<filename></filename>
	<source>
		<database></database>
	</source>
	<size>
		<width></width>
		<height></height>
		<depth></depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name></name>
		<pose></pose>
		<truncated></truncated>
		<difficult></difficult>
		<bndbox>
			<xmin></xmin>
			<ymin></ymin>
			<xmax></xmax>
			<ymax></ymax>
		</bndbox>
	</object>
</annotation>
```

在这种格式中，PP-Label将把**数据集路径**下的所有xml文件作为标签，并将该标签与位于`/Dataset Path/folder/filename`的图像文件匹配。 其中的`folder`和`filename`将从该xml文件中解析。 如果xml中没有`folder`节点，默认值将是JPEGImages。 如果文件夹节点数据为空，图像文件应该位于`/Dataset Path/filename`中。

### COCO

COCO格式将一个数据集的所有信息保存在一个`json`文件中。 这里列出了COCO的部分规格，更多细节请访问[COCO官网](https://cocodataset.org/#format-data)进行了解。 注意，在所有使用COCO格式的项目中，`xx_list.txt`和`labels.txt`都是不受支持的。 样本数据集：[Plane Detection]()。

示例格式如下：

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

COCO文件的格式如下：

```text
{
    "info": info,
    "images": [image],
    "annotations": [annotation],
    "licenses": [license],
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

categories[
{
	"id": int,
	"name": str,
	"supercategory": str,
	"color": str // this feature is specific to PP Label. It's not in the coco spec.
}
]
```

PP-Label使用[pycocotoolse](https://github.com/linhandev/cocoapie)解析标注文件。pycocotoolse在[pycocotools](https://github.com/cocodataset/cocoapi)的基础上添加了一些数据集管理功能。该功能会在数据集路径下寻找三个json文件：`train.json`、`val.json`和`test.json`，并从这三个文件中解析解析出用于训练、验证和测试数据集子集。请确保**在所有文件中每个图像的定义不超过一次**，否则导入将失败。`xx_list.txt`和`labels.txt`在所有COCO格式的项目中都不能使用。

PP-Label会导入数据集路径文件夹下的所有图像作为某一任务的数据集，通过寻找COCO记录中基于`Dataset path`以`file_name`结束的相对路径来匹配磁盘上的图像与COCO中的图像记录。例如一个路径为`\Dataset Path\folder\image.png`的图像将与`file_name`为“image.png”的图像记录进行匹配。 如果没有找到或找到大于一个的匹配项，则导入失败。 例如路径为`\Dataset Path\folder1\image.png` 和`\Dataset Path\folder2\image.png`的图像都将与`file_name`为“image.png”的图像进行匹配。 建议将所有图像放在一个文件夹下，以避免重复的图像名称。

如果一个图像的记录中没有包含宽度或高度的信息，PP-Label将在导入期间通过读取图像来获取它们，但这将减慢数据集导入的速度。  

在导出过程中，即使其中一些文件中没有图像记录，这三个json文件也会全部生成。

在类别部分，PP-Label添加了一个颜色字段。 此字段不在原始COCO规格中。该颜色字段会导出保存，并在导入时使用。 

## 图像分割

PP-Label支持两种类型的分割任务（语义分割和实例分割）和两种数据集格式（掩码格式和多边形格式）。语义分割和实例分割在多边形格式中是相同的，而掩码格式中则不同。 

### 多边形

为了将语义分割或实例分割的信息保存为多边形，PP-Label使用COCO格式进行存储。 其导入/导出过程与对象检测项目中使用COCO格式的过程基本相同。 

For saving semantic or instance segmentation information as polygon we use the COCO format. The import and export process is virtually the same to [using COCO format with object detection project](#coco).

### 掩码

在语义分割中，只需要确定输入图像中的每个像素属于哪一类即可。因此输出的结果是与输入图像相同大小的png，其中每个像素将被分配一个灰度或颜色表示类别。

而实例分割在此基础上更进了一步。 不仅需要确定每个像素的类别，而且还区分同一类别的不同实例（如车是同一个类别，但每一辆车都是一个实例）。每个像素都有两个标签，一个是分类标签，另一个是实例编号。 

### 语义分割

样本数据集：[视盘分割数据集](https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz)（注意PP-Label不能直接导入此数据集。 此数据集中的蒙版采用伪颜色。 您必须修改`labels.txt`文件以指定视盘类别的颜色)  。

语义分割中图像和标签都是这种格式（jpg/png/bmp等）的图像文件，所以PP-Label在文件夹结构上设置了更多的限制来区分图像和标签。我们希望所有的图像都放在`/Dataset Path/JPEGImages/`文件夹下，该文件夹下的所有图像都将被PP-Label搜索和自动导入，无论该图像是否存在标签。而标签数据应该放在`/Dataset Path/Annotations/`中。 

示例格式如下：

```shell
Dataset Path
├── Annotations
│   ├── A0001.png
│   ├── B0001.png
│   ├── H0002.png
│   └── ...
├── JPEGImages
│   ├── A0001.jpg
│   ├── B0001.png
│   ├── H0002.bmp
│   └── ...
├── labels.txt
├── test_list.txt
├── train_list.txt
└── val_list.txt

# labels.txt
background -
optic_disk - 128 0 0 // for pesudo color mask, color for each label must be specified
```

在语义分割数据集导入期间，PP-Label将从`labels.txt`中获取标签编号，其中**第一个标签将被视为背景，并给定标签编号为0**。 对于灰度标签，PP-Label会将标签中的像素灰度值与标签编号匹配。 而对于伪彩色标签，PP-Label会将每个像素的颜色与`labels.txt`中指定的颜色进行匹配。 但如果注释没有匹配的标签，导入将失败。   

标签图像通常使用的是PNG格式。 PP-Label在图像文件匹配时会丢掉文件的扩展名，并为图像匹配为具有相同基本文件名的标签。 如果多个图像都对应一个具有相同的基本文件名的标签（尽管它们拥有不同的扩展名，如image.png和image.webp），导入将会失败。  

在导出过程中，`labels.txt`的第一行将始终是背景类。掩码图像中的值遵循与导入时相同的规则。对于灰度标签，输出将是一个单通道图像，灰度值对应分类标签。 对于伪彩色标签，输出将是一个三通道图像，标签颜色作为每个像素的颜色。

### 实例分割

实例分割中导入和导出实例分割掩码的过程类似于语义分割。PP-Label将掩码存储为tiff格式的双通道图像。其中第一个通道（索引为0）是分标签，第二个通道（索引为1）是实例编号。 

[Napari](https://napari.org/#)是用于便捷查看tiff图像的工具。 可以按照[官方文档](https://napari.org/#installation)进行安装。 然后参照下面的步骤使用：

- 打开图像：
![image](https://user-images.githubusercontent.com/29757093/178112182-1b7ae5d7-ab7b-4fee-b851-da2c43676da5.png)
- 打开它对应的PP-Label导出的tiff掩码：
![image](https://user-images.githubusercontent.com/29757093/178112188-e9c2e081-6752-4137-b60d-e64d9e7a11b6.png)
- 右键单击蒙版图层，选择`Split Stack`：
![image](https://user-images.githubusercontent.com/29757093/178112212-13c84d24-d753-4037-8851-d3e09f8fe9c8.png)
![image](https://user-images.githubusercontent.com/29757093/178112232-85feeec9-2ede-4045-9105-446b07454864.png)
- 右键单击图层0，选择`Convert to Label`，查看实例蒙版：
  ![image](https://user-images.githubusercontent.com/29757093/178112305-6a0e36d2-3cab-4265-a88d-9ee55044b97e.png)
- 右键单击图层1，选择`Convert to Label`，可以看到类别蒙版。


https://bj.bcebos.com/paddlex/datasets/xiaoduxiong_ins_det.tar.gz

https://paddlex.readthedocs.io/zh_CN/release-1.3/data/format/index.html
