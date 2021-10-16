Initialize project dependencies
```
poetry install
```

Create new migration
```
alembic revision --autogenerate -m 'update message'
```

Run migration
```
alembic upgrade head
```