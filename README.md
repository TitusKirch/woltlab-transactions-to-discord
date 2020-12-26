# woltlab-transactions-to-discord
"woltlab-transactions-to-discord" is a small project to post trader transaction at WoltLab via a webhook in a Discord channel.

## Requirements
You will need Python 3, pip3 and git.

## Installation
First download the project, go to the appropriate folder, install the required packages and create the .env file.
```bash
git clone https://github.com/TitusKirch/woltlab-transactions-to-discord.git
cd woltlab-transactions-to-discord/
pip3 install -r requirements.txt
cp .env.example .env
```
Afterwards they deposit the necessary data in the .env file

## Usage
Afterwards you can create a cronjob that executes the script every 30 minutes.
```BASH
*/30 * * * * cd /path/to/woltlab-transactions-to-discord && python3 ./run.py >/dev/null 2>&1
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT License](LICENSE)