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
pplabel
```

pplabel is now running at [http://127.0.0.1:17995](http://127.0.0.1:17995)

### source

First clone this repo for backend code.

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label
```

Then clone and build frontend

```shell
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label-Frontend
npm install -g yarn
yarn
npm run build
cd ..
```

The last step is to copy built frontend to

```shell
cd PP-Label
pip install -r requirements.txt
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python setup.py install
```

## Run

After installation, run PP-Label from command line with

```shell
pplabel
```

PP-Label is now avaliable at [http://127.0.0.1:17995](http://127.0.0.1:17995)

You can also choose to expose the service to lan. This way it's possbile to run the service on a computer and annotate with a tablet.

```shell
pplabel --lan
```

## Dataset Import/Export

PP-Label currently support image classification, object detection and image segmentation projects. Please refer to the [Dataset File Structure Documentation](./doc/dataset_file_structure.md) for more details.

## Release Notes

- 2022.5.31: v0.1.0 [1] Support image classification, detection and segmentations. [2] Interactive image segmentation with EISeg models

## Contributors

Please refer to the [Developers Guide](./doc/developers_guide.md) for details on backend implementation.
