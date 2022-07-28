# 检测标注

![detection](https://user-images.githubusercontent.com/71769312/181412379-42721d08-aba2-4e73-a2ae-f925721b4b03.png)

## 创建项目

PP-Label支持图像目标检测的标注任务。浏览器打开PP-Label后，可以通过创建项目下的“图像分类”项目创建。点击卡片进入到对应的功能创建导航菜单，数据地址为本地数据文件夹的路径。完成后点击创建即可进入到标注界面。

## 数据标注

PP-Label的界面分为图像显示区域，显示区域左右两侧的工具栏，界面右侧为标签列表，用于添加不同的标签和标注；下方为标注进度展示，上方为可以切换的标签页。使用时：

1. 在右侧创建标签，如果标签存在就选择
2. 在左侧点击矩形，在界面上点击物体的左上角和右下角，完成当前目标的标注
3. 切换下一张，重复上述步骤，直到标注完成

## 数据结构

基础结构请参考[这里](dataset_file_structure.md)。

PP-Label 支持 PASCAL VOC 和 COCO 两种目标检测数据集格式。

### PASCAL VOC

PASCAL VOC 格式将标注信息保存在 xml 文件中，每个图像都对应一个 xml 文件。样例数据集：[昆虫检测数据集](https://bj.bcebos.com/paddlex/datasets/insect_det.tar.gz)。

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

xml 文件格式如下：

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

导入 VOC 格式数据集时，PP-Label 将把数据集路径下所有 xml 结尾文件作为标签，并将该标签与位于`/数据集路径/folder/filename`的图像文件匹配。路径中的`folder`和`filename`将从该 xml 文件中解析。如果 xml 中没有`folder`节点，默认值是 JPEGImages。如果`folder`节点内容为空，将认为图像文件位于`/数据集路径/filename`。

### COCO

COCO 格式将整个数据集的所有标注信息存在一个`json`文件中。这里列出了 COCO 的部分格式规范，更多细节请访问[COCO 官网](https://cocodataset.org/#format-data)。注意，所有使用 COCO 格式的项目都不支持`xx_list.txt`和`labels.txt`。样例数据集：[Plane Detection]()。

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

COCO 文件的格式如下：

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

PP-Label 使用[pycocotoolse](https://github.com/linhandev/cocoapie)解析标注文件。pycocotoolse 与原版 [pycocotools](https://github.com/cocodataset/cocoapi)基本相同，只是在其基础上增加了一些数据集管理功能。导入过程中 PP-Label 会在数据集路径下寻找三个 json 文件：`train.json`、`val.json`和`test.json`，并从这三个文件中解析解析出用于训练、验证和测试的数据。请确保**每个图像在三个 json 中只被定义一次**，否则将导入失败。

PP-Label 会导入数据集文件夹下的所有图像。COCO json 中每张图有一个 `file_name`，如果一张图的路径以 COCO json 中某一条记录的`file_name`结尾，将认为二者匹配。比如一个路径为`\Dataset Path\folder\image.png`的图像将与`file_name`为“image.png”的图像记录匹配。如果发现一张图片有多条匹配的记录，导入会失败。例如路径为`\Dataset Path\folder1\image.png`和`\Dataset Path\folder2\image.png`的两张图像都将与`file_name`为“image.png”的图像匹配。建议将所有图像放在一个文件夹下，以避免图像重名。

如果一个图像的记录中没有包含宽度或高度的信息，PP-Label 将在导入期间读取图像来获取。这将拖慢数据集导入速度。

导出过程中，三个 COCO json 文件都会生成，就算其中一些是空的。

在 COCO json 的分类部分，PP-Label 添加了一个颜色字段。这个字段不在标准的 COCO 结构中。颜色字段会导出保存，并在导入时使用。

## 数据导出

数据集标注完成后通过项目概述对数据集进行训练集、验证集和测试集的划分，并导出数据保存在指定路径。