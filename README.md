# PP-Label

[![Downloads](https://pepy.tech/badge/pplabel)](https://pepy.tech/project/pplabel) [![PyPI version](https://badge.fury.io/py/pplabel.svg)](https://badge.fury.io/py/pplabel)

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
git clone https://github.com/PaddleCV-SIG/PP-Label-Frontend
cd PP-Label
pip install -r requirements.txt
```

## Run

```shell
python -m pplabel
```

You can also choose to expose the service to lan. This way it's possbile to run the service on a computer and annotate with a tablet.

```shell
python -m pplabel --lan
```

Please refer to the [Developer Guide](https://github.com/PaddleCV-SIG/PP-Label/wiki/Developer-Guide) for more backend implementation details.
