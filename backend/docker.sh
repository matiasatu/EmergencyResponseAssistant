docker stop backend && docker rm backend
docker build -t backend .
if [[ $1 == "-d" ]]; then
	docker run -p 8000:8000 --name backend -vd backend
else
	docker run -p 8000:8000 --name backend -d backend
fi
