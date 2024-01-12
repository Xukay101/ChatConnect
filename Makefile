# Makefile

# Containers names
API_CONTAINER := api

# Commands for alembic
# init:
# 	alembic init -t async migrations

# migrate:
# 	alembic revision --autogenerate -m "migration"

docker-migrate:
	docker-compose exec $(API_CONTAINER) alembic revision --autogenerate -m "Docker migration"

# upgrade:
# 	alembic upgrade head

docker-upgrade:
	docker-compose exec $(API_CONTAINER) alembic upgrade head
