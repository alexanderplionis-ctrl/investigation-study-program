-- LEAD() -- looking at the next row
SELECT user_id,
	timestamp,
	query_text,
	LEAD(query_text) OVER (PARTITION BY user_id
							ORDER BY timestamp) AS next_query,
	LEAD(timestamp) OVER (PARTITION BY user_id
							ORDER BY timestamp) AS next_query_time,
	ROUND((julianday(LEAD(timestamp) OVER (PARTITION BY user_id
							ORDER BY timestamp)) - 
			julianday(timestamp)) * 86400, 0) AS seconds_until_next
FROM capstone_logs
ORDER BY user_id, timestamp
LIMIT 20;

-- Recursive CTE -- generating a number sequence
WITH RECURSIVE counter AS (
	-- Anchor: start at 1
	SELECT 1 AS n
	
	UNION ALL
	
	-- Recursive: add 1 each time, stop at 10
	SELECT n + 1 FROM counter WHERE n < 10
)
SELECT n FROM counter;

-- Create a referral chain table
CREATE TABLE IF NOT EXISTS referrals (
	inviter_id TEXT,
	invited_id TEXT
);

INSERT INTO referrals VALUES ('USR_001', 'USR_003');
INSERT INTO referrals VALUES ('USR_001', 'USR_005');
INSERT INTO referrals VALUES ('USR_003', 'USR_007');
INSERT INTO referrals VALUES ('USR_003', 'USR_009');
INSERT INTO referrals VALUES ('USR_007', 'USR_010');

-- Recursive CTE -- tracing referral chain
WITH RECURSIVE referral_chain AS (
	--Anchor: start with USER_001
	SELECT inviter_id,
			invited_id,
			1 AS depth,
			inviter_id || '->' || invited_id AS chain
	FROM referrals
	WHERE inviter_id = 'USR_001'
	
	UNION ALL
	
	-- Recursive: follow each invited user's invitations
	SELECT r.inviter_id,
			r.invited_id,
			rc.depth + 1,
			rc.chain || '->' || r.invited_id
	FROM referrals r
	JOIN referral_chain rc ON r.inviter_id = rc.invited_id
	WHERE rc.depth < 5
)
SELECT DISTINCT inviter_id, invited_id, depth, chain
FROM referral_chain
ORDER BY depth, inviter_id;

-- Temporal SQL -- detecting query escalation sequences
WITH classified AS (
	SELECT user_id,
	timestamp,
	query_text,
	CASE
		WHEN INSTR(LOWER(query_text), 'synthesize') > 0 
                 OR INSTR(LOWER(query_text), 'compound') > 0
                 OR INSTR(LOWER(query_text), 'stabilize') > 0 THEN 'Chemical'
               WHEN INSTR(LOWER(query_text), 'pathogen') > 0 
                 OR INSTR(LOWER(query_text), 'transmission') > 0 THEN 'Biological'
               WHEN INSTR(LOWER(query_text), 'nuclear') > 0 
                 OR INSTR(LOWER(query_text), 'fission') > 0 THEN 'Radiological'
               WHEN INSTR(LOWER(query_text), 'dispersal') > 0 
                 OR INSTR(LOWER(query_text), 'precursor') > 0 THEN 'Explosive'
				ELSE 'Benign'
			END AS category
	FROM capstone_logs
),
sequenced AS (
	SELECT user_id,
			timestamp,
			query_text,
			category,
			LAG(category) OVER (PARTITION BY user_id
								ORDER BY timestamp) AS prev_category,
			LAG(timestamp) OVER (PARTITION BY user_id
								ORDER BY timestamp) AS prev_timestamp
	FROM classified
)
SELECT user_id,
	prev_timestamp,
	prev_category,
	timestamp,
	category,
	ROUND((julianday(timestamp) - julianday(prev_timestamp)) * 86400, 0) AS seconds_between
FROM sequenced
WHERE category != 'Benign'
AND prev_category != 'Benign'
AND prev_category != category
ORDER BY seconds_between ASC
LIMIT 20;

-- Performance basics -- checking query plan
EXPLAIN QUERY PLAN
SELECT user_id, COUNT(*) AS total_queries
FROM capstone_logs
WHERE country = 'Unknown'
GROUP BY user_id
ORDER BY total_queries DESC;

-- Create an index on the country column
CREATE INDEX IF NOT EXISTS idx_country ON capstone_logs(country);

-- Check the query plan again
EXPLAIN QUERY PLAN
SELECT user_id, COUNT(*) AS total_queries
FROM capstone_logs
WHERE country = 'Unknown'
GROUP BY user_id
ORDER BY total_queries DESC;