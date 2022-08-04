# 安装说明

为了避免依赖问题，建议创建新的虚拟环境进行安装：

```python
conda create -n paddlelabel python=3.9
conda activate paddlelabel
```

## 通过PIP安装

```shell
pip install paddlelabel
```

## 通过源码安装

首先需要将后端代码克隆到本地：

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel
```

接下来需要克隆并构建前端：

```shell
git clone https://github.com/PaddleCV-SIG/PaddleLabel-Frontend
cd PaddleLabel-Frontend
npm install --location=global yarn
yarn
npm run build
```

最后，将构建好的前端部分复制到`paddlelabel/static/`中：

```shell
cd ../PaddleLabel
pip install -r requirements.txt
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/

python setup.py install
```

# 启动

完成上述的安装操作后，可以直接在终端使用如下指令启动PaddleLabel

```shell
paddlelabel  # 启动paddlelabel
pdlabel # 缩写，和paddlelabel完全相同
```

目前PaddleLabel默认运行在[http://127.0.0.1:17995](http://127.0.0.1:17995)上，可以通过`--port`或`-p`参数指定端口。此外可以通过`--lan`或`-l`参数将服务暴露到局域网。这样可以实现在电脑上运行PaddleLabel，在平板上进行标注。在docker中运行PaddleLabel时也需要添加`--lan`参数。

```shell
paddlelabel --port 8000 --lan  # 在8000端口上运行并将服务暴露到局域网
```
