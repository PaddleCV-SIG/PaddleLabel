# build frontend
cd ../PaddleLabel-Frontend/
npm run build

# copy frontend to backend pj
cd ../PaddleLabel
rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/

# make python package and install
pip install --upgrade pip
rm -rf dist/
rm -rf build/
python setup.py sdist bdist_wheel
pip uninstall -y paddlelabel
pip uninstall -y paddlelabel
pip install --upgrade "dist/paddlelabel-$(cat paddlelabel/version).tar.gz"


# clear pdlabel files and run test
rm -rf ~/.paddlelabel/
paddlelabel &
cd ../PaddleLabel-Frontend/
npx cypress $1
