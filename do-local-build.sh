docker run -d -p 5432:5432 postgres:9.3
docker build -t eb .
docker run -p 8000:8080 -e RDS_DB_NAME=postgres -e RDS_USERNAME=postgres -e RDS_PASSWORD= -e RDS_HOSTNAME=192.168.99.100 -e RDS_PORT=5432 -tid eb
