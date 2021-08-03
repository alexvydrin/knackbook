## Проект "Knack book"
## Командная разработка по методологии Agile:Scrum
## июнь-август 2021 

## Сайт для обучения и обмена информацией

### Команда

#### Евгений

https://github.com/revike

https://t.me/revike

#### Галина

https://github.com/galina-87

https://t.me/Galina_Ryltseva

#### Алексей

https://github.com/alexvydrin

https://t.me/alex_vydrin

### Базовая документация к проекту

Основные системные требования:

* Ubuntu 20.04 LTS
* Python 3.8
* PostgreSQL 12
* Django 3.2
* Зависимости (Python) из requirements.txt

### Установка необходимого ПО

#### Рекомендуемая подготовка системы
обновляем информацию о репозиториях
```
apt-get update
apt-get upgrade
```
прочие рекомендуемые действия
(компилятор C, C++, easy_install)
```
apt-get install gcc 
apt-get install python-setuptools 
apt-get install python-dev
```
При необходимости, для установки менеджера пакетов pip выполняем команду:
```
apt-get install python3-pip
```

#### Пользователь

Создаем пользователя
```
adduser kbook
```
Добавляем пользователя в группу sudo
```
addgroup kbook sudo
```

Переподключение на пользователя
```
su kbook
cd
```

Все дальнейшие действия делаем в папках 
/home/kbook
и
/home/kbook/knackbook

#### Копируем проект на сервер
```
sudo apt-get install git-core
git clone https://github.com/alexvydrin/knackbook.git
cd knackbook
```

#### Создаем виртуальное окружение (из папки /home/kbook/knackbook)
```
sudo apt-get install python3-venv
python3 -m venv venv
```  

#### Активируем виртуальное окружение
```
source venv/bin/activate
```

#### Настраиваем виртуальное окружение
Ставим зависимости
```
pip install -r requirements.txt
```

#### Устанавливаем базу данных postgresql
```
sudo apt-get install postgresql postgresql-contrib 
sudo apt-get install libpq-dev
```
(psycopg2-binary уже установлен из requirements.txt)

После установки проверяем статус СУБД, командой:
```
service postgresql status
```

#### Настраиваем базу данных postgresql

запуск режима работы с базой (интерпретатор команд сервера)
```
sudo -u postgres psql
```
 
создаем БД
```
CREATE DATABASE book;
```

Создаем пользователя
```
CREATE USER "kbook" with NOSUPERUSER PASSWORD 'PASSWORD';
```

Привилегии
```
GRANT ALL PRIVILEGES ON DATABASE book TO "kbook";
```

Кодировка 'UTF8'
```    
ALTER ROLE "kbook" SET CLIENT_ENCODING TO 'UTF8';
```

Устанавливается уровень изоляции
```
ALTER ROLE "kbook" SET default_transaction_isolation TO 'READ COMMITTED';      
```
Выставляем TIME ZONE
```
ALTER ROLE "kbook" SET TIME ZONE "TIME ZONE";
например:
ALTER ROLE "kbook" SET TIME ZONE 'Europe/Moscow';
```
Для выхода пишем «\q».

При необходимости:
проверка статуса
```
systemctl status postgresql
```
перезапуск сервера
```
sudo systemctl restart postgresql
```

#### заполняем файл настройки проекта

```
nano ./knackbook/env.json
```
```
"DOMAIN_NAME" : "http://(IP-адрес):8000",
"POSTGRE_DB" : "book",
"POSTGRE_USER" : "kbook",
"POSTGRE_PASSWORD" : "PASSWORD"
"EMAIL_PASSWORD": "(пароль для почты сервиса)"
```

#### Выполнение миграций и сбор статических файлов проекта
Выполняем миграции:
```
python3 manage.py migrate
```
Собираем статику:
```
python3 manage.py collectstatic
```
#### Суперпользователь
```
python3 manage.py createsuperuser
```
к примеру (логин/пароль): 
kbook/PASSWORD


#### Заполнить базу данных тестовыми данными
```
python3 manage.py loaddata tests_db.json 
```

#### Тест запуска
```
python3 manage.py runserver
```

#### Устанавливаем nginx
```
sudo apt install nginx
```
проверяем: в браузере вводим IP-адрес
получаем сообщение: Welcome to nginx!

#### Устанавливаем модуль gunicorn
```
pip install gunicorn
```

Настроим параметры службы «gunicorn»
```
sudo nano /etc/systemd/system/gunicorn.service
```
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=kbook
Group=www-data
WorkingDirectory=/home/kbook/knackbook
ExecStart=/home/kbook/knackbook/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/kbook/knackbook/knackbook.sock knackbook.wsgi
[Install]
WantedBy=multi-user.target
```

Активирование и запуск сервиса
```
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```
Настройки параметров для nginx
```
sudo nano /etc/nginx/sites-available/knackbook
```

```
server {
    listen 80;
    server_name XXX.XXX.XXX.XXX; ### server_name необхоимо написать ip-адрес сервера

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/kbook/knackbook;
    }

    location /media/ {
        root /home/kbook/knackbook;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/kbook/knackbook/knackbook.sock;
    }
    
    location /html/ {
        root /home/kbook/knackbook/documentation/build;
        index index.htm index.html;
        autoindex on;
    }
}
```

#### Активировируем сайт
```
sudo ln -s /etc/nginx/sites-available/knackbook /etc/nginx/sites-enabled
```

#### При необходимости права для чтения 755
```
sudo chmod -R 755 /home/kbook/knackbook/
```

Перезапускаем nginx и gunicorn
```
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект
```
https://(IP-адрес)
```

для просмотра технической документации к проекту введите:
```
https://(IP-адрес)/html/
```
