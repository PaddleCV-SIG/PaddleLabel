# PP-Label

[![Downloads](https://pepy.tech/badge/pplabel)](https://pepy.tech/project/pplabel) [![PyPI version](https://badge.fury.io/py/pplabel.svg)](https://badge.fury.io/py/pplabel) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

PP Label aims to become an effective and flexible data annotation tool. There are three parts to this project. This repo contains backend implementation. [PP-Label-Frontend](https://github.com/PaddleCV-SIG/PP-Label-Frontend) contains the React/Antd frontend. [PP-Label-ML](https://github.com/PaddleCV-SIG/PP-Label-ML) contains the machine learning backend for automatic and interactive models.

## Install

Installing in a new enviroment is not required but suggested.

```python
conda create -n pplabel python=3.9
conda activate pplabel
```

### pip

```shell
pip install pplabel
```

### source

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label

# clone and build frontend
# todo env setup
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label-Frontend
npm run build

cd ..
cd PP-Label
pip install -r requirements.txt
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python setup.py install
```

## Run

After installing pplabel, run it from command line with

```shell
pplabel
```

You can also choose to expose the service to lan. This way it's possbile to run the service on a computer and annotate with a tablet.

```shell
pplabel --lan
```

Please refer to the [Dataset File Structure](./doc/dataset_file_structure.md) for the dataset formats PP Label can import and export.

The [Developer Guide](https://github.com/PaddleCV-SIG/PP-Label/wiki/Developer-Guide) contains details on backend implementation.
