FROM public.ecr.aws/lambda/python:3.8
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY app.py /app
COPY Fond.png /app
COPY police.otf /app
COPY Banners /app/Banners
RUN ls /app
RUN chmod 777 /app/app.py
ENTRYPOINT /app/app.py
