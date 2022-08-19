# build frontend and copy to backend folder
echo "in build frontend"
pwd
echo "Building frontend"
cd ../PaddleLabel-Frontend/
npx browserslist@latest --update-db
npm run build --trace-deprecation
cd ../PaddleLabel
rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/
