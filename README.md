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

Run with
```
python easypoll.py
```
