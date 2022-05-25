# Dataset File Structure

This page describes the dataset file structures that PP Label can import and export. PP Label may make modifications to files under the dataset folder. Like during "Import Additional Data", files will be moved to this folder. Currently we won't delete anything. This behavior is intended to save disk space. **You may make a copy of the dataset as backup before import.** There will be a file named pplabel.warning under the folder PP Label is using. Avoid making changes to files under the folder to avoid bugs.

## Without Annotation

If the dataset doesn't contain any annotation, just put all the files under a single folder. PP Label wil walk through the folder (and all subfolders) to import all files it can annotate based on file name extension.

## Globally Supported Functions

Dataset file structures vary across different types of projects but some functions are globally supported.

### labels.txt

PP Label will look for a labels.txt file under the `Dataset Path` during import. You can list labels in this file, one for each line. For example:

```text
# labels.txt
Monkey
Mouse
```

PP Label supports any string as label name. But label names may be used as folder names during dataset export, so avoid anything your os won't support like listed [here](https://stackoverflow.com/a/31976060). Other toolkits in the PaddlePaddle ecosystem, like [PaddleX](https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/data/format/classification.md), may also not support Chinese chracters as label names.

During import, PP Label will first create labels in labels.txt. So you are guarenteed the ids for labels in this file will start from 0 and increase. During export this file will be generated.

### xx_list.txt

This includes `train_list.txt`, `val_list.txt` and `test_list.txt`. The files should be in the `Dataset Path` folder. These three files specify the dataset split and labels for each piece of data. File stucture for the three files are the same. Each line starts with path to a piece of data, relative to `Dataset Path`. It's followed by integers or strings indicating categories. For example:

```text
# train_list.txt
image/9911.jpg 0 3
image/9932.jpg 4
image/9928.jpg Cat
```

For integers, PP Label will look for the label in `labels.txt`, index starts from 0. There can be multiple categories for one piece of data like in multi class image classification. To use a number as label name, you can either write the number down in `labels.txt` and provide label index in xx_list.txt. Or you can add a prefix to make it not a number like 10 -> n10. All three files will be generated during export, even when some of them are empty.

## Classification

PP Label supports single class and multi class classification.

### Single Class Classification

Also know as ImageNet format. Sample datasets: [flowers102](https://paddle-imagenet-models-name.bj.bcebos.com/data/flowers102.zip) [vegetables_cls](https://bj.bcebos.com/paddlex/datasets/vegetables_cls.tar.gz)

Example Layout

```shell
single_class_classification/
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

The folder name an image is in will be considered it's category. So the three cat and three dog images will have annotation after import. monkey.jpg won't have annotation after import. Folder name labels will be created during import if they doesn't exist.

To avoid confilict, we only use dataset split information in the xx_list.txt file, category information in these three files won't be considered. You can use [this script]() to change the file positions accroding to the three xx_list.txt files before import.

### Multi Class Classification

Example Layout

```shell
multi_class_classification/
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

In multi class classification, images' categories are only decided by xx_list.txt. Folder names aren't considered.

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
