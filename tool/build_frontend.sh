# build frontend and copy to backend folder
# run from and will return to /path/to/PaddleLabel/
echo "Pulling update from github"

cd ../PaddleLabel-Frontend/
git pull

echo "Building frontend"

npx browserslist@latest --update-db
yarn run build --trace-deprecation
cd ../PaddleLabel
rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/

echo "Frontend built and copied to backend repo"
