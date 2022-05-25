# Dataset File Structure

This page describes the dataset file structures that PP Label can import and export.

## Without Annotation

If the dataset doesn't contain any annotation, just put all the files under a single folder. PP Label wil walk through the folder( including all subfolders) to import all files it can annotate based on file name extension.

## Classification

PP Label supports single class and multi class classification.

### Single Class Classification

Also know as ImageNet format. Sample datasets: [flowers102](https://paddle-imagenet-models-name.bj.bcebos.com/data/flowers102.zip) [vegetables_cls](https://bj.bcebos.com/paddlex/datasets/vegetables_cls.tar.gz)

Example Layout

```shell
PetImages/
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
monky
mouse
```

The folder name an image is in will be considered to be it's category. So the three cat and three dog images will have annotation after import. monkey.jpg won't have annotation after import. Folder name labels will be created during import if they doesn't exist.

label.txt is optional. You will select the path to this file during dataset import. List labels in this file, one for each line. Even you don't list folder name labels, they will be created during import. PP Label supports any string as label name but this name will be used as the folder name during export. So avoid any character your os doesn't allow. To use exported dataset with [PaddleX](https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/data/format/classification.md), don't include any space or Chinese characters in label name.

Labels in label.txt will be created first during import. So the id for labels in labels.txt will start from 1 and increment.

### Multi Class Classification

Example Layout

```shell
PetImages/
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
├── cat-4.png
├── cat-5.png
├── dog-4.png
├── dog-5.png
├── monkey.jpg
└── labels.txt

# labels.txt
Cat/cat-1.jpg Cat Yellow
cat-4.png Cat Black
monkey.jpg Monkey Yellow Black
```

In multi class classification, images' annotation are only decided by labels.txt. Folder name aren't relevant.

In labels.txt, each line's first part is the image's relative path `to the dataset base directory`, not to labels.txt. All other strings in the line will be a category for the image. You can specify other delimiters than space during import, so space in category name is also possible.

## Detection

PP Label supports two object detection dataset format: PASCAL VOC and COCO.

### PASCAL VOC

[Example Datasset](https://bj.bcebos.com/paddlex/datasets/insect_det.tar.gz)

Example Layout:

```shell
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

Format for the xml fils is as follows

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

## Segmentation

### Semantic Segmentation

https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz

### Instance Segmentation

https://bj.bcebos.com/paddlex/datasets/xiaoduxiong_ins_det.tar.gz

https://paddlex.readthedocs.io/zh_CN/release-1.3/data/format/index.html
