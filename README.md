<div id="top"></div>

<!-- shields -->

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge)](https://www.python.org/downloads/release/python-390/) ![PyPI](https://img.shields.io/pypi/v/pplabel?color=blue&style=for-the-badge) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE) [![Start](https://img.shields.io/github/stars/PaddleCV-SIG/PP-Label?color=orange&style=for-the-badge)]() [![Fork](https://img.shields.io/github/forks/PaddleCV-SIG/PP-Label?color=orange&style=for-the-badge)]() ![PyPI - Downloads](https://img.shields.io/pypi/dm/pplabel?color=orange&style=for-the-badge) [![OS](https://img.shields.io/badge/os-linux%2C%20windows%2C%20macos-green.svg?style=for-the-badge)]() 

<!-- project informations -->

<div align="center">
  <a href="https://github.com/PaddleCV-SIG/PP-Label">
    <img src="doc/images/pplabel.png" alt="Logo" width="512">
  </a>
  <!-- <h3 align="center">PP-Label</h3> -->
  <p align="center">
    一个高效且灵活的数据标注工具
    <br />
      <i>An effective and flexible tool for data annotation</i>
    <br />
    <a href="https://github.com/PaddleCV-SIG/PP-Label"><strong>浏览文档 »</strong></a>
    <br />
    <br />
    简体中文 · <a href="doc/README_en.md">English</a>
    <br />
    <br />
    <a href="https://paddlecv-sig.github.io/PP-Label-Frontend/#/PP-Label-Frontend/welcome">查看演示</a>
    ·
    <a href="https://github.com/PaddleCV-SIG/PP-Label/issues">报告错误</a>
    ·
    <a href="https://github.com/PaddleCV-SIG/PP-Label/issues">请求功能</a>
  </p>
</div>
<!-- contents -->

<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#关于项目">关于项目</a>
    </li>
    <li>
      <a href="#使用教程">使用教程</a>
      <ul>
        <li><a href="#安装依赖">安装依赖</a></li>
        <li><a href="#使用">使用</a></li>
        <li><a href="#高级功能">高级功能</a></li>
      </ul>
    <li><a href="#发行说明">发行说明</a></li>
    <li><a href="#许可证书">许可证书</a></li>
    <li>
      <a href="#开源贡献">开源贡献</a>
      <ul>
        <li><a href="#贡献者">贡献者</a></li>
        <li><a href="#鸣谢">鸣谢</a></li>
        <li><a href="#如何参与开源项目">如何参与开源项目</a></li>
      </ul>
    <li><a href="#学术引用">学术引用</a></li>
  </ol>
</details>

<!-- about project -->

## 关于项目

![demo](doc/images/demo2.png)

PP-Label旨在构建一个高效且灵活的图像数据标注工具。整个PP-Label包括三部分，本项目包含PP-Label的后端实现。 [PP-Label-Frontend](https://github.com/PaddleCV-SIG/PP-Label-Frontend)是基于React和Ant Design构建的PP-Label前端，[PP-Label-ML](https://github.com/PaddleCV-SIG/PP-Label-ML)包含基于PaddlePaddle的自动和交互式标注的机器学习后端。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- start -->

## 使用教程

这是一个如何在本地设置项目的示例。要启动并运行本地副本，请遵循以下简单的示例步骤。

### 安装依赖

为了避免依赖问题，建议创建新的虚拟环境进行安装：

```python
conda create -n pplabel python=3.9
conda activate pplabel
```

#### 通过PIP安装

```shell
pip install pplabel
pplabel # 运行 pplabel
```

#### 通过源码安装

首先需要将后端代码克隆到本地：

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label
```

接下来需要克隆并构建前端：

```shell
cd ..
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label-Frontend
npm install -g yarn
yarn
npm run build
```

最后，将构建好的前端部分复制到`pplabel/static/`中：

```shell
cd ../PP-Label
pip install -r requirements.txt
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python setup.py install
pplabel # 运行 pplabel
```

### 使用

完成上述的安装操作后，可以直接使用`pplabel`指令运行PP-Label的前后端。目前PP-Label默认运行在[http://127.0.0.1:17995](http://127.0.0.1:17995)上。同时也可以使用`pplabel --lan`将服务暴露到局域网。这样可以在计算机上运行该服务，并用平板电脑进行注释。在docker中运行pplabel时也需要添加该选项。

```shell
pplabel --lan
```
#### 创建项目

PP-Label支持图像分类、语义/实例分割以及目标/关键点检测的标注任务，浏览器打开PP-Label后，可以通过创建项目下的五个卡片进行不同类型的项目创建。点击卡片进入到对应的功能创建导航菜单，数据地址为本地数据文件夹的路径。完成后点击创建即可进入到标注界面。

#### 数据标注

PP-Label的界面分为图像显示区域，显示区域左右两侧的工具栏（不同任务有不同的工具栏，不同任务的使用详情请参考[数据集文件结构说明](doc/dataset_file_structure.md)）；界面右侧为标签列表，用于添加不同的标签和标注；下方为标注进度展示，上方为可以切换的标签页。使用时：

1. 在右侧创建标签或标注
2. 在工具栏中移动和缩放图像，找到对应的需要标注的目标（图像分类除外）
3. 根据创建项目时选择的标注类型选择对应的工具进行标注
4. 标注完成后点击保存

#### 数据导出

数据集标注完成后通过项目概述对数据集进行训练集、验证集和测试集的划分，并导出数据保存在指定路径。

### 高级功能

PP-Label带有基于PaddlePaddle的机器学习标注功能，可以通过加载模型实现交互式数据标注（目前仅支持语义分割），使用方法如下：

1. 安装PP-Label-ML：

   1. 通过pip安装：

       ```shell
       pip install pplabel-ml
       ```

   2. 通过源码安装：

       ```shell
       git clone https://github.com/PaddleCV-SIG/PP-Label-ML
       cd PP-Label-ML
       python setup.py install
       ```

2. 开启ML后端：

   ```shell
   pplabel-ml # 运行 pplabel-ml
   ```

3. 进入到标注页面，打开右侧工具栏的智能标注功能，在Backend URL中填入ML后端提供的URL。若通过pip方式安装的PP-Label-ML，则自带一个通用的交互式分割模型参数。如果需要针对不同任务选择不同的交互式模型参数，可以通过下方“模型下载”处下载模型参数到本地，并在Model Path和Weight Path中填入对应的`*.pdmodel`和`*.pdiparams`的文件绝对路径，完成后点击Save即可。

4. 点击图像，鼠标左键为添加正样本点，鼠标右键为添加负样本点。

#### 模型下载

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

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- release notes-->

## 发行说明

- [2022.7.XX] [alpha] 测试版本发布。 

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- license -->

## 开源协议

本项目的发布受Apache 2.0 license许可认证，详细信息请查阅[LICENSE](LICENSE)。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- contributors -->

## 开源贡献

### 贡献者

感谢下列开发者参与或协助PP-Label的开发、维护、测试等：[linhandev](https://github.com/linhandev)、[cheneyveron](https://github.com/cheneyveron)、[Youssef-Harby](https://github.com/Youssef-Harby)、[geoyee](https://github.com/geoyee)、[yzl19940819](https://github.com/yzl19940819)、[haoyuying](https://github.com/haoyuying)

### 鸣谢

感谢下列开源项目，使用它们使得PP-Label更加完善和强大：

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

### 如何参与开源项目

如果你有任何好的想法或发现了任何问题，欢迎参与到我们的开发和维护中。有关后端实现的详细信息，请参阅[开发者指南](doc/developers_guide.md)。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- quote-->

## 学术引用

```
@misc{pplabel2022,
    title={PP-Label, An effective and flexible tool for data annotation},
    author={PaddlePaddle Authors},
    howpublished = {\url{https://github.com/PaddleCV-SIG/PP-Label}},
    year={2022}
}
```

<p align="right">(<a href="#top">返回顶部</a>)</p>
