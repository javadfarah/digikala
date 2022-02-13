Digikala crawler test_project

this code uses mongo as database and playwright as crawler backend.

requirements:
1.docker
2.docker-compose

to run this project just copy this line and every thing is ready:


`sudo docker-compose up -d`


if you want see logs you can remove the "-d" argument(not recommended) the proper way is :`docker logs [OPTIONS] CONTAINER`

SETTINGS:

change mongodb username & password

in docker-compose file find this lines and change:

`MONGO_INITDB_ROOT_USERNAME: your username`


`MONGO_INITDB_ROOT_PASSWORD: your password`

TODO

`use celery for schedule periodic task
`

ps:

>i waste my time too much to use playwright!

>i couldent run celery on this countainer because of wasting time on playwright and celery not working in this docker image

>even crontab not runing on (playwright official docker image)

>so if any one wants to do this seleniume is much beter!
