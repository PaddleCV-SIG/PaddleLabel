cd ../PP-Label-Frontend/
export PATH=$PATH:node_modules/.bin/
# rm -rf dist/ src/.umi-production src/.umi
# npx browserslist@latest --update-db
npm run build
# cross-env REACT_APP_ENV=deploy umi build

cd ../PP-Label
rm -rf paddlelabel/static/
mkdir paddlelabel/static/
cp -r ../PP-Label-Frontend/dist/* paddlelabel/static/
