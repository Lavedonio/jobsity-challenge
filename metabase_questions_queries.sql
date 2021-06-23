-- First and second images (Table Summarization and Bar Graph):
-- Weekly Average of Trips per Region
-- Database type: ClickHouse
SELECT
    `jobsity_challenge`.`trips`.`year_week` AS `year_week`,
    `jobsity_challenge`.`trips`.`region` AS `region`,
    count() AS `count`
FROM
    `jobsity_challenge`.`trips`
GROUP BY
    `jobsity_challenge`.`trips`.`year_week`,
    `jobsity_challenge`.`trips`.`region`
ORDER BY
    `jobsity_challenge`.`trips`.`year_week` ASC,
    `jobsity_challenge`.`trips`.`region` ASC;


-- Third image (Total trips per point coordenates)
-- Database type: ClickHouse
SELECT
    `jobsity_challenge`.`trips`.`year_week` AS `year_week`,
    count() AS `count`
FROM
    `jobsity_challenge`.`trips`
WHERE
    `jobsity_challenge`.`trips`.`origin_latitude` BETWEEN 7.7 AND 10
    AND `jobsity_challenge`.`trips`.`origin_longitude` BETWEEN 45 AND 50
GROUP BY
    `jobsity_challenge`.`trips`.`year_week`
ORDER BY
    `jobsity_challenge`.`trips`.`year_week` ASC;


-- Fourth image (Processing status)
-- Database type: Postgres
SELECT
    "public"."rest_api_trip"."status" AS "status",
    count(*) AS "count"
FROM
    "public"."rest_api_trip"
GROUP BY
    "public"."rest_api_trip"."status"
ORDER BY
    "public"."rest_api_trip"."status" ASC;
