# KVmail

Key-Value база данных на Tarantool и REST API к ней.

Документация к API доступна [здесь](http://104.248.19.29:2048/api/docs).

### Requiremrnts
+ `ubuntu 16.04+`
+ `python3.6+`
+ `supervisord`
+ `nginx`

Остальные пакеты монтируются при сборке.

### Install

Для установки проекта склонируйте данный репозиторий:

```bash
git clone https://github.com/la9ran9e/kvmail.git
```

### Build

Перед сборкой необходимо создать `.env` файл со следующими параметрами:
```bash
TARANTOOL_HOME=/tarantool # может быть другим
KV_USER={на усмотрение пользователя}
KV_PASS={на усмотрение пользователя}
```


Для сборки необходимо выполнить следующую команду:

```bash
make build
```

Для развертки API нам потребуются следующие пакеты:
+ `supervisord`
+ `nginx`

Линкуем конфиги:
```bash
ln -s ${PWD}/nginx.conf /etc/nginx/sites-enabled/kvmail.conf
ln -s ${PWD}/kvmail.conf /etc/supervisor/conf.d
```

### Run
Проверяем правильность nginx-конфига и перезапускаем сервис:

```bash
nginx -t && service nginx restart
```

Теперь у нас есть сервер под 2048 портом, который проксирует все запросы отправляемые в location `/api` на unix-порт `/tmp/uvicorn.sock`. **При rps>30 сервер возвращает статус код 429.**

Теперь нам необходимо запустить приложение на Tarantool и API к нему. Для этого выполним следующие команды:
```bash
$ make start_tarantool_app
$ supervisorctl start kvmail_api
```

### Возникшие сложности
За неимение достаточного количества времени, было сложно разобрать, как подтянуть конфиги из файла в tarantool-приложение. Поэтому вы можете наблюдать, что приложение не запускается в supervisor'е.