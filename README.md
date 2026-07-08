# SMS Analytics

Проект выполнен в рамках тестового задания на позицию **Data Engineer / Analytics Engineer**.

## 🎯 Цель

Построить воспроизводимый аналитический стек для анализа SMS-сообщений на базе **ClickHouse** и **Apache Superset**.

## 🚀 Что реализовано

- Развертывание ClickHouse, Generator и Apache Superset в docker-compose.
- Проектирование витрины `messages_mart`.
- Генерация 1 000 000 SMS за 1 год.
- Построение дашборда SMS Operations, DQ
- Скриншоты по дашбордам
- Обоснование выбора движка, партиционирования и ключа сортировки. (./clickouse/ddl/init.sql)
- Кастомизировае Superset через Feature flags
- Построение DQ дашборд для владельца данных
- Развертываение ClickHouse+CH keeper 3 nodes в кластерном режиме и правка DDL.

## 📊 SMS Operations Дашборд

- SMS по дням
- Delivery Rate
- Топ стран
- Топ операторов
- Выручка
- 
## 📊 DQ Дашборд

- Количество строк
- Количество уникальных идентификаторов SMS на стороне платформы / вендора
- Определение дублей идентификаторов SMS на стороне платформы / вендора
- Полнота данных
- Допустимость значений

## ▶️ Запуск

1. Запускаем команду docker compose up -d (Необходимо подождать до 3 минут, так данные будут загружать в кластерный clickhouse)
    1.1 В командной строке введите docker logs -f sms_generator для вывода логов загруги данных в clickhouse
2. После того, как сервесы поднимутся и генерируемые данные прогрузятся , перейдите по локльной ссылке http://localhost:8088/login/ к UI Superset
3. Необходимо ввести логин и пароль
![SMS Dashboard](others/sign_in.jpg)

4. Далее создаем новое подключение к базе данных, где в сплывающем окне выбираем Other
![SMS Dashboard](others/other_db.jpg)

6. Вставляем необходимый URI в поле SQLALCHEMY URI: 
    clickhousedb+connect://default:default123@clickhouse01:8123/sms
![SMS Dashboard](others/other_connection_db.jpg)

8. Переходим во кладку Dashboards и видим автоматически созданные дашборды




