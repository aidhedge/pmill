sudo git pull
sudo docker stop $(docker ps -aq)
sudo docker-compose build
sudo docker-compose up -d