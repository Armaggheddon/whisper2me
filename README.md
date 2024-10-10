<div id="top"></div>
<br/>
<br/>

<p align="center">
  <img src="./doc/images/shushing_emojy.png" width="150" height="150">
</p>

<h1 align=center>
    <a href="https://github.com/Armaggheddon/whisper2me">whisper2me</a>
</h1>

<p align="center">
<a href="https://github.com/Armaggheddon/whisper2me/commits/main">
<img src="https://img.shields.io/github/last-commit/Armaggheddon/whisper2me">
</a>
<a href="https://github.com/Armaggheddon/whisper2me">
<img src="https://img.shields.io/badge/Maintained-yes-green.svg"/>
</a>
<a href="https://github.com/Armaggheddon/whisper2me/issues">
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/Armaggheddon/whisper2me">
</a>
<a href="https://github.com/Armaggheddon/whisper2me/blob/main/LICENSE">
<img alt="GitHub License" src="https://img.shields.io/github/license/Armaggheddon/whisper2me"/>
</a>
<!--<a href="https://github.com/Armaggheddon/whisper2me">
<img src="https://img.shields.io/badge/Maintained%3F-no-red.svg">
</a> -->
</p>

<p align="center">
💬 <b>Hate voice messages?</b> 🎙️ Let <b>whisper2me</b> handle them! Just forward the audios and get smooth transcriptions. Fast, simple, and ready for action! ⚡✨
</p>


## Table of Contents  
* [Prerequisites](#preprequisites)
* [Setup](#setup)
* [CUDA Setup](#cuda-setup)
* [Usage](#usage)
* [Available commands](#available-commands)
* [How it works](#how-it-works)
* [Known issues](#known-issues)
* [Task list](#task-list)


## Prerequisites 🚀

The easiest way to get **whisper2me** up and running is via Docker. Check out the official guide to install Docker Compose [here](https://docs.docker.com/compose/install/).

Here's what you'll need:
- The **bot token** from BotFather on Telegram (find out how [here](https://core.telegram.org/bots/tutorial#getting-ready))
- Your **user_id** from Telegram
- An Nvidia GPU if you're planning to run the CUDA version with the NVIDIA Container Toolkit (see installation steps [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html))

> [!NOTE]
> Heads-up! Tested on Ubuntu and WSL. No guarantees for other OS's. CUDA tests were done on Nvidia Orin AGX and RTX 3070 Ti via WSL.


## Setup 🔧

1. Clone the repository on your machine with:
    ```bash
    git clone https://github.com/Armaggheddon/whisper2me.git
    ```
1. Enter the folder:
    ```bash
    cd whisper2me
    ```
1. Rename `bot_config.env.example` to `bot_config.env` and replace the fields with your own:
    - Replace `YOUR_BOT_TOKEN` and `ADMIN_USER_ID`:

        ```dosini
        BOT_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        ADMIN_USER_ID=000000000
        ```
    - By default, the bot uses the **TINY** model, but you can pick a larger one if your system can handle it. Here are your options:
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
    
        To try different models, replace `TINY` with one of the above options in `bot_config.env`:
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


1. Build the image:
    ```bash
    docker compose build
    ```
    The image created is named as `whisper2me_bot:latest`.


1. Run the container with:
    ```bash
    docker compose up -d
    ```
    `-d` runs the container in detached mode.
    
> [!TIP]
> The container is, by default, set to automatically restart on failure and when the device restart. This can be changed in the `deploy.restart_policy.condition` setting in `docker-compose.yml` file.


9. When the container starts the model is downloaded. Depending on your internet connection and the selected model, this might take a while. The model's weights and the list of allowed users (other than the administrator) are stored in a volume named `whisper2me_bot_data`.


## CUDA Setup ⚡

To run whisper2me with CUDA acceleration, follow the regular setup, but use these commands for building and running the container:

- Build:
    ```bash
    docker compose -f cuda-docker-compose.yml build
    ```

- Run:
    ```bash
    docker compose -f cuda-docker-compose up -d
    ```

> [!NOTE]
> Tested on Nvidia Orin AGX running Jetpack 5.1.2 with the NVIDIA L4T PyTorch r35.2.1-pth2.0-py3 image and on an RTX 3070 Ti running in WSL. 



## Usage 🎉

Once everything’s running, open your bot’s chat and hit `/start`. Ready to roll! 🏁

![](/doc/images/start_example.png)

To transcribe, just forward any voice message, and voilà, you’ll receive the transcription. 🚀 

![](/doc/images/test_message.png)

When a non-admin user tries a restricted command, the admin will be notified with a message containing the `user_id` and the `command` that the user sent. 🔔

![](/doc/images/admin_warning.png)


## Available commands 📝

**For all users:**
- `/start` begins the conversation with the bot
- `/info` shows the current bot settings
- `/help` shows a list of available commands

**For the admin only:**
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
    - Forward a text message of the desired user so that the `user_id` is automatically retrieved, much simpler!
    
- `/remove_user` starts the interaction to remove a user. A list of currently allowed users is display, simply click the one you want to remove

- `/purge` removes all users from the allowed list. Requires a confirmation message that spells exactly `YES`



## How it works ⚙️

whisper2me combines the magic of OpenAI's [whisper](https://github.com/openai/whisper) and [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

> [!NOTE]
> Translation works only with non-`_EN` models

The code can run on both ARM-64 and X64 architectures. It has been tested on:
- Raspberry Pi 3B with 1GB of RAM (using [Raspberry Pi OS(64-bit) Lite](https://www.raspberrypi.com/software/operating-systems/)), the only runnable model is the `TINY` one. Almost all available Pi's resources are used and runs approximately 6x slower than real-time.

- Nvidia Orin AGX with 64GB of RAM (using [Jetpack 5.1.2](https://developer.nvidia.com/embedded/jetpack-sdk-512)), all models run without any issue. Using the `LARGE_V3` model requires around 25-30 GB of combined RAM (both CPU and GPU). Execution time is faster than real-time.

- WSL on a desktop in both standard and CUDA version with an RTX 3070 Ti. Execution time is faster than real-time.
