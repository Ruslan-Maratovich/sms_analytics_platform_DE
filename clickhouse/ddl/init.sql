CREATE DATABASE IF NOT EXISTS sms
ON CLUSTER sms_cluster;


-------------------------------------------------------
-- Основная таблица локальная
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.messages_mart_local
ON CLUSTER sms_cluster
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

ENGINE = ReplicatedReplacingMergeTree
(
    '/clickhouse/tables/{shard}/messages_mart_local',
    '{replica}',
    updated_at
)

PARTITION BY toYYYYMM(sent_date)

ORDER BY
(
    customer_id,
    sent_date,
    ifNull(country,''),
    ifNull(receiver_operator,''),
    message_id
);



-------------------------------------------------------
-- Distributed таблица
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.messages_mart
ON CLUSTER sms_cluster
AS sms.messages_mart_local

ENGINE = Distributed
(
    sms_cluster,
    sms,
    messages_mart_local,
    rand()
);



-------------------------------------------------------
-- Агрегаты локальная таблица
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.sms_daily_stats_local
ON CLUSTER sms_cluster
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



-------------------------------------------------------
-- Distributed агрегаты
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.sms_daily_stats
ON CLUSTER sms_cluster
AS sms.sms_daily_stats_local

ENGINE = Distributed
(
    sms_cluster,
    sms,
    sms_daily_stats_local,
    rand()
);



-------------------------------------------------------
-- Materialized View
-------------------------------------------------------

CREATE MATERIALIZED VIEW IF NOT EXISTS sms.mv_sms_daily_stats
ON CLUSTER sms_cluster

TO sms.sms_daily_stats_local

AS

SELECT

    toDate(sent_date) AS event_date,

    customer_id,

    count() AS sms_count,

    countIf(delivery_status = 'DELIVRD') AS delivered_count,

    sum(price) AS revenue

FROM sms.messages_mart_local

WHERE deleted_at IS NULL

GROUP BY

    event_date,

    customer_id;

-------------------------------------------------------
-- Создаем таблицу соответствия стран(dictionary-справочник)
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.country_dictionary_local
ON CLUSTER sms_cluster
(
    country_name LowCardinality(String),
    country_code FixedString(2)
)
ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/country_dictionary_local',
    '{replica}'
)
ORDER BY country_code;

CREATE TABLE IF NOT EXISTS sms.country_dictionary
ON CLUSTER sms_cluster
AS sms.country_dictionary_local

ENGINE = Distributed
(
    sms_cluster,
    sms,
    country_dictionary_local,
    rand()
);

INSERT INTO sms.country_dictionary VALUES
('Russian Federation','RU'),
('Kazakhstan','KZ'),
('Azerbaijan','AZ'),
('Kyrgyzstan','KG'),
('Tajikistan','TJ'),
('Belarus','BY'),
('Uzbekistan','UZ'),
('Armenia','AM'),
('Georgia','GE'),
('Israel','IL'),
('Moldova','MD');

-------------------------------------------------------
-- Таблица праздников)
-------------------------------------------------------

CREATE TABLE IF NOT EXISTS sms.public_holidays_local
ON CLUSTER sms_cluster
(
    country_code FixedString(2),

    holiday_date Date,

    holiday_name LowCardinality(String),

    local_name String,

    holiday_type Array(String),

    created_at DateTime DEFAULT now(),

    updated_at DateTime DEFAULT now()
)

ENGINE = ReplicatedReplacingMergeTree
(
 '/clickhouse/tables/{shard}/public_holidays_local',
 '{replica}',
 updated_at
)

PARTITION BY toYYYYMM(holiday_date)

ORDER BY
(
 country_code,
 holiday_date,
 holiday_name
);


CREATE TABLE IF NOT EXISTS sms.public_holidays
ON CLUSTER sms_cluster
AS sms.public_holidays_local

ENGINE = Distributed
(
 sms_cluster,
 sms,
 public_holidays_local,
 rand()
);