FROM python:latest
RUN mkdir /flask-proj
RUN mkdir -p /flask-proj/static/uploads
WORKDIR /flask-proj
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]