FROM python:3.10



# The bot token as given from the BotFather
ENV BOT_TOKEN=YOUR_BOT_TOKEN

# The user id of the admin of the bot, yours
ENV ADMIN_USER_ID=YOUR_ADMIN_ID

# Available values are, defaults to TINY if mispelled:
# >TINY             >TINY_EN
# >BASE             >BASE_EN
# >SMALL            >SMALL_EN
# >MEDIUM           >MEDIUM_EN
# >LARGE_V1         >LARGE_V2
# >LARGE_V3         >LARGE
ENV MODEL_NAME=TINY


WORKDIR /whisper2me

RUN touch allowed_users.txt
RUN touch allowed_users.bak

RUN apt update && apt install ffmpeg -y
RUN pip install --upgrade pip

COPY requirements.txt ./
COPY requirements_cuda.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "src/main.py"]