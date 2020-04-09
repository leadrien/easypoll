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
git clone https://githepia.hesge.ch/adrienma.lescourt/easypoll
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
