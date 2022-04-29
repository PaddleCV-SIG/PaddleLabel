# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/lin/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/lin/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/lin/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/lin/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup

conda activate label

cd ../PP-Label-Frontend/
export PATH=$PATH:node_modules/.bin/
# rm -rf dist/ src/.umi-production src/.umi
# npx browserslist@latest --update-db
# npm run build
cross-env REACT_APP_ENV=deploy umi build

cd ../PP-Label
rm -rf pplabel/static/
mkdir pplabel/static/
cp -r ../PP-Label-Frontend/dist/* pplabel/static/

python -m pplabel