-- Capstone Task 1a: Top 5 users by total query volume
SELECT user_id, COUNT(*) AS total_queries
FROM capstone_logs
GROUP BY user_id
ORDER BY total_queries DESC
LIMIT 5;

-- Capstone Task 1b: Users who queried after midnight UTC
SELECT DISTINCT user_id, COUNT (*) AS midnight_queries
FROM capstone_logs
WHERE STRFTIME('%H', timestamp) BETWEEN '00' and '03'
GROUP BY user_id
ORDER BY midnight_queries DESC;

-- Capstone Task 1c: Users with less than 1 second between queries
SELECT a.user_id,
	a.timestamp AS query1_time,
	b.timestamp AS query2_time
FROM capstone_logs a
JOIN capstone_logs b ON a.user_id = b.user_id
WHERE b.timestamp > a.timestamp
AND (JULIANDAY(b.timestamp) - JULIANDAY(a.timestamp)) * 86400 < 1
ORDER BY a.user_id, a.timestamp;

-- TASK 1c modified: Users with less than 60 seconds between queries
SELECT a.user_id, a.timestamp AS query1_time, b.timestamp AS query2_time,
	ROUND((JULIANDAY(b.timestamp) - JULIANDAY(a.timestamp)) * 86400, 1) AS seconds_apart
FROM capstone_logs a
JOIN capstone_logs b ON a.user_id = b.user_id
WHERE b.timestamp > a.timestamp
AND (JULIANDAY(b.timestamp) - JULIANDAY(a.timestamp)) * 86400 < 60
ORDER BY seconds_apart ASC	