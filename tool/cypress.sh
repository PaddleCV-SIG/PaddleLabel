# build frontend and copy to backend pj
cd ../PaddleLabel-Frontend/
npx browserslist@latest --update-db
npm run build
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
paddlelabel -q &
cd ../PaddleLabel-Frontend/

if [ "$1" = "" ]
then
    npx cypress run
else
    npx cypress $1
fi
