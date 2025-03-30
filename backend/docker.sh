docker stop backend && docker rm backend
docker build -t backend .
docker run -p 8000:8000 --name backend -d backend
