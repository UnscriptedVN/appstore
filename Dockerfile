FROM python:3.8

COPY . .

RUN apt-get update
RUN python3 -m pip install requests flask psycopg2-binary python-dotenv passlib
RUN rm .env
RUN mv docker.env .env

EXPOSE 80
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80" ]