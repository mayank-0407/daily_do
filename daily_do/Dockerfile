FROM python:3.10
WORKDIR .

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=daily_do.settings

EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]