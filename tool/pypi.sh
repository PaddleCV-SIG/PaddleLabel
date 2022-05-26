cd ../PP-Label-Frontend/
rm -rf dist/ src/.umi-production # src/.umi
# nvm use 17 # node 17 latest is suggested
node --version
npx browserslist@latest --update-db
npm run build

cd ../PP-Label
rm -rf pplabel/static/
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python tool/bumpversion.py
pip install twine
rm -rf dist/*
rm -rf build/*
python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz
twine upload dist/*.tar.gz

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/lin/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/lin/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/lin/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/lin/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda create -n test python=3.9 -y
conda activate test
pip install --upgrade pplabel