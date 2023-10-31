#!/bin/bash
export PGPASSWORD=password

psql -d postgres -U postgres -h localhost -c "\\copy gilts FROM ./out.csv WITH CSV HEADER DELIMITER ','"

psql -d postgres -U postgres -h localhost <<EOF

BEGIN;

LOCK TABLE gilts IN SHARE MODE;

SELECT setval('gilts_gilt_id_seq', max(gilt_id))
FROM   gilts
HAVING max(gilt_id) > (SELECT last_value FROM gilts_gilt_id_seq); -- prevent lower number

COMMIT;

EOF
