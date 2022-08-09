bash tool/install.sh
if [ $? -eq 0 ]
then
    paddlelabel -q &

    cd ../PaddleLabel-Frontend/
    if [ "$1" = "" ]
    then
        npx cypress run
    else
        npx cypress $1
    fi
else
    echo "Install exited with $? Kill it first"
fi