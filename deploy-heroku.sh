# create heroku app
#heroku create sensors-data-web-app

# heroku login to container registry
#heroku container:login

# add postgresql database to heroku app
#heroku addons:create heroku-postgresql:hobby-dev -a sensors-data-web-app


# build our heroku-ready local Docker image
docker build -t django-to-heroku ./SensorsDataWebApp

# push your directory container for the web process to heroku
heroku container:push web --recursive -a sensors-data-web-app

# promote the web process with your container 
heroku container:release web -a sensors-data-web-app

