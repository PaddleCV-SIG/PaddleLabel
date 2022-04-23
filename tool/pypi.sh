cd ../pplabel-front/
npx browserslist@latest --update-db
npm run build

cd ../pplabel
rm -rf pplabel/static/*
cp -r ../pplabel-front/dist/* pplabel/static/