# 安装指南

<!-- TOC -->

- [安装方式](#%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F)
    - [通过 pip 安装](#%E9%80%9A%E8%BF%87-pip-%E5%AE%89%E8%A3%85)
    - [下载最新开发版](#%E4%B8%8B%E8%BD%BD%E6%9C%80%E6%96%B0%E5%BC%80%E5%8F%91%E7%89%88)
    - [通过源码安装](#%E9%80%9A%E8%BF%87%E6%BA%90%E7%A0%81%E5%AE%89%E8%A3%85)
- [启动](#%E5%90%AF%E5%8A%A8)
    - [更多启动选项](#%E6%9B%B4%E5%A4%9A%E5%90%AF%E5%8A%A8%E9%80%89%E9%A1%B9)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

为了避免环境冲突，建议首先创建一个新的虚拟环境。

```python
conda create -n paddlelabel python=3.11
conda activate paddlelabel
```

## 安装方式

您可以通过以下三种方式中的**任意一种**安装 PaddleLabel，其中通过 pip 安装最简单。

### 通过 pip 安装

```shell
pip install --upgrade paddlelabel # 更新和安装后升级 paddlelabel 都是用这行命令
```

看到类似于 `Successfully installed paddlelabel-0.5.0` 的命令行输出即为安装成功，您可以直接继续浏览[启动](#%E5%90%AF%E5%8A%A8)章节。

{: .note }
**以下两种安装方式主要针对二次开发场景**

### 下载最新开发版

<details> <summary markdown="span">详细步骤</summary>
每当 PaddleLabel 的代码有更新，项目的 Github Action 脚本都会构建一个反映最新版代码的安装包。这一安装包未经过全面测试，因此很可能存在一些问题，仅推荐为尝试最新版本使用。其中可能修复了一些 pypi 版本中存在的问题，添加了一些新功能或进行了一些性能提升。

安装方式为

<!-- 1. 访问 [Action 执行记录网页](https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/build.yml)
2. 选择最上面（最新）的一条记录，点击进入
   ![](/doc/CN/assets/action-1.png)
3. 滑到页面最下方，点击下载 PaddleLabel_built_package 压缩包
   ![1](https://user-images.githubusercontent.com/29757093/201905747-a2b0901c-9331-4a90-b4ae-44c855314810.jpg) -->

1. 从[此链接](https://nightly.link/PaddleCV-SIG/PaddleLabel/workflows/build/develop/PaddleLabel_built_package.zip)下载最新开发版安装包
2. 解压该压缩文件，之后执行

```shell
pip install [解压出的.whl文件名，如 paddlelabel-0.5.0-py3-none-any.whl ]
```

</details>

### 通过源码安装

<details> <summary markdown='span'>详细步骤</summary>
以下命令针对bash命令行，一些类似cp，mv指令可能无法在powershell或cmd.exe中执行。不过每步的作用都有说明，可以在文件管理器中完成等效的操作。

1. 首先将后端代码克隆到本地

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel
```

2. 接下来克隆并构建前端，构建前请确保安装了 [Node.js](https://nodejs.org/en/) 和 npm

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel-Frontend
cd PaddleLabel-Frontend
npm install --location=global yarn
yarn
yarn run build
```

3. 将构建好的前端部分，`PaddleLabel-Frontend/dist/` 目录下所有文件复制到 `PaddleLabel/paddlelabel/static/` 目录中

```shell
cd ../PaddleLabel/
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/
```

4. 安装 PaddleLabel 或不安装直接启动

```shell
# 在PaddleLabel目录下
python setup.py install # 安装PaddleLabel

python -m paddlelabel # 不安装直接启动
```

</details>

## 启动

安装成功后，可以在终端使用如下指令启动 PaddleLabel

```shell
paddlelabel  # 启动paddlelabel
pdlabel # 缩写，和paddlelabel完全相同
```

PaddleLabel 启动后会自动在浏览器中打开网页。

### 更多启动选项

- -p, \-\-port：指定运行端口。PaddleLabel 默认运行网址为[http://localhost:17995](http://localhost:17995)
- -l, \-\-lan：暴露服务到局域网。开启后可以在同一局域网下机器 A 上运行 PaddleLabel，在电脑 B 或平板 C 上进行标注。在 docker 中运行时也需要添加 -l
- -d， \-\-debug：在命令行中显示更详细的 log，可用于观察导入导出过程中的行为，定位问题等

```shell
paddlelabel --port 8000 --lan --debug # 在8000端口上运行，将服务暴露到局域网，显示详细log
```

更多启动参数可以使用 `paddlelabel -h` 查看。

## 下一步

恭喜您成功运行 PaddleLabel！您可以继续浏览[快速开始](./quick_start.md)页面了解 PaddleLabel 的主要功能和使用流程。
