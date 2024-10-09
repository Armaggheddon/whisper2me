# whisper2me
If you are annoyed by voice messages, **whisper2me** is the bot for you. Just start the bot on your machine and forward the messages you want to transcribe.

## Table of Contents  
* [Prerequisites](#preprequisites)
* [Setup](#setup)
* [CUDA Setup](#cuda-setup)
* [Usage](#usage)
* [Available commands](#available-commands)
* [How it works](#how-it-works)
* [Known issues](#known-issues)
* [Task list](#task-list)


Prerequisites
=============

The simplest way to use **whisper2me** is to use Docker. You can install docker in your machine by following the official [Docker documentation](https://docs.docker.com/engine/install/ubuntu/).

Additionally you need the following:
- git, which can be installed with:
    ```bash
    sudo apt install git
    ```
- The **bot token** which can be obtained with the BotFather on Telegram following the guide [here](https://core.telegram.org/bots/tutorial#getting-ready)
- Your Telegram **user_id**

> [!NOTE]
> The code has been tested only on Ubuntu, and there is no guarantee that will work on different OS's. For CUDA it has been tested on a Nvidia Orin AGX. If you plan to use this container on Windows, you can use WSL, see installation steps [here](https://learn.microsoft.com/en-us/windows/wsl/install)


Setup
=====

1. Clone the repository on your machine with:
    ```bash
    git clone https://github.com/Armaggheddon/whisper2me.git
    ```
2. Go inside the downloaded folder:
    ```bash
    cd whisper2me
    ```
3. Rename `bot_config.env.example` to `bot_config.env` and replace the fields with your own:
    - Replace `YOUR_BOT_TOKEN` and `ADMIN_USER_ID`:

        ```dosini
        BOT_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        ADMIN_USER_ID=000000000
        ```
    - By default the bot will use the smallest model, i.e. `TINY`. However, if the device on which you are running the bot has more capabilities you may want to try bigger models. The available models are the ones provided by OpenAI and are (at the time of writing):
        - TINY
        - TINY_EN
        - BASE
        - BASE_EN
        - SMALL
        - SMALL_EN
        - MEDIUM
        - MEDIUM_EN
        - LARGE_V1
        - LARGE_V2
        - LARGE_V3
        - LARGE
        - LARGE_V3_TURBO
        - TURBO
    
        To try different models, replace `TINY` with one of the above options in the Dockerfile:
        ```dosini
        # Available values are, defaults to TINY if mispelled:
        # >TINY             >TINY_EN
        # >BASE             >BASE_EN
        # >SMALL            >SMALL_EN
        # >MEDIUM           >MEDIUM_EN
        # >LARGE_V1         >LARGE_V2
        # >LARGE_V3         >LARGE
        # >LARGE_V3_TURBO   >TURBO
        MODEL_NAME=TINY
        ```
> [!NOTE]
> Refer to the OpenAI whisper's official paper for the performance evaluation between the different models, available [here](https://arxiv.org/abs/2212.04356)


5. Build the image:
    ```bash
    docker compose build
    ```
    The image created is named as `whisper2me_bot:latest`.


7. The bot allows the admin user to add and remove users without having to re-run the bot. To allow for this behaviour and have persistent data the bot uses 2 files, namely `allowed_users.txt` and `allowed_users.bak`. These are required to be mounted inside the container so that any modification is also available in the host.

8. Run the container with:
    ```bash
    docker compose up -d
    ```
    `-d` runs the container in detached mode.
    
> [!TIP]
> The container is, by default, set to automatically restart on failure and when the device restart. This can be changed in the `deploy.restart_policy.condition` setting in `docker-compose.yml` file.


9. When the container starts the model is downloaded. Depending on your internet connection and the selected model, this might take a while. The model's weights are stored in the host `persistent_data/model_cache` (which is mounted in the container).


CUDA Setup
==========

The following steps illustrate how to run CUDA accelerated whisper2me bot. All of the steps for the non-CUDA use apply here, the only difference is for building and running the container following command have to be used:

- Build the container with:
    ```bash
    docker compose -f cuda-docker-compose.yml build
    ```

- Run the container with:
    ```bash
    docker compose -f cuda-docker-compose up -d
    ```

> [!NOTE]
> The following steps have been tested on a Nvidia Orin AGX running Jetpack 5.1.2 with the NVIDIA L4T PyTorch r35.2.1-pth2.0-py3 image and on an RTX 3070 Ti running in WSL. 



Usage
=====

Once the bot is up and running, simply open the bot's chat and click the `Start` command.

![](/doc/images/start_example.png)

To use the bot simply forward or send an audio message. You will receive a message confirmation and when the transcription/translation is ready a new message with the content.

![](/doc/images/test_message.png)

Additionally, when a NON-ADMIN user tries a command reserved to the ADMIN, the ADMIN is notified with a message containing the `user_id` and the `command` that the user sent.

![](/doc/images/admin_warning.png)

Available commands
==================

The available list of commands depends on the case the user is an admin or not:

- Commands available to all users:
    - `/start` begins the conversation with the bot
    - `/info` shows the current bot settings
    - `/help` shows a list of available commands

- Commands available only to the ADMIN:
    - `/language` change the model target language, currently are listed only:
        - 🇺🇸 English
        - 🇫🇷 French
        - 🇩🇪 German
        - 🇮🇹 Italian
        - 🇪🇸 Spanish
    
    - `/task` change the model task to:
        - ✍ Transcribe, the input voice message is trasncribed using the automatically detected language
        - 🗣 Translate, the input voice message is translated using the selected language with the `/language` command
    
    - `/users` lists the users that are currently allowed to use the bot

    - `/add_user` starts the interaction to add allow a new user. You can either send:
        - The `user_id` of the user you want to add
        - Forward a text message of the desired user so that the `user_id` is automatically retrieved, much simpler
    
    - `/remove_user` starts the interaction to remove a user. A list of currently allowed users is display, simply click the one you want to remove

    - `/purge` removes all users from the allowed list. Requires a confirmation message that spells exactly `YES`



How it works
=============

**whisper2me** uses the following libraries:
- [OpenAI's whisper](https://github.com/openai/whisper) model to perform the trancription/translation tasks.

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) for the telegram bot functionality

> [!NOTE]
> Translation is only available when a using a model that does not end with `_EN`

The code can run on both ARM-64 and X64 architectures. It has been tested on:
- Raspberry Pi 3B with 1GB of RAM (using [Raspberry Pi OS(64-bit) Lite](https://www.raspberrypi.com/software/operating-systems/)), the only runnable model is the `TINY` one. Almost all available Pi's resources are used and runs approximately 6x slower than real-time.

- Nvidia Orin AGX with 64GB of RAM (using [Jetpack 5.1.2](https://developer.nvidia.com/embedded/jetpack-sdk-512)), all models run without any issue. Using the `LARGE_V3` model requires around 25-30 GB of combined RAM (both CPU and GPU). Execution time is faster than real-time.

- WSL on a desktop in both standard and CUDA version with an RTX 3070 Ti. Execution time is faster than real-time.


Task list
=========
- [x] `/purge` command not removing all users [Fixed 😁](https://github.com/Armaggheddon/whisper2me/commit/417a7942ef443fb804d8d13778d59616679cac2b)
* [x] Add model cache to avoid redownload of the model every time the container is ran. [Fixed 😁](https://github.com/Armaggheddon/whisper2me/commit/4500298ba79377e9f156fccbd4e3f91de613b911)
