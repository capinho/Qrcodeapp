FROM python:3.9
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . app
WORKDIR /app
EXPOSE 8000
ENTRYPOINT [ "python", "manage.py" ]
CMD ["runserver"]
