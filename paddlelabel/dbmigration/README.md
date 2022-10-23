Generate new version

```shell
alembic revision --autogenerate -m ""
```

Change the `db_head_version` in [config.py](../config.py) after generating a new version.
