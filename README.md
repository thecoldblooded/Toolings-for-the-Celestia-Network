This Celestia tool is a software application designed to assist with monitoring Celestia nodes and sending automatic notifications to a connected Telegram bot. The tool has several features, including the ability to:

  - Monitor CPU usage to ensure it does not exceed a certain threshold.
  - Monitor RAM usage to ensure it does not exceed a certain threshold.
  - Monitor disk usage to ensure it does not exceed a certain threshold.
  - Detect if the blockchain is stuck.
  - Monitor the height of samples.
  - Verify that the node is syncing.
  - Report on P2P checking.
  - Report on state checking.

To set up a Telegram bot for use with Celestia tool, you must first create a new bot using the Telegram BotFather. To do this, open a chat with BotFather on Telegram by searching for **`@BotFather`** in the search bar and selecting it. Then type the command **`/newbot`** to begin the process.

Next, you will need to choose a name and a unique username for your new bot. The name can be whatever you like, but the username must end in "bot" (e.g. CelestiaBot). After you have made your selections, BotFather will provide you with an API token which will allow you to access your bot's API. Be sure to keep this token secure.

Once you have created your bot, you will need to add it to a new Telegram group and obtain the group's chat ID. There are several ways to obtain the chat ID, but one of the easiest methods is to add **`@getidsbot`** to your group. This bot will automatically send the group ID to the chat group.

You will need to use the API token and chat ID during the installation process, which will be referred to as <tg_token> and <tg_chat_id>, respectively.

Clone repository

```bash
git clone https://gitlab.com/celestia_job/tool.git ~/tool
```

Before proceeding, ensure that your server has Python 3 installed. You can verify the version of Python 3 by running the following command.

```bash
python3 -V
which python3
```

```bash
sudo apt update -y
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git 
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```

```bash
pyenv install 3.8.10 
```

Establish a virtual environment and activate it.

```bash
cd ~/tool
~/.pyenv/versions/3.8.10/bin/python -m venv venv
```

Install requirements

```bash
cd ~/tool
venv/bin/python3 install -r requirements.txt
```

Create environment variables

```bash
cp .env.example .env
```

```bash
cd ~/tool
nohup python3 main.py 1>/dev/null 2>/dev/null &
```

Execute the command below to halt the service.

```bash
kill -9 $(ps -aux | grep "python3 main.py" | awk '{print $2}')
```
