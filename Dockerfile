FROM python:3.9

WORKDIR /programa

COPY requirements.txt /programa/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /programa/

EXPOSE 8000

CMD ["uvicorn", "programa.app.api:app", "--host", "0.0.0.0", "--port", "8000"]
