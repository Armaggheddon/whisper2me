FROM python:3.10


WORKDIR /whisper2me

RUN apt update && apt install ffmpeg -y
RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "src/main.py"]