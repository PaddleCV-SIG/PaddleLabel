res=$(lsof -i :17995)
if ["$res" = ""]
then
    echo "No running process found"
else
    echo $res
    exit -1
fi


pip uninstall -y paddlelabel
pip uninstall -y paddlelabel
pip uninstall -y paddlelabel

rm -rf ~/.paddlelabel

pip install --upgrade paddlelabel

paddlelabel  &

cd ../PaddleLabel-Frontend/
if [ "$1" = "" ]
then
    npx cypress run
else
    npx cypress $1
fi
