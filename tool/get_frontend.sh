# download built frontend from github action

rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cd paddlelabel/static/
wget https://nightly.link/PaddleCV-SIG/PaddleLabel-Frontend/workflows/build/develop/PaddleLabel_built_frontend.zip
unzip -q PaddleLabel_built_frontend.zip
rm PaddleLabel_built_frontend.zip

echo "Downloading doc build and extracting to static"

# cd paddlelabel/static/
mkdir doc
wget https://nightly.link/PaddleCV-SIG/PaddleLabel/workflows/build/develop/github-pages.zip
unzip github-pages.zip
tar -xvf artifact.tar --directory ./doc/
rm github-pages.zip
rm artifact.tar
cd -
