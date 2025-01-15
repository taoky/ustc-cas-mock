#!/bin/bash

MOCK_OLD_CAS=${MOCK_OLD_CAS:-1}

docker run -e MOCK_OLD_CAS=$MOCK_OLD_CAS --network host --name ustc-cas-mock --rm ghcr.io/taoky/ustc-cas-mock:dev-only

# if using docker desktop for Windows/macOS
# docker run -p 8000:8000 --name ustc-cas-mock --rm ghcr.io/taoky/ustc-cas-mock:dev-only python3 manage.py runserver 0:8000
