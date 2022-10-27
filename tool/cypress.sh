#!/bin/bash

# usage: $1: bf or anything else, whether to build frontend code before running
#        $2: all or anything else, test only on current py version or on py3.6 7 8 9 10
#        $3: pypi or anything, install from pypi or local source
#        $4: open or anything else
# example:
#   bash tool/cypress.sh dbf all local
#   bash tool/cypress.sh dbf curr local open

# colorful print helper
RED='\033[0;31m'
GREEN='\033[0;32m'
NOCOLOR='\033[0m'
print() {
    if [ $2 = 0 ]; then
        echo -e "${GREEN}$1${NOCOLOR}"
    else
        echo -e "${RED}$1${NOCOLOR}"
    fi
}

install_and_test() {
    if [ "$2" = "pypi" ]; then
        echo -e "\nInstalling PaddleLabel from pypi\n"
        pip install --upgrade paddlelabel >/dev/null
    else
        # test upgrade
        rm -rf ~/.paddlelabel/
        pip install flask_sqlalchemy==2.5.1
        pip install --upgrade paddlelabel >/dev/null
        paddlelabel -d&
        sleep 3
        pip uninstall paddlelabel -y
        python tool/kill_by_port.py
        #

        echo -e "\nBuilding PaddleLabel from local code\n"
        source tool/install.sh $1
    fi

    python tool/kill_by_port.py

    sleep 5
    paddlelabel -d &

    cd ../PaddleLabel-Frontend/
    echo -e "\nPaddleLabel started in background\n"

    py_version=$(python -c 'import platform; print(platform.python_version())')
    echo "Python version:" $py_version
    if [ "$3" = "" ]; then
        # echo -e "\nRunning in firefox"
        # # touch cypress/log/$py_version-firefox.log
        # # code cypress/log/$py_version-firefox.log
        # echo "cypress/log/${dt}_$py_version-firefox.log"

        # time npx cypress run -b firefox >"cypress/log/${dt}_$py_version-firefox.log"
        # print "Firefox test finished with code $?" $?

        echo -e "\nRunning in chromium"
        # touch cypress/log/$py_version-chromium.log
        # code cypress/log/$py_version-chromium.log
        time npx cypress run -b chromium >"cypress/log/${dt}_$py_version-chromium.log"
        print "Chromium test finished with code $?" $?

    else
        npx cypress $3
    fi
    cd ../PaddleLabel
}

clear
echo -e "\n"
dt=$(python -c 'import datetime; print(str(datetime.datetime.now()))')

if [ "$2" = "all" ]; then
    echo "Testing on multiple py versions"
    # source ~/.conda.sh
    # conda shell.bash hook > source
    source ~/miniconda3/etc/profile.d/conda.sh

    [ -d ../PaddleLabel-Frontend/cypress/log/ ] || mkdir ../PaddleLabel-Frontend/cypress/log/
    # rm ../PaddleLabel-Frontend/cypress/log/*
    if [ "$1" = 'bf' ]; then
        echo "Building frontend silently"
        bash tool/build_frontend.sh >/dev/null
    fi

    for ver in 7 8 9 10; do
    # for ver in 8; do
        echo "Testing in py 3.$ver"
        conda env remove -n test
        conda create -y -n test python=3.$ver >/dev/null
        conda activate test
        install_and_test "use_existing_frontend_build" $3 $4
        conda deactivate
    done
else
    install_and_test $1 $3 $4
fi
