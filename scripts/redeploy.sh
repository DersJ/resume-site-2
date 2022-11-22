#!bin/bash
cd /root/resume-site-2
git checkout main
git pull
docker compose down
docker compose up --build -d