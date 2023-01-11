<!-- TOC -->

- [数据集格式](#%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
    - [单分类](#%E5%8D%95%E5%88%86%E7%B1%BB)
        - [ImageNet 格式](#imagenet-%E6%A0%BC%E5%BC%8F)
        - [ImageNet-txt 格式](#imagenet-txt-%E6%A0%BC%E5%BC%8F)
    - [多分类](#%E5%A4%9A%E5%88%86%E7%B1%BB)
        - [ImageNet-txt 格式](#imagenet-txt-%E6%A0%BC%E5%BC%8F)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
- [深度学习预标注](#%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E9%A2%84%E6%A0%87%E6%B3%A8)

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

创建项目后会自动跳转到标注页面

1. 您可以点击右侧标签列表下方“添加标签”按钮创建一个新类别
   ![](/doc/CN/assets/add_label.png)
   ![](/doc/CN/assets/test_label.png)
2. 您可以点击一个类别右侧的 x 删除该类别。注意：如果有图片属于该类别，该类别不能被删除
3. 点击类别进行标注，单分类项目仅允许选中一个类别，多分类项目可以同时选中多个类别。标注结果将自动保存
4. 完成一张图片标注后点击画布左右 < > 按钮切换图片

<!-- https://just-the-docs.github.io/just-the-docs/docs/utilities/layout/#display -->

https://user-images.githubusercontent.com/29757093/211701850-5ba4e377-9afe-4fbb-8aee-379c2439cdc3.mp4

<video controls src="https://github.com/linhandev/static/releases/download/PaddleLabel%E7%9B%B8%E5%85%B3/clas_ann_demo.mp4" width="100%"></video>

## 深度学习预标注

{: note}
在使用深度学习相关功能前请先按照说明[安装并启动](/doc/CN/install_ml.md) PaddleLabel-ML 后端
