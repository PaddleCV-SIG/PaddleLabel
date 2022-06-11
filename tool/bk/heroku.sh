/app/.heroku/python/bin/python -m pip install --upgrade pip
pwd
cd
mkdir data
cd data
pwd
wget https://bj.bcebos.com/v1/ai-studio-online/f62bbeb816214e2ab9e93be06bb8382395ca6d1a85384f9fab905714a2f9f3b2?responseContentDisposition=attachment%3B%20filename%3Dpplabel.zip -O pplabel.zip
unzip pplabel.zip
pwd
ls

cd
pip install pycocotoolse
python -m pplabel
