FROM python:3.9

WORKDIR /app

COPY . .
USER user
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD ["main.py"]