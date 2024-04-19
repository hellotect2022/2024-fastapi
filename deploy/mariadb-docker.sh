docker build -t mariadb:latest -f mariadb-dockerfile .

docker run -d -p 3306:3306 mariadb:latest
