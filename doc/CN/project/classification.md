<!-- TOC -->

- [数据集格式](#%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
    - [单分类](#%E5%8D%95%E5%88%86%E7%B1%BB)
        - [ImageNet 格式](#imagenet-%E6%A0%BC%E5%BC%8F)
        - [ImageNet-txt 格式](#imagenet-txt-%E6%A0%BC%E5%BC%8F)
    - [多分类](#%E5%A4%9A%E5%88%86%E7%B1%BB)
        - [ImageNet-txt 格式](#imagenet-txt-%E6%A0%BC%E5%BC%8F)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
- [完成标注](#%E5%AE%8C%E6%88%90%E6%A0%87%E6%B3%A8)
    - [数据划分](#%E6%95%B0%E6%8D%AE%E5%88%92%E5%88%86)
    - [数据导出](#%E6%95%B0%E6%8D%AE%E5%AF%BC%E5%87%BA)
- [\*分类预标注](#%5C%E5%88%86%E7%B1%BB%E9%A2%84%E6%A0%87%E6%B3%A8)

<!-- /TOC -->

{: .note }
有关数据集[导入](../quick_start.md#导入数据集)，[导出](../quick_start.md#导出数据集)，[训练/验证/测试集划分](../quick_start.md#数据集划分)流程请参考快速开始文档

# 图像分类项目

![image](/doc/CN/assets/classification.png)

PaddleLabel 支持**单分类**和**多分类**两种图像分类项目。其中单分类项目每张图片只能对应一个类别，多分类项目一张图片可以对应多个类别。

## 数据集格式

### 单分类

#### ImageNet 格式

ImageNet 格式数据集中，图像所在文件夹名称即为图像类别。标注 # 可选 的文件导入时可以不提供。

样例格式如下：

```shell
数据集路径
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
├── train_list.txt # 可选
├── val_list.txt # 可选
├── test_list.txt # 可选
└── labels.txt # 可选

# labels.txt
Monkey
Mouse
Cat
```

根据文件夹名表示类别的规则，上述数据集导入后，三张猫和三张狗的图片会有分类，monkey.jpg 没有分类。如果提供了 labels.txt 文件，该文件中的类别会在开始导入图像前按顺序创建。此后如果文件夹名表示的类别不存在会自动创建，因此 labels.txt 不需要包含所有文件夹名。

{: note}
ImageNet 格式仅以图像所在文件夹判断图像分类，train/val/test_list.txt 文件中的数据集**划分信息会被导入**，但是其中的**类别信息不会被导入**。如果您数据集的类别信息保存在三个列表文件中，请选择 ImageNet-txt 格式

#### ImageNet-txt 格式

ImageNet-txt 格式数据集中，图像的类别在 train/val/test_list.txt 文件中声明。

样例格式如下：

<!-- TODO: -->

```shell
数据集路径
├── image
│   ├── cat-1.jpg
│   ├── cat-2.png
│   ├── cat-3.webp
│   ├── dog-1.jpg
│   ├── dog-2.jpg
│   ├── dog-3.jpg
│   ├── monkey.jpg
│   └── ...
├── train_list.txt # 可选
├── val_list.txt # 可选
├── test_list.txt # 可选
└── labels.txt # 可选

# labels.txt
Cat

```

### 多分类

#### ImageNet-txt 格式

多分类的这一个格式和单分类的 ImageNet-txt 格式基本相同，唯一的区别是多分类的 train/val/test_list.txt 文件中，每行文件名后面可以跟多个表示类别的数字或字符串。

样例格式如下：

```shell
Dataset Path
├── image
│   ├── 9911.jpg
│   ├── 9932.jpg
│   └── monkey.jpg
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
image/9932.jpg 2 0
image/9928.jpg monkey
```

## 数据标注

创建项目后会自动跳转到标注页面。

1. 您可以点击右侧标签列表下方“添加标签”按钮创建一个新类别
   ![](/doc/CN/assets/add_label.png)
   ![](/doc/CN/assets/test_label.png)
2. 您可以点击一个类别右侧的 x 删除该类别。注意：如果有图片属于该类别，该类别不能被删除
3. 点击类别进行标注，标注结果将自动保存
4. 完成一张图片标注后点击画布左右 < > 按钮切换图片

<video controls>
  <source src="https://github.com/linhandev/static/releases/download/PaddleLabel%E7%9B%B8%E5%85%B3/clas_ann_demo.mp4" type="video/mp4">
</video>

## 完成标注

完成数据标注后，PaddleLabel 提供了方便的数据划分功能，以便与 Paddle 其他工具套件（如 PaddleClas）进行快速衔接。点击右侧工具栏的**项目总览**按钮，来到该项目的总览界面，这里可以看到数据以及标注状态。

### 数据划分

点击**划分数据集**按钮弹出划分比例的设置，分别填入对应训练集、验证集和测试集的占比，点击确定即可完成数据集的划分。

### 数据导出

点击**导出数据集**，输入需要导出到的文件夹路径，点击确认，即可导出标注完成的数据到指定路径。

## \*分类预标注

PaddleLabel 带有基于 PaddlePaddle 的机器学习分类标注功能，可以通过加载模型实现分类预标注功能，使用方法参考[图像分类自动标注](classification_auto_label.md)。
