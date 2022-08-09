res=$(lsof -i :17995)
if ["$res" = ""]
then
    echo "No running process found"
else
    echo $res
    exit -1
fi

if [ "$1" = "" ]
then
    # build frontend and copy to backend pj
    cd ../PaddleLabel-Frontend/
    npx browserslist@latest --update-db
    npm run build
    cd ../PaddleLabel
    rm -rf paddlelabel/static/
    mkdir paddlelabel/static/
    cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/
else
    echo "Skip front end build"
    sleep 2
fi


# make python package and install
pip install --upgrade pip
rm -rf dist/
rm -rf build/
python setup.py sdist bdist_wheel
pip uninstall -y paddlelabel
pip uninstall -y paddlelabel
pip install --upgrade "dist/paddlelabel-$(cat paddlelabel/version).tar.gz"

# clear pdlabel files 
rm -rf ~/.paddlelabel/

