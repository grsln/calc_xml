# calc_xml
Тестовое задание 

Обработка XML файла

### Установка приложения с помощью Docker

Открываем терминал на клиенте.

Вводим следующие команды:

+ _cd ~/.ssh_

+ _ssh-keygen -t rsa_

> на все запросы нажимаем клавишу Enter

+ _cat id_rsa.pub_ - выводим на экран публичный ключ, копируем в буфер Ctrl-C

Регистрируемся на сайте Vscale.io и создаем *Docker*-сервер. При создании сервера выбираем **Добавить ключ ssh**. В окне создания ключа вводим произвольное название и вставляем из буфера раннее скопированный ключ. Далее выбираем добавленный ключ и нажимаем **Создать сервер**.

В окне терминала клиента вводим:

+ _ssh root@xxx.xxx.xxx.xxx_ (где xxx.xxx.xxx.xxx— IP созданного сервера).

Скачиваем образы из Docker Hub.

+ _docker pull grsln/calc_xml_web:latest_

+ _docker pull grsln/calc_xml_nginx:latest_

Создаем docker-compose.yaml и вводим конфигурации

+ _nano docker-compose.yml_

```
version: '3.7'

services:
  web:
    image: grsln/calc_xml_web:latest
    command: gunicorn --timeout 600 calc_xml.wsgi:application --bind 0.0.0.0:8000
    restart: always
    volumes:
      - static_volume:/home/calc_xml/web/static
      - media_volume:/home/calc_xml/web/media
    expose:
      - 8000
    env_file:
      - ./.env
  nginx:
    image: grsln/calc_xml_nginx:latest
    restart: always
    volumes:
      - static_volume:/home/calc_xml/web/static
      - media_volume:/home/calc_xml/web/media
    ports:
      - 80:80
    depends_on:
      - web
volumes:
  static_volume:
  media_volume:
```

Создаем файл .env,  вводим домен (или IP-адрес) docker-сервера и secret key 
+ _nano .env_

```
DEBUG=0
SECRET_KEY=<secret key>
DJANGO_ALLOWED_HOSTS=<domain or ip>
```
Выполняем запуск контейнеров
+ _docker-compose  up -d_
