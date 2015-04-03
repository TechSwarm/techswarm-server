# techswarm-server

## Quick start guide
```
virtualenv -p python3 server
cd server
source bin/activate
git clone https://github.com/m4tx/techswarm-server.git
cd techswarm-server
pip install -r requirements.txt
python tsserver.py
```

## Testing
TechSwarm Ground Station Server uses [behave](http://pythonhosted.org/behave/) BDD framework.

All packages required by the server to be tested can be installed using:

```
pip install -r requirements-test.txt
```

Then, ```behave``` can be started in server root directory (the one with tsserver.py).
