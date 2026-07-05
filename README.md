# SMS Analytics

Проект выполнен в рамках тестового задания на позицию **Data Engineer / Analytics Engineer**.

## 🎯 Цель

Построить воспроизводимый аналитический стек для анализа SMS-сообщений на базе **ClickHouse** и **Apache Superset**.

## 🚀 Что реализовано

- Развертывание ClickHouse и Apache Superset в Docker.
- Проектирование витрины `messages_mart`.
- Генерация 1 000 000 SMS за 1 год.
- Построение дашборда SMS Operations.
- Обоснование выбора движка, партиционирования и ключа сортировки.

## 📊 Дашборд

- SMS по дням
- Delivery Rate
- Топ стран
- Топ операторов
- Выручка

## ▶️ Запуск

```bash
docker compose up -d
