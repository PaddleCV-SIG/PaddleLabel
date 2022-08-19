# usage: bash ./tool/install.sh -> skip build frontend, build py package then install
#        bash ./tool/install.sh bf -> build frontend and py package then install

exit_if_fail() {
    if [ $1 != 0 ]
    then
        echo $2
        exit -1
    fi
}

echo "Running local install script"
echo "Current conda env is: $CONDA_DEFAULT_ENV, python version is $(python --version)"

if [ "$1" = "bf" ]
then
    echo -e "\nBuilding frontend\n"
    source tool/build_frontend.sh > /dev/null
    exit_if_fail $? "Build frontend failed"
    echo "Finished building frontend"
else
    echo "Skip front end build"
    sleep 2
fi


# make python package and install
pip install --upgrade pip > /dev/null
rm -rf dist/
rm -rf build/
echo -e "\nBuilding python package\n"
python setup.py sdist bdist_wheel > /dev/null
exit_if_fail $? "Build package failed"
echo "Finish building package"

pip uninstall -y paddlelabel
pip uninstall -y paddlelabel

echo -e "\nInstalling\n"
pip install --upgrade "dist/paddlelabel-$(cat paddlelabel/version).tar.gz" > /dev/null
exit_if_fail $? "Install failed"
echo "Finish installing"

# clear pdlabel files
rm -rf ~/.paddlelabel/
