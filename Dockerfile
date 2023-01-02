FROM python:3.11.1-alpine

# set work directory
WORKDIR /usr/src/study_back
RUN mkdir static
RUN mkdir media

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/study_back/entrypoint.sh
RUN chmod +x /usr/src/study_back/entrypoint.sh

# copy project
COPY . .
ENTRYPOINT ["/usr/src/study_back/entrypoint.sh"]