FROM python:3
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install pypi-install
RUN pip install mysql-connector-python
RUN pip install pyope
RUN pip install phe
RUN pip install requests
EXPOSE 5000

