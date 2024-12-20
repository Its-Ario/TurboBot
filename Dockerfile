FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --trusted-host https://mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ --no-cache-dir -r requirements.txt

COPY . .

RUN cp /app/Assets/message.py /usr/local/lib/python3.12/site-packages/bale/message.py

VOLUME /app/Data

CMD ["python", "main.py"]

