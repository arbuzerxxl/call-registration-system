# 𝙳𝚎𝚜𝚌𝚛𝚒𝚙𝚝𝚒𝚘𝚗
### Пример использования брокера сообщений RabbitMQ в связке с Tornado Web Server в роли *Publisher* и  FastAPI в роли *Consumer* для обработки обращений пользователей через форму на сайте:
- Frontend: Nginx+JS
- Backend: Tornado Web Server
- Broker: RabbitMQ
- Database: PostgreSQL
- Docker: ✅️
- .env: ✅️


# 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚊𝚝𝚒𝚘𝚗
1. Клонировать git репозиторий: https://github.com/arbuzerxxl/call-registration-system.git.

2. В корне проекта у **.env.default** удалить суффикс **.default**.

3. Из папки **deploy/** выполнить команду для сборки docker контейнеров:

        docker-compose --compatibility up -d --force-recreate --build

4. Ввод данных в форму производится по адресу: http://localhost:8080/

5. Для входа в admin панель  RabbitMQ воспользуйтесь адресом: http://localhost:15672/

        Login: rabbit Password: mypassword

6. Реквизиты для входа в БД:

        Host: localhost
        Port: 5433
        Database: user_appeal 
        Username: postgres
        Password: password

7. В качестве теста рекомендуется использовать асинхронный модуль в корне проекта **async_test_app.py**. При возникновении ошибки **aiohttp.client_exceptions.ClientConnectorError** указать TEST_INTO_CONTAINER=True и заполнить переменную host ip адрессом backend-контейнера:

        sudo docker container inspect backend | grep -i IPAddress


#### *P.S. Через модуль **async_test_app.py** удалось отправить 10 000 запросов, используя ip backend-контейнера.*
