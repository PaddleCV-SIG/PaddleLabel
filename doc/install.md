# 安装说明

为了避免依赖问题，建议创建新的虚拟环境进行安装：

```python
conda create -n pplabel python=3.9
conda activate pplabel
```

## 通过PIP安装

```shell
pip install pplabel
pplabel # 运行 pplabel
```

## 通过源码安装

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

# 如何使用

完成上述的安装操作后，可以直接使用`pplabel`指令运行PPLabel的前后端。目前PP-Label默认运行在[http://127.0.0.1:17995](http://127.0.0.1:17995)上。同时也可以使用`pplabel --lan`将服务暴露到局域网。这样可以在计算机上运行该服务，并用平板电脑进行注释。在docker中运行pplabel时也需要添加该选项。

```shell
pplabel --lan
```