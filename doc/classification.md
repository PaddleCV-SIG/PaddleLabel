# 分类标注

![classification](https://user-images.githubusercontent.com/71769312/181412360-2a190e7f-6508-432d-9a87-0517e6874a45.png)

## 创建项目

PPLabel支持单类别分类与多类别分类的图像分类标注任务。浏览器打开PPLabel后，可以通过创建项目下的“图像分类”项目创建。点击卡片进入到对应的功能创建导航菜单，数据地址为本地数据文件夹的路径。完成后点击创建即可进入到标注界面。

## 数据标注

PPLabel的界面分为图像显示区域，显示区域左右两侧的工具栏，界面右侧为标签列表，用于添加不同的标签和标注；下方为标注进度展示，上方为可以切换的标签页。使用时：

1. 在右侧创建标签，如果标签存在就选择该图像对应标签（多分类就选择多个对应的标签）
2. 自动完成该图像的类别标注
3. 切换下一张，重复步骤1
4. 直到所有数据标注完毕

## 数据结构

基础结构请参考[这里](dataset_file_structure.md)。

### 单分类

也称为 ImageNet 格式。样例数据集：[flowers102](https://paddle-imagenet-models-name.bj.bcebos.com/data/flowers102.zip)、[vegetables_cls](https://bj.bcebos.com/paddlex/datasets/vegetables_cls.tar.gz)。

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

单分类中图像所在的文件夹名称将被视为它的类别。所以如上数据集导入后，三张猫和三张狗的图片会有分类，monkey.jpg 没有分类。如果与文件夹名同名的标签不存在，导入过程中会自动创建。

为了避免冲突，PPLabel 只使用`xx_list.txt`中的数据集划分信息，**这三个文件中的类别信息将不会被考虑**。您可以使用[此脚本](../tool/clas/mv_image_acc_split.py)在导入数据之前根据三个`xx_list.txt`文件更改数据的位置。

### 多分类

在多分类项目中，一条数据可以有多个类别。

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

在多分类项目中，数据的类别仅由`xx_list.txt`决定，不会考虑文件夹名称。

## 数据导出

数据集标注完成后通过项目概述对数据集进行训练集、验证集和测试集的划分，并导出数据保存在指定路径。
