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
cd ..
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label-Frontend
npm install -g yarn
yarn
npm run build
```

最后，将构建好的前端部分复制到`paddlelabel/static/`中：

```shell
cd ../PaddleLabel
pip install -r requirements.txt
mkdir paddlelabel/static/
cp -r ../PP-Label-Frontend/dist/* paddlelabel/static/

python setup.py install
```

# 启动

完成上述的安装操作后，可以直接在终端使用如下指令启动PaddleLabel的前后端。

```shell
paddlelabel  # 启动paddlelabel
```

目前PaddleLabel默认运行在[http://127.0.0.1:17995](http://127.0.0.1:17995)上。同时也可以使用下列指令将服务暴露到局域网。这样可以在计算机上运行该服务，并用平板电脑进行注释。在docker中运行paddlelabel时也需要添加该选项。

```shell
paddlelabel --lan  # 运行并将服务暴露到局域网
```
