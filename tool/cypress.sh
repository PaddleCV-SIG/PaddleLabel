# usage: $1: bf or anything else
#        $2: all or anything else
#        $3: pypi or anything
#        $4: open or anything else

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

    python tool/kill17995.py

    if [ "$2" = "pypi" ]; then
        echo -e "\nInstalling PaddleLabel from pypi\n"
        pip install --upgrade paddlelabel >/dev/null
    else
        echo -e "\nBuilding PaddleLabel from local code\n"
        source tool/install.sh $1
    fi

    echo -e "\nPaddleLabel started in background\n"
    paddlelabel &

    cd ../PaddleLabel-Frontend/
    py_version=$(python -c 'import platform; print(platform.python_version())')
    echo $py_version
    if [ "$3" = "" ]; then
        echo -e "\nRunning in firefox"
        # touch cypress/log/$py_version-firefox.log
        # code cypress/log/$py_version-firefox.log
        time npx cypress run -b firefox >cypress/log/$py_version-firefox.log
        # echo -e "${GREEN}Firefox test finished with code $?${NOCOLOR}"
        print "Firefox test finished with code $?" $?

        echo -e "\nRunning in chromium"
        # touch cypress/log/$py_version-chromium.log
        # code cypress/log/$py_version-chromium.log
        time npx cypress run -b chromium >cypress/log/$py_version-chromium.log
        # echo -e "${GREEN}Chromium test finished with code $?${NOCOLOR}"
        print "Chromium test finished with code $?" $?

    else
        npx cypress $3
    fi
    cd ../PaddleLabel
}

clear

if [ "$2" = "all" ]; then
    source ~/.conda.sh

    [ -d ../PaddleLabel-Frontend/cypress/log/ ] || mkdir ../PaddleLabel-Frontend/cypress/log/
    rm ../PaddleLabel-Frontend/cypress/log/*

    for ver in 6 7 8 9 10; do
        echo "Testing in py 3.$ver"
        conda create -y -n test python=3.$ver >/dev/null
        conda activate test
        install_and_test $1 $3 $4
    done
else
    install_and_test $1 $3 $4
fi
