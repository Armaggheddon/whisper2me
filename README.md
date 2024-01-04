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
3. Inside the Dockerfile you have to edit the following lines:
    ```Dockerfile
    ENV BOT_TOKEN=YOUR_BOT_TOKEN
    ENV ADMIN_USER_ID=YOUR_ADMIN_ID
    ```
    where `YOUR_BOT_TOKEN` and `ADMIN_USER_ID` are written as is, for example:

    ```Dockerfile
    ENV BOT_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    ENV ADMIN_USER_ID=000000000
    ```
4. By default the bot will use the smallest model, i.e. `TINY`. However, if the device on which you are running the bot has more capabilities you may want to try bigger models. The available models are the ones provided by OpenAI and are (at the time of writing):
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
    
    To try different models, replace `TINY` with one of the above options in `src/whisper_helper/__init__.py`:
    ```python
    whisper_helper = _WhisperHelper(
        model_name = ModelNames.TINY # for example ModelNames.MEDIUM
        ...
    )
    ```
    >Refer to the OpenAI whisper's official paper for the performance evaluation between the different models, available [HERE](https://arxiv.org/abs/2212.04356)

5. Build the docker image with:
    ```bash
    docker build -t whisper2me .
    ```

6. After the image has been built you can see it with:
    ```bash
    docker images list
    ```
    And check for **whisper2me:latest**

7. The bot allows the admin user to add and remove users without having to re-run the bot. To allow for this behaviour and have persistent data the bot uses 2 files, namely `allowed_users.txt` and `allowed_users.bak`. These are required to be mounted inside the container so that any modification is also available in the host.

8. Run the container with:
    ```bash
    docker run -it --rm -v "$(pwd)"/allowed_users.txt:/whisper2me/allowed_users.txt -v "$(pwd)"/allowed_users.bak:/whisper2me/allowed_users.bak -d whisper2me:latest
    ```
    > `-d` runs the container in detached mode. \
    > To start the container automatically see Docker's `--restart` policies [here](https://docs.docker.com/config/containers/start-containers-automatically/), replace `--rm` with `--restart <YOUR_POLICY>`, i.e. `--restart unless-stopped`

9. When the container starts the model is downloaded. Depending on your internet connection and the selected model, this might take a while.


CUDA Setup
==========

If using on Jetson platform, `docker` is already installed in Jetpack, use [NVIDIA L4T PyTorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch/tags) image. If using on DGPU, `nvidia-docker` requires to be installed, you can follow the Nvidia's guide [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-the-nvidia-container-toolkit) and use the [PyTorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) image.

> [!NOTE]
> The following steps have been tested on a Nvidia Orin AGX running Jetpack 5.1.2 with the NVIDIA L4T PyTorch r35.2.1-pth2.0-py3 image. If trying to use on a DGPU the steps might be different

1. Follow steps `1` and `2` of [Setup](#setup)

2. Run the container and mount the current directory with:
    ```bash
    docker run -it --rm --runtime nvidia --gpus all -v "$(pwd)":/whisper2me nvcr.io/nvidia/pytorch:xx.xx-py3
    ```
    replace `pythorch:xx.xx-py3` with the version you downloaded

3. Once inside the container install ffmpeg with:
    ```bash
    apt update && apt install ffmpeg -y
    ```

4. Install the python requirements with:
    ```bash
    cd /whisper2me
    pip install -r requirements_cuda.txt
    ```
    If you get an error stating
    > ERROR: numba 0.58.1 has requirement numpy<1.27,>=1.22, but you'll have numpy 1.17.4 which is incompatible.
    
    run the following command:
    ```bash
    pip install -U numpy
    ```
    and then re-run the above command 

5. When the installation has finished press `CTRL+P` + `CTRL+Q` to detach from the running container

6. Get the container ID with:
    ```bash
    docker container list
    ```
    and copy the `CONTAINER ID` of the PyTorch container

7. Commit the changes to the container and save it with a new name with:
    ```bash
    docker commit -p CONTAINER_ID whisper2me:latest
    ```
    The changes to the base image are stored in the new image that will be named `whisper2me:latest`
    > `-p` option pauses the container while the commit is being executed.

8. Check the new image with:
    ```bash
    docker image list
    ```

9. To change the default model used see step `4` in [Setup](#setup)

10. Enable CUDA editing the following lines in `src/whisper_helper/__init__.py`:
    ```python
    whisper_helper = _WhisperHelper(
        model_name = ModelNames.TINY, # or a different one like ModelNames.MEDIUM
        device = Devices.CUDA,
        use_fp16 = ModelDtypes.USE_FP32, # or ModelDtypes.USE_FP16 to use fp16
        device_id = 0, # replace 0 with the GPU id you want to use
    )
    ```
    Additionally using `ModelDtypes.USE_FP16`, when using `Devices.CUDA`, you can enable the use of 16-bit floating point weights instead of 32-bit to improve inference time while losing a bit of precision (bigger models are less influenced by this change). If you have more than one GPU and plan to run this code on a specific GPU use `device_id` to chose the GPU.

11. Now you can run the bot with your new image with:
    ```bash
    docker run -it --rm --runtime nvidia --gpus all --env BOT_TOKEN=YOUR_BOT_TOKEN --env ADMIN_USER_ID=YOUR_USER_ID -v "$(pwd)":/whisper2me -d whisper2me:latest bash -c "cd /whisper2me && python3 src/main.py"
    ```
    replacing `YOUR_BOT_TOKEN` and `YOUR_USER_ID` with the appropriate values. 

12. When the container starts the model is downloaded. Depending on your internet connection and the selected model, this might take a while. The startup time, compared to CPU is significantly longer, on my tests the bot can take up to 1 minute before being ready.


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
    - `/help` shows a list of available commands

- Commands available only to the ADMIN:
    - `/language` change the model target language, currently are listed only:
        - 🇺🇸 English
        - 🇮🇹 Italian
    
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


Task list
=========
- [x] `/purge` command not removing all users [Fixed 😁](https://github.com/Armaggheddon/whisper2me/commit/417a7942ef443fb804d8d13778d59616679cac2b)
* [ ] Add model cache to avoid redownload of the model every time the container is ran.
