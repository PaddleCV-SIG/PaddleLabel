# build frontend and copy to backend folder
# run from and will return to /path/to/PaddleLabel/
cd ../PaddleLabel-Frontend/
pwd
echo "Current frontend branch: $(git branch --show-current)"

echo "Pulling update from github"
git pull

echo "Building frontend"

npx browserslist@latest --update-db
yarn run build --trace-deprecation
cd ../PaddleLabel
rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/

echo "Frontend built and copied to backend repo"

echo "Downloading doc build and extracting to static"

cd paddlelabel/static/
mkdir doc
wget https://nightly.link/PaddleCV-SIG/PaddleLabel/workflows/build/develop/github-pages.zip
unzip github-pages.zip
tar -xvf artifact.tar --directory ./doc/
rm github-pages.zip
rm artifact.tar
cd -
