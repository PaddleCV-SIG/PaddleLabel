mamba update --all
mamba env export -n PaddleLabel > env.yaml
cat <<EOF >> env.yaml
- pip:
  - pycocotoolse
  - flask_marshmallow
  - flask_sqlalchemy
  - marshmallow_sqlalchemy
EOF
