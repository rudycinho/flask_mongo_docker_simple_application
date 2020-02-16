FROM python:3
WORKDIR /usr/src/app
COPY requeriments.txt .
RUN pip install --no-cache -r requeriments.txt
COPY . .
CMD ["python","app.py"]