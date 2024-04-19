docker build -t redis:7 -f redis-dockerfile .

docker run -d -p 6379:6379 redis:7
