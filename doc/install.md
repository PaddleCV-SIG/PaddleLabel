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