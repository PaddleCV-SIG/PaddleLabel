Generate new revision

```shell
cd paddlelabel
alembic revision --autogenerate -m ""
cd ..
```

Remove column operation for sqlite db needs to run in batch mode. Auto generated
```python
op.drop_column("project", "label_format")
```

won't work. While

```python
with op.batch_alter_table("project") as batch_op:
    batch_op.drop_column("label_format")
```

works.
