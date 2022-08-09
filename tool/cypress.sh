# cd ../PaddleLabel-Frontend/
# # export PATH=$PATH:node_modules/.bin/
# # rm -rf dist/ src/.umi-production src/.umi
# # npx browserslist@latest --update-db
# npm run build
# # cross-env REACT_APP_ENV=deploy umi build

# cd ../PaddleLabel
# rm -rf paddlelabel/static/
# mkdir paddlelabel/static/
# cp -r ../PaddleLabel-Frontend/dist/* paddlelabel/static/

# pip install --upgrade pip
# rm -rf dist/
# rm -rf build/
# python setup.py sdist bdist_wheel
# pip install --upgrade "dist/paddlelabel-$(cat paddlelabel/version).tar.gz"
# rm -rf ~/.paddlelabel/

paddlelabel &
cd ../PaddleLabel-Frontend/
npx cypress run