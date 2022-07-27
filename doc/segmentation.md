# 分割标注

## 创建项目

PP-Label支持语义分割与实例分割的图像分割标注任务。浏览器打开PP-Label后，可以通过创建项目下的“语义分割/实例分割”项目创建。点击卡片进入到对应的功能创建导航菜单，数据地址为本地数据文件夹的路径。完成后点击创建即可进入到标注界面。

## 数据标注

PP-Label的界面分为图像显示区域，显示区域左右两侧的工具栏，界面右侧为标签列表，用于添加不同的标签和标注；下方为标注进度展示，上方为可以切换的标签页。使用时：

1. 在右侧创建标签，如果标签存在就选择
2. 逐点描绘物体轮廓
3. 标注完成后点击保存

## 数据结构

基础结构请参考[这里](dataset_file_structure.md)。

PP-Label 支持两种类型的分割任务（语义分割和实例分割）和两种数据集格式（掩膜格式和多边形格式）。语义分割和实例分割中，多边形格式中是完全相同的，二者保存掩膜格式存在区别。

### 多边形格式

PP-Label 使用 COCO 格式将分割结果存为多边形。其导入/导出过程与[目标检测项目中使用 COCO 格式](#coco)的过程基本相同。

### 掩膜格式

进行语义分割时，只需要确定输入图像中每个像素属于哪一类。输出是和输入图像大小相同的 png，每个像素的灰度或颜色代表其类别。而实例分割在此基础上更进一步。不仅需要确定每个像素的类别，而且还要区分同一类别的不同实例（如图像中的所有车属于同一类别，但每一辆车都是一个实例）。实力分割时每个像素都有两个标签，一个是类别标签，另一个是实例编号。

### 语义分割

样例数据集：[视盘分割数据集](https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz)（注意 PP-Label 不能直接导入此数据集。此数据集中的掩膜是伪颜色。您必须修改`labels.txt`文件以指定视盘类别的颜色）。

语义分割中图像和标签都是图像文件，所以需要通过图像所在文件夹区分图像和标签。所有在`/Dataset Path/JPEGImages/`文件夹下的图像都会被导入，无论图像是否存在标签。所有在`/Dataset Path/Annotations/`文件夹下的图片将被作为标签导入。

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

在语义分割数据集导入过程中，PP-Label 将从`labels.txt`中获取标签编号。`labels.txt` 中**第一个标签将被视为背景，并赋标签编号 0**。对于灰度标签，PP-Label 会将标签中的像素灰度值与标签编号匹配。而对于伪彩色标签，PP-Label 会将每个像素的颜色与`labels.txt`中指定的颜色进行匹配。如果掩膜中有标注没有对应的标签，导入将失败。

标签图像通常用 PNG 格式。 PP-Label 在确定图像和标签对应关系时会去掉所有文件拓展名，同名的图像和标签为一组。如果存在多长图像对应一个标签（如图像 image.png 和 image.webp 都对应标签 image.png），导入将会失败。

在导出过程中，**`labels.txt`的第一行固定是背景类**。掩膜图像中的值遵循与导入时相同的规则。对于灰度标签，输出将是一个单通道图像，灰度值对应分类标签。对于伪彩色标签，输出将是一个三通道图像，标签颜色作为每个像素的颜色。

### 实例分割

实例分割中导入和导出掩膜的过程与语义分割类似，区别是标签由单通道或三通道变为二通道，格式由 png 变为 tiff。tiff 标签中第一个通道（下标 0）是类别标签，第二个通道（下标 1）是实例编号。

用[Napari](https://napari.org/)查看这种标签很方便。可以按照[官方文档](https://napari.org/#installation)进行安装。然后参照下面的步骤使用：

- 打开图像：
  ![image](https://user-images.githubusercontent.com/29757093/178112182-1b7ae5d7-ab7b-4fee-b851-da2c43676da5.png)
- 打开图像对应的 tiff 掩膜：
  ![image](https://user-images.githubusercontent.com/29757093/178112188-e9c2e081-6752-4137-b60d-e64d9e7a11b6.png)
- 右键单击掩膜图层，选择`Split Stack`：
  ![image](https://user-images.githubusercontent.com/29757093/178112212-13c84d24-d753-4037-8851-d3e09f8fe9c8.png)
  ![image](https://user-images.githubusercontent.com/29757093/178112232-85feeec9-2ede-4045-9105-446b07454864.png)
- 右键单击图层 0，选择`Convert to Label`，查看实例掩膜：
  ![image](https://user-images.githubusercontent.com/29757093/178112305-6a0e36d2-3cab-4265-a88d-9ee55044b97e.png)
- 右键单击图层 1，选择`Convert to Label`，可以看到类别掩膜。

https://bj.bcebos.com/paddlex/datasets/xiaoduxiong_ins_det.tar.gz

https://paddlex.readthedocs.io/zh_CN/release-1.3/data/format/index.html

## 高级功能

PP-Label带有基于PaddlePaddle的机器学习标注功能，可以通过加载模型实现交互式数据标注（目前仅支持语义分割），使用方法如下：

1. 进入到标注页面，打开右侧工具栏的智能标注功能，在Model Path和Weight Path中填入对应的`*.pdmodel`和`*.pdiparams`的文件路径，点击Save即可。
2. 点击图像，鼠标左键为添加正样本点，鼠标右键为添加负样本点。

### 模型下载

| 模型类型     | 适用场景             | 模型结构            | 模型下载地址                                                 |
| ------------ | -------------------- | ------------------- | ------------------------------------------------------------ |
| 高精度模型   | 通用场景的图像标注   | HRNet18_OCR64       | [static_hrnet18_ocr64_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_cocolvis.zip) |
| 轻量化模型   | 通用场景的图像标注   | HRNet18s_OCR48      | [static_hrnet18s_ocr48_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_cocolvis.zip) |
| 高精度模型   | 通用图像标注场景     | EdgeFlow            | [static_edgeflow_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_edgeflow_cocolvis.zip) |
| 高精度模型   | 人像标注场景         | HRNet18_OCR64       | [static_hrnet18_ocr64_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_human.zip) |
| 轻量化模型   | 人像标注场景         | HRNet18s_OCR48      | [static_hrnet18s_ocr48_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_human.zip) |
| 轻量化模型   | 遥感建筑物标注场景   | HRNet18s_OCR48      | [static_hrnet18_ocr48_rsbuilding_instance](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr48_rsbuilding_instance.zip) |
| 高精度模型\* | x光胸腔标注场景      | Resnet50_Deeplabv3+ | [static_resnet50_deeplab_chest_xray](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_resnet50_deeplab_chest_xray.zip) |
| 轻量化模型   | 医疗肝脏标注场景     | HRNet18s_OCR48      | [static_hrnet18s_ocr48_lits](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_lits.zip) |
| 轻量化模型\* | MRI椎骨图像标注场景  | HRNet18s_OCR48      | [static_hrnet18s_ocr48_MRSpineSeg](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_MRSpineSeg.zip) |
| 轻量化模型\* | 质检铝板瑕疵标注场景 | HRNet18s_OCR48      | [static_hrnet18s_ocr48_aluminium](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_aluminium.zip) |