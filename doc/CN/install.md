# 安装指南

<!-- TOC -->

- [安装方式](#%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F)
  - [通过 pip 安装](#%E9%80%9A%E8%BF%87-pip-%E5%AE%89%E8%A3%85)
  - [下载最新开发版](#%E4%B8%8B%E8%BD%BD%E6%9C%80%E6%96%B0%E5%BC%80%E5%8F%91%E7%89%88)
  - [通过源码安装](#%E9%80%9A%E8%BF%87%E6%BA%90%E7%A0%81%E5%AE%89%E8%A3%85)
- [启动](#%E5%90%AF%E5%8A%A8)
  - [更多启动选项](#%E6%9B%B4%E5%A4%9A%E5%90%AF%E5%8A%A8%E9%80%89%E9%A1%B9)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)
- [安装 FAQ](#%E5%AE%89%E8%A3%85-faq)
  - [Windows 下使用 msys2 运行](#windows-%E4%B8%8B%E4%BD%BF%E7%94%A8-msys2-%E8%BF%90%E8%A1%8C)
  - [Microsoft Visual C++ 14.1 is required](#microsoft-visual-c-141-is-required)
  - [中文兼容问题](#%E4%B8%AD%E6%96%87%E5%85%BC%E5%AE%B9%E9%97%AE%E9%A2%98)

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
如果使用Windows系统，推荐使用git bash或powershell执行以下命令。

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

## 安装 FAQ

<!-- TODO: 折叠，不用标题 -->

<!-- ### Windows 下安装依赖软件

推荐使用 [chocolatey](https://community.chocolatey.org/) 在 Windows 上进行依赖管理。chocolatey 的安装可以参考[官方文档](https://chocolatey.org/install)。一些 PaddleLabel 可能需要的依赖安装命令如下：

```shell
choco install python # python
choco install miniconda3 # miniconda
``` -->

### Windows 下使用 msys2 运行

如果您在 Windows 中使用 PaddleLabel 时遇到了不容易解决的问题，如无法使用中文，可以尝试在 Windows Linux 子系统或 msys2 环境中运行。以下为在 msys2 中运行方法

- 访问 [msys2 官网](https://www.msys2.org/)下载安装 msys2，或使用 [chocolatey](https://chocolatey.org/install) 安装

```shell
choco install msys2
```

- 运行 msys2 msys，安装项目依赖

```shell
pacman -S python
```

### Microsoft Visual C++ 14.1 is required

如果 `pip install paddlelabel` 命令报错，可以使用 `pip install numpy` 尝试单独安装 numpy。如果安装 numpy 时在命令行中看到如下报错说明缺少 msvc 依赖。

```shell
error: Microsoft Visual C++ 14.1 is required. Get it with "Build Tools for Visual Studio"
```

- 访问命令行给出的网址下载 Microsoft Visual C++ 构建工具，下载完成后运行
- 点击左侧 “使用 C++ 的桌面开发”
- 选中一个最新的 MSVC
- 根据 Windows 版本选中一个最新的 Windows 10/11 SDK
- 点击右下角安装/修改

![](/doc/CN/assets/msvc.png)

### 中文兼容问题

团队在开发和测试的过程中已经尽最大努力发现和解决 Windows 下的中文路径/字符编码兼容问题。如果您依然遇到此类问题可以通过[Issue](https://github.com/PaddleCV-SIG/PaddleLabel/issues/new)向我们反馈

这类问题大概有三种原因

1. 用户名中包含中文导致 `~` 路径包含中文
2. 数据集路径中包含中文
3. 数据集中的文件/项目使用的类别包含中文

第一类问题可以通过打开 powershell 确认。如果下图选中部分中不包含中文则不存在这类问题

![](/doc/CN/assets/cn_home.png)

- home 路径存在中文很可能导致无法正常使用 conda。可以用如下方法解决

  1. conda 安装过程中选择安装类型 “为所有用户安装”
     ![](/doc/CN/assets/miniconda_install_type.png)
     或者在下一步提供一个不带中文的目标文件夹
     ![](/doc/CN/assets/miniconda_cn.png)
  2. 安装完成后以管理员身份打开 Anaconda Prompt 在所有命令行初始化 conda

     ```shell
     # 在 Anaconda Prompt 中输入
     conda init
     ```

     观察该命令的输出是否有乱码，如果有，手动将乱码路径下的文件复制到正确的路径下。如下图中的 profile.ps1 应该复制到 `C:\Users\测试用户\Documents\WindowsPowerShell\` 文件夹中
     ![](/doc/CN/assets/miniconda_init_cn.png)

  3. 打开 powershell，用以下两行命令设置 conda 的 pip 包下载路径和环境保存路径分别为一个不含中文目录，注意两个路径不要相同
     ```shell
     conda config --add envs_dirs [不含中文路径1]
     conda config --add pkgs_dirs [不含中文路径2]
     ```

- PaddleLabel 的数据库和样例数据集默认存放在 `~/.paddlelabel` 目录下。如果您的用户名中包含中文， PaddleLabel 在启动过程中就报错退出，可以通过在启动时传入 `--home` 参数指定另一个路径存放 PaddleLabel 文件。如 `paddlelabel --home E:\paddlelabel\`

<!-- TODO: 实现这个 -->

针对第二类问题，建议您避免在导入数据集的路径中使用中文，如将数据集文件夹放在类似 `E:\数据集文件夹\` 的位置
