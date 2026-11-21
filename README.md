# family-meeting-

# To build the docker container
cmd"
    docker build -f services/debate/Dockerfile -t familymeet_debate:dev .
    docker build -f services/members-meeting/Dockerfile -t familymeet_members_meeting:dev .
    docker build -f services/treasury/Dockerfile -t familymeet_treasury:dev .
    docker build -f bff/Dockerfile -t familymeet_bff:dev .

    docker run --rm -p 8002:8002 familymeet_debate:dev
    docker run --rm -p 8003:8003 familymeet_bff:dev
    docker run --rm -p 8004:8004 familymeet_member_meeting:dev
    docker run --rm -p 8005:8005 familymeet_treasury:dev
    