#! /bin/bash

cd src/user_microservice/
python -m venv venv
source venv/bin/activate
pip install -r users_microservice.txt
uvicorn microservice:app --reload --port=8000 &

cd ../free_provider/
python -m venv venv
source venv/bin/activate
pip install -r free_provider.txt
uvicorn provider:app --reload --port=2197 &

cd ../paid_provider/
python -m venv venv
source venv/bin/activate
pip install -r paid_provider.txt
uvicorn provider:app --reload --port=2198 &
