# 交互式分割标注

![interactive_segmentation](https://user-images.githubusercontent.com/71769312/181561624-de3f74e4-ca86-4764-a7a5-9043b9a1c363.png)

PaddleLabel 基于[EISeg](https://github.com/PaddlePaddle/PaddleSeg/tree/release/2.6/EISeg)后端支持交互式分割。

## 安装说明

要使用交互式分割功能，需要安装 PaddleLabel ML 扩展。

### 通过 PIP 安装

```shell
pip install paddlelabel-ml
```

### 通过源码安装

首先需要将 ML 代码克隆到本地：

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel-ML
```

接下来需要安装 ML：

```shell
cd PaddleLabel-ML
python setup.py install
```

## 启动

完成上述的安装操作后，可以直接在终端使用如下指令启动 PaddleLabel 的机器学习端。

```shell
paddlelabel_ml  # 启动ml后端
```

## 数据标注

前置的项目创建及数据准备等工作与[分割标注](segmentation.html)相同，其不同点在于：

1. 启动 ML 后端并进入到分割标注任务后，可点击右侧工具栏的“智能标注”按钮，将 ML 后端的 URL 复制粘贴到 ML Backend 中，点击 Save 即可。
1. 点击图像，鼠标左键为添加正样本点，鼠标右键为添加负样本点，**单个目标的交互式模式以鼠标中键进行确认，建议用户在标注完每一个目标后点击一次鼠标中键，这样标注结果精度回更高**。
1. 点击"**确认轮廓**"来完成实例标注时单个目标的生成。

_注意：① 当在智能标注状态，左侧工具栏部分功能无法使用，需要再次点击“智能标注”暂时关闭该功能后左侧工具栏可以正常使用。②ML 后端默认自带一个通用交互式模型，如果需要使用其他特定领域的模型，可以在下方的模型下载区域进行下载，并在“智能标注”按钮中的 Model Path 和 Weight Path 中填入对应的`_.pdmodel`和`_.pdiparams`的文件路径。_

### \*模型下载

| 模型类型     | 适用场景             | 模型结构            | 模型下载地址                                                                                                                       |
| ------------ | -------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 高精度模型   | 通用场景的图像标注   | HRNet18_OCR64       | [static_hrnet18_ocr64_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_cocolvis.zip)                       |
| 轻量化模型   | 通用场景的图像标注   | HRNet18s_OCR48      | [static_hrnet18s_ocr48_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_cocolvis.zip)                     |
| 高精度模型   | 通用图像标注场景     | EdgeFlow            | [static_edgeflow_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_edgeflow_cocolvis.zip)                                 |
| 高精度模型   | 人像标注场景         | HRNet18_OCR64       | [static_hrnet18_ocr64_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_human.zip)                             |
| 轻量化模型   | 人像标注场景         | HRNet18s_OCR48      | [static_hrnet18s_ocr48_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_human.zip)                           |
| 轻量化模型   | 遥感建筑物标注场景   | HRNet18s_OCR48      | [static_hrnet18_ocr48_rsbuilding_instance](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr48_rsbuilding_instance.zip) |
| 高精度模型\* | x 光胸腔标注场景     | Resnet50_Deeplabv3+ | [static_resnet50_deeplab_chest_xray](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_resnet50_deeplab_chest_xray.zip)             |
| 轻量化模型   | 医疗肝脏标注场景     | HRNet18s_OCR48      | [static_hrnet18s_ocr48_lits](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_lits.zip)                             |
| 轻量化模型\* | MRI 椎骨图像标注场景 | HRNet18s_OCR48      | [static_hrnet18s_ocr48_MRSpineSeg](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_MRSpineSeg.zip)                 |
| 轻量化模型\* | 质检铝板瑕疵标注场景 | HRNet18s_OCR48      | [static_hrnet18s_ocr48_aluminium](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_aluminium.zip)                   |
