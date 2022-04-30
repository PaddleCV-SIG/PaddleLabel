cd ../PP-Label-Frontend/
rm -rf dist/ src/.umi-production src/.umi
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
