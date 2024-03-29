# 机器学习后端安装

<!-- TOC -->

- [前置步骤](#%E5%89%8D%E7%BD%AE%E6%AD%A5%E9%AA%A4)
- [安装方式](#%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F)
    - [通过 pip 安装](#%E9%80%9A%E8%BF%87-pip-%E5%AE%89%E8%A3%85)
    - [下载最新开发版](#%E4%B8%8B%E8%BD%BD%E6%9C%80%E6%96%B0%E5%BC%80%E5%8F%91%E7%89%88)
    - [通过源码安装](#%E9%80%9A%E8%BF%87%E6%BA%90%E7%A0%81%E5%AE%89%E8%A3%85)
- [启动](#%E5%90%AF%E5%8A%A8)
    - [更多启动选项](#%E6%9B%B4%E5%A4%9A%E5%90%AF%E5%8A%A8%E9%80%89%E9%A1%B9)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

## 前置步骤

为了避免环境冲突，建议首先创建一个新的虚拟环境。

```python
conda create -n paddlelabel-ml python=3.10
conda activate paddlelabel-ml
```

您可以选择安装 cpu 或 gpu 版本的 PaddlePaddle，cpu 版本安装简便，首次尝试推荐安装这一版本；gpu 版本推理速度更快，重度使用时体验更好。推荐安装不低于 2.2.0 版本的 PaddlePaddle。

cpu 版本

```shell
pip install paddlepaddle
```

gpu 版本

```shell

```

<!-- TODO: -->

## 安装方式

与 PaddleLabel 类似，您可以通过以下三种方式中的**任意一种**安装 PaddleLabel-ML，其中通过 pip 安装最简单。

### 通过 pip 安装

```shell
pip install --upgrade paddlelabel-ml
```

看到类似于 `Successfully installed paddlelabel-ml-0.5.0` 的命令行输出即为安装成功，您可以直接继续浏览[启动](#%E5%90%AF%E5%8A%A8)章节。

{: .note }
**以下两种安装方式主要针对二次开发场景**

### 下载最新开发版

<details> <summary markdown="span">详细步骤</summary>
每当 PaddleLabel-ML 的代码有更新，项目的 Github Action 脚本都会构建一个反映最新版代码的安装包。这一安装包未经过全面测试，因此很可能存在一些问题，仅推荐为尝试最新版本使用。其中可能修复了一些 pypi 版本中存在的问题，添加了一些新功能或进行了一些性能提升。

下载方式为

<!-- TODO: 更新图片 -->

1. 访问 [Action 执行记录网页](https://github.com/PaddleCV-SIG/PaddleLabel-ML/actions/workflows/build.yml)
2. 选择最上面（最新）的一条执行记录，点击进入
   ![](/doc/CN/assets/action-1.png)
3. 滑到页面最下方，点击下载
   PaddleLabel-ML_built_package 压缩包
   ![1](https://user-images.githubusercontent.com/29757093/201905747-a2b0901c-9331-4a90-b4ae-44c855314810.jpg)
4. 解压该压缩包，之后执行

```shell
pip install [解压出的.whl文件名，如 paddlelabel-ml-0.5.0-py3-none-any.whl ]
```

</details>

### 通过源码安装

<details> <summary markdown='span'>详细步骤</summary>

<!-- TODO: -->

</details>

## 启动

完成上述的安装操作后，可以直接在终端使用如下指令启动 PaddleLabel-ML

```shell
paddlelabel-ml  # 启动paddlelabel-ml
```

看到类似 `PaddleLabel-ML is running at http://localhost:1234` 的输出即为启动成功。您也可以访问[http://localhost:1234/running](http://localhost:1234/running)网页确定 ML 后端是否启动成功。

{: .note}
PaddleLabel-ML 没有独立的前端网页，您可以继续浏览[机器学习辅助标注](/doc/CN/ML/ml.md)章节了解如何在各个类型项目中配置和使用机器学习辅助标注功能。

### 更多启动选项

PaddleLabel-ML 的默认运行网址为[http://localhost:1234](http://localhost:1234)。如果该端口已被占用，可以通过`--port`或`-p`参数指定其他端口。此外可以通过`--lan`或`-l`参数将服务暴露到局域网。在 docker 中运行 PaddleLabel 时也需要添加`--lan`参数。

```shell
paddlelabel --port 6000 --lan  # 在6000端口上运行并将服务暴露到局域网
```

更多启动参数可以使用 `paddlelabel-ml -h` 查看。

## 下一步

恭喜您成功运行 PaddleLabel 机器学习辅助标注后端！您可以继续浏览[机器学习辅助标注](/doc/CN/ML/ml.md)章节了解如何在各个类型项目中配置和使用辅助标注功能。
