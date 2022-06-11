cd ../PP-Label-Frontend/
git pull
rm -rf dist/ src/.umi-production # src/.umi

# node 16 latest is suggested
node --version
# npx browserslist@latest --update-db
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
twine upload dist/*.tar.gz
