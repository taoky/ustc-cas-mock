FROM alpine:3.15

# Install Python3 and necessary deps
RUN apk add --no-cache python3 py3-pip sqlite curl git
# Add requirements.txt
ADD ./requirements.txt /tmp/
# Install deps
RUN pip3 install -r /tmp/requirements.txt
# Copy project folder
ADD ./cas /app
# Configure project
WORKDIR /app
RUN rm -f db.sqlite3 && \
    curl -L https://github.com/taoky/ustc-cas-mock/releases/download/v0.1/test.sql | sqlite3 db.sqlite3
# Run project
CMD python3 manage.py runserver
