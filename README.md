Please create a virtual env
```python
py -m venv venv
```
Use the `requirements.txt` to download all the required packages in the venv
```command
pip install -r requirements.txt
```
To train the bot
```
rasa train --domain domain
```
To run the bot
run `actions` in one termial and `shell` in another terminal
```
rasa run actions
rasa shell
```
Use shell to interact with the bot
