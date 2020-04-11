# Easypoll

Easypoll is a discord bot to create polls

## Usage

The question must comes as first argument after the `/poll`

All arguments must comes between double quotes

You can optionally add choices.

```
/poll "Question"
```
or

```
/poll "Question" "Choice A" "Choice B" "Choice C"
```


## Install

Straightforward python deployment:

```
git clone https://github.com/leadrien/easypoll.git
cd easypoll
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The discord bot token can be stored in a `.env` file, located in the script folder.
```
# .env file
DISCORD_TOKEN=my_bot_token
```

Run with
```
python easypoll.py
```

## Example

![Easypoll](screen_1.png)


## Credits

Icon based on [Freepik from www.flaticon.com](https://www.flaticon.com/free-icon/histogram_2658175?term=histogram&page=1&position=7)
