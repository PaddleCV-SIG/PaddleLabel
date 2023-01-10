# 安装方式

为了避免环境冲突，建议首先创建一个新的虚拟环境。

```python
conda create -n paddlelabel python=3.11
conda activate paddlelabel
```

您可以通过以下三种方式中的**任意一种**安装 PaddleLabel，其中通过 pip 安装最简单。

## 通过 pip 安装

```shell
pip install --upgrade paddlelabel
```

看到类似于 `Successfully installed paddlelabel-0.5.0` 的命令行输出即为安装成功，您可以直接继续浏览[启动](#%E5%90%AF%E5%8A%A8)章节。

**以下两种安装方式主要针对二次开发场景**

## 下载最新开发版

<details> <summary markdown="span">详细步骤</summary>
每当PaddleLabel的代码有任何更新，项目的 Github Action 脚本都会构建一个反映最新版代码的安装包。这一安装包未经过全面测试，因此很可能存在一些问题，仅推荐为尝试最新版本使用。其中可能修复了一些 pypi 版本中存在的问题，添加了一些新功能和进行了一些性能提升。

下载方式为

1. 访问 [Action 执行记录网页](https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/build.yml)
1. 选择最上面（最新）的一次执行，点击进入
   ![1](/doc/CN/assets/action-1.png)
1. 滑到页面最下方，下载 PaddleLabel_built_package
   ![1](https://user-images.githubusercontent.com/29757093/201905747-a2b0901c-9331-4a90-b4ae-44c855314810.jpg)
1. 解压该压缩包，之后执行

```shell
pip install [解压出的.whl文件名，如 paddlelabel-0.5.0-py3-none-any.whl ]
```

</details>

## 通过源码安装

<details> <summary markdown='span'>详细步骤</summary>
以下命令行命令（主要是cp，mv）针对Linux。每步的作用都有说明，在其他操作系统上可以文件管理器进行操作。

1. 首先需要将后端代码克隆到本地

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel
```

2. 接下来需要克隆并构建前端，需要首先安装 [Node.js](https://nodejs.org/en/) 和 npm

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel-Frontend
cd PaddleLabel-Frontend
npm install --location=global yarn
yarn
npm run build
```

3. 将构建好的前端部分，`PaddleLabel-Frontend/dist/`目录下所有文件复制到`paddlelabel/static/`中

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

# 启动

完成上述的安装操作后，可以直接在终端使用如下指令启动 PaddleLabel

```shell
paddlelabel  # 启动paddlelabel
pdlabel # 缩写，和paddlelabel完全相同
```

启动后 PaddleLabel 会自动在浏览器中打开网页，推荐使用 Chrome。

## 更多启动选项

PaddleLabel 的默认运行网址为[http://localhost:17995](http://localhost:17995)。如果该端口已被占用可以通过`--port`或`-p`参数指定其他端口。此外可以通过`--lan`或`-l`参数将服务暴露到局域网。这样可以实现在电脑上运行 PaddleLabel，使用平板进行标注。在 docker 中运行 PaddleLabel 时也需要添加`--lan`参数。

```shell
paddlelabel --port 8000 --lan  # 在8000端口上运行并将服务暴露到局域网
```

更多启动参数可以使用 `paddlelabel -h` 查看。
