FROM python:3.11-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache --user -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "run" , "--host=0.0.0.0"] 