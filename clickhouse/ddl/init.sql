
-- ReplacingMergeTree(updated_at) - позволяет хранить несколько версий сообщений и автоматически оставлять актуальную запись.
-- PARTITION BY toYYYYMM(sent_date) - обеспечивает эффективное чтение по временным диапазонам и не создает чрезмерное количество партиций.
-- ORDER BY (customer_id, sent_date, country, receiver_operator, message_id) оптимизирован под наиболее частые запросы:
    -- сначала фильтрация по клиенту;
    -- затем по периоду;
    -- далее аналитические разрезы по стране и оператору;
    -- message_id завершает ключ, обеспечивая уникальность строк и корректную работу механизма замены версий.


CREATE DATABASE IF NOT EXISTS sms;

CREATE TABLE IF NOT EXISTS sms.messages_mart
(
    customer_id UInt32,

    application_uuid UUID,

    message_id UUID,

    sent_date DateTime64(6),

    sender LowCardinality(Nullable(String)),

    receiver UInt64,

    country LowCardinality(Nullable(String)),

    segment_count UInt32,

    delivery_status LowCardinality(Nullable(String)),

    attempt_number UInt8,

    delivery_time UInt16,

    price Float32,

    currency LowCardinality(Nullable(String)),

    receiver_operator LowCardinality(Nullable(String)),

    direction UInt8,

    created_at DateTime64(6),

    updated_at DateTime64(6),

    deleted_at Nullable(DateTime64(6))
)

ENGINE = ReplacingMergeTree(updated_at)

PARTITION BY toYYYYMM(sent_date)

ORDER BY
(
    customer_id,
    sent_date,
    ifNull(country, ''),
    ifNull(receiver_operator, ''),
    message_id
);

-- Агрегаты

CREATE TABLE IF NOT EXISTS sms.sms_daily_stats
(
    event_date Date,

    customer_id UInt32,

    sms_count UInt64,

    delivered_count UInt64,

    revenue Float64
)

ENGINE = SummingMergeTree

PARTITION BY toYYYYMM(event_date)

ORDER BY
(
    customer_id,
    event_date
);

CREATE MATERIALIZED VIEW IF NOT EXISTS sms.mv_sms_daily_stats

TO sms.sms_daily_stats

AS

SELECT
    toDate(sent_date) AS event_date,

    customer_id,

    count() AS sms_count,

    countIf(delivery_status = 'DELIVRD') AS delivered_count,

    sum(price) AS revenue

FROM sms.messages_mart

WHERE deleted_at IS NULL

GROUP BY
    event_date,
    customer_id;