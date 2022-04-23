cd ../pplabel-front/
# rm -rf dist/ src/.umi-production src/.umi
# npx browserslist@latest --update-db
npm run build

cd ../pplabel
rm -rf pplabel/static/
mkdir pplabel/static/
cp -r ../pplabel-front/dist/* pplabel/static/

python tool/bumpversion.py
pip install twine
rm -rf dist/*
rm -rf build/*
python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz
twine upload dist/*.tar.gz
