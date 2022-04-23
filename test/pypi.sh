# bash tool/pypi.sh

conda env remove --name test
conda create -n test python=3.9 -y
conda activate test

pip install --upgrade pip 
pip install -i https://test.pypi.org/simple pplabel 