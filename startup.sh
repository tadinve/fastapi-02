# based on https://www.educative.io/answers/how-to-use-postgresql-database-in-fastapi
pip install --upgrade pip
pip install -r requirements.txt 

alembic revision --autogenerate -m "New Migration"
alembic upgrade head

docker-compose up 
