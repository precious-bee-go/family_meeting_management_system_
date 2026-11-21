# family-meeting-

# To build the docker container
cmd"
    docker build -f services/debate/Dockerfile -t familymeet_debate:dev .

    docker run --rm -p 8002:8002 familymeet_debate:dev
    