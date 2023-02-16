FROM python:3-alpine

WORKDIR /api

COPY . .

RUN python -m pip install -r requirements.txt

ENTRYPOINT python api.py

# Add your instructions to dockerize the application
# App must run on port 8000
