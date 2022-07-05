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
        <li><a href="#数据导入/导出">数据导入/导出</a></li>
        <li><a href="#图像分类">图像分类</a></li>
        <li><a href="#语义分割">语义分割</a></li>
        <li><a href="#目标检测">目标检测</a></li>
        <li><a href="#关键点检测">关键点检测</a></li>
      </ul>
    <li><a href="#发行说明">发行说明</a></li>
    <li><a href="#许可证书">许可证书</a></li>
    <li><a href="#开源贡献">开源贡献</a></li>
    <li><a href="#学术引用">学术引用</a></li>
  </ol>
</details>


<!-- about project -->

## 关于项目

![demo](doc/images/demo2.png)

PP-Label旨在构建一个高效且灵活的图像数据标注工具。目前该完整的PP-Label包含三部分，这个项目包含PP-Label的后端实现。 [PP-Label-Frontend](https://github.com/PaddleCV-SIG/PP-Label-Frontend)是基于React和Ant Design构建的前端实现，[PP-Label-ML](https://github.com/PaddleCV-SIG/PP-Label-ML)包含基于PaddlePaddle的用于自动和交互标注的机器学习后端实现。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- start -->

## 使用教程

这是一个如何在本地设置项目的示例。要启动并运行本地副本，请遵循以下简单的示例步骤。

### 安装依赖

建议创建一个新的虚拟环境进行安装：

```python
conda create -n pplabel python=3.9
conda activate pplabel
```

#### 通过PIP进行安装

```shell
pip install pplabel
pplabel
```

#### 通过源码进行安装

首先需要将源代码克隆到本地：

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label
```

接下来需要克隆并构建前端部分：

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label-Frontend
npm install -g yarn
yarn
npm run build
cd ..
```

最后，将构建好的前端部分复制到`pplabel/static/`中：

```shell
cd PP-Label
pip install -r requirements.txt
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python setup.py install
```

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 使用

完成上述的安装操作后，可以直接使用`pplabel`指令运行PP-Label的前后端。目前PP-Labell默认运行在[http://127.0.0.1:17995](http://127.0.0.1:17995)上。同时也可以选择将服务公开给`lan`。这样就可以在计算机上运行该服务，并用平板电脑进行注释：

```shell
pplabel --lan
```

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 数据导入/导出

XXXXXXXXXX。

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 图像分类

XXXXXXXXXX。

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 语义分割

XXXXXXXXXX。

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 目标检测

XXXXXXXXXX。

<p align="right">(<a href="#top">返回顶部</a>)</p>

### 关键点检测

XXXXXXXXXX。

<p align="right">(<a href="#top">返回顶部</a>)</p>



<!-- release notes-->

## 发行说明

- [2022.7.XX] [alpha] 测试版本。 

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- license -->

## 开源协议

本项目的发布受Apache 2.0 license许可认证。

<p align="right">(<a href="#top">返回顶部</a>)</p>

<!-- contributors -->

## 开源贡献

- 非常感谢XXXXXXX。
- 非常感谢XXXXXXX。

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
