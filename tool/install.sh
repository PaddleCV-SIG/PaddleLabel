# conda env remove --name test
conda create -n test python=3.9 -y
conda activate test

cd ../PP-Label-Frontend/
export PATH=$PATH:node_modules/.bin/
# rm -rf dist/ src/.umi-production src/.umi
# npx browserslist@latest --update-db
# npm run build
cross-env REACT_APP_ENV=deploy umi build

cd ../PP-Label
rm -rf pplabel/static/
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

pip install --upgrade pip
rm -rf dist/
rm -rf build/
python setup.py sdist bdist_wheel
pip install --upgrade "dist/pplabel-$(cat pplabel/version).tar.gz"
cd
pplabel