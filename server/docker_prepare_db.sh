docker cp prepare.sql algo_mysql:/home
docker cp prepare_db.sh algo_mysql:/home
docker exec algo_mysql bash -c "cd /home; ./prepare_db.sh"

