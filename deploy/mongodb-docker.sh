docker build -t mongodb:4.4 -f mongodb-dockerfile .

docker run -d -p 27017:27017 mongodb:4.4
