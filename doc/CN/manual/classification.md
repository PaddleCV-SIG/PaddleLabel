# 图像分类手动标注

<!-- TOC -->

- [单分类数据集格式](#%E5%8D%95%E5%88%86%E7%B1%BB%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
    - [ImageNet](#imagenet)
    - [ImageNet-txt](#imagenet-txt)
- [多分类数据集格式](#%E5%A4%9A%E5%88%86%E7%B1%BB%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
    - [ImageNet-txt](#imagenet-txt)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

![image](/doc/CN/assets/classification.png)

PaddleLabel 支持**单分类**和**多分类**两种图像分类项目。其中单分类项目一张图片只能对应一个类别，多分类项目一张图片可以对应多个类别。

## 单分类数据集格式

### ImageNet

{: .label }
v0.1.0+

ImageNet 格式数据集中，图像所在文件夹名称即为图像类别。

样例格式如下，标注 `# 可选` 的文件导入时可以不提供：

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

# train_list.txt
Cat/cat-1.jpg 2
```

根据文件夹名表示类别的规则，上述数据集导入后，三张猫和三张狗的图片会有分类，monkey.jpg 没有分类。

如果提供了 labels.txt 文件，该文件中的类别会在开始导入图像之前按顺序创建。此后如果文件夹名表示的类别不存在也会自动创建，因此 labels.txt 不需要包含所有文件夹名。

{: .note}
ImageNet 格式仅以图像所在文件夹判断图像分类，train/val/test_list.txt 文件中的**子集划分信息会被导入**，但是其中的**类别信息不会被导入**。如果您数据集的类别信息保存在三个列表文件中，请使用 ImageNet-txt 格式

### ImageNet-txt

{: .label }
v1.0.0+

ImageNet-txt 格式的数据集在 train/val/test_list.txt 文件中记录图像的类别。

样例格式如下：

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
Monkey
Mouse
Cat

# train_list.txt
image/dog-1.jpg Dog
image/cat-2.png 2 # 对应 labels.txt 中第三行类别 Cat
```

labels.txt 的处理同 ImageNet 格式。在三个列表文件中，每行使用空格分隔，第一部分为到一个图片文件的路径，第二部分为一个字符串或一个数字代表类别。

- labels.txt 中类别编号从 0 开始，所以数字类别 i 将对应 labels.txt 中第 i+1 行
- 字符串类别的处理同 ImageNet 格式中的文件夹名，如果不存在对应类别将在导入过程中自动创建

{: .note}
三个列表文件以空格为分隔符，请不要在文件路径或类别名称中使用空格

## 多分类数据集格式

### ImageNet-txt

{: .label }
v0.1.0+

多分类的 ImageNet-txt 格式和单分类的基本相同，唯一区别是多分类的三个列表文件中，每行文件名后面可以跟多个空格分隔的表示类别的数字或字符串。

样例格式如下：

```shell
数据集路径
├── image
│   ├── cat.jpg
│   ├── dog.jpg
│   └── monkey.jpg
├── labels.txt # 可选
├── test_list.txt # 可选
├── train_list.txt # 可选
└── val_list.txt # 可选

# labels.txt
cat
dog
yellow
black

# train_list.txt
image/cat.jpg 0 2 # 对应第一行和第3行类别，cat，yellow
image/dog.jpg 1 3
image/monkey.jpg monkey yellow black
```

{: .note}
三个列表文件以空格为分隔符，请不要在文件路径或类别名称中使用空格

## 数据标注

创建项目后会自动跳转到标注页面

1. 您可以点击右侧类别列表下方“添加类别”按钮创建一个新类别
   ![](/doc/CN/assets/add_label.png)
   ![](/doc/CN/assets/test_label.png)
2. 您可以点击一个类别右侧的 x 删除该类别。注：如果有图片属于该类别，该类别不能被删除
3. 点击类别进行标注，单分类项目仅允许选中一个类别，多分类项目可以同时选中多个类别。每次选择后标注结果将自动保存，页面上方将提示“保存成功”
4. 完成一张图片标注后点击画布左右 < > 按钮切换图片

<video controls src="https://github.com/linhandev/static/releases/download/PaddleLabel%E7%9B%B8%E5%85%B3/clas_ann_demo.mp4" width="100%"></video>

## 下一步

您可以继续浏览[自动预标注使用方法](/doc/CN/ML/auto_inference.md)了解如何使用 PaddleLabel-ML 提高分类项目标注效率。
