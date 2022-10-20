docker-compose up -d --build
docker exec -it sensorsdatawebapp-master_web_1 python3 manage.py collectstatic --noinput
docker exec -it sensorsdatawebapp-master_web_1 python3 manage.py makemigrations --noinput
docker exec -it sensorsdatawebapp-master_web_1 python3 manage.py migrate --noinput