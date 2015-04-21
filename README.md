# techswarm-server

## Quick start guide
```
virtualenv -p python3 server
cd server
source bin/activate
git clone https://github.com/m4tx/techswarm-server.git
cd techswarm-server
pip install -r requirements.txt
python install.py
python runserver.py
```
techswarm-server uses SQLite database (named database.db, stored in server root directory) by default. Database settings can be changed in `config.py` file.

## Testing
TechSwarm Ground Station Server uses [behave](http://pythonhosted.org/behave/) BDD framework.

All packages required by the server to be tested can be installed using:

```
pip install -r requirements-testing.txt
```

Then, testing framework can be started in server root directory (the one with `runserver.py`) via:

```
behave tsserver/features
```

Tests use in-memory SQLite database by default. There is also an option to use temporary database file instead - see `features/environment.py` for that.

## Usage
### So-called generic models
* `/status`
* `/gsinfo`
* `/imu`
* `/sht`
* `/gps`
* `/planetarydata`

Both retrieval and adding data is pretty straightforward here:

* GET returns list of objects in database.
* POST is used to send data. POST request *must* include data for each 
  column, otherwise 400 status code is returned (the only exception is 
  `/planetarydata`). Each URL from here has its exactly corresponding model in 
  `tsserver/genericapi/models.py`, so you should check this file for the list 
  of parameters and their value types. Example of POST parameters for /sht:
  
`timestamp=2015-01-01T03:01:12.001122&humidity=70.1&temperature=24.01`

There are also some models which include URLs that can be used to work with 
element with latest timestamp:

* `/status/current`
* `/gsinfo/current`

In these cases, GET retrieves the latest element, and PUT can be used to send
new data (usage is exactly the same as with POST).

### Photos
* `/photos`
* `/panorama`

Available actions:

* List of all photos can be retrieved using GET on `/photos` URL
* Latest photo with is_panorama column value equal to True can be retrieved 
  using GET on `/panorama`
* New photo can be uploaded using POST to `/photos` with photo timestamp in 
  `timestamp` parameter and the image itself in `photo` parameter
  (`is_panorama`, which is False by default, can be provided as well, but using
  `/panorama` URL for sending panoramas is preferred over it)
* New panorama image can be uploaded using PUT on `/panorama` - usage is 
  exactly the same as when using POST on `/photos`, except that `is_panorama` 
  value is forced to be True

Returned JSONs with Photo data include URL of the image file in "url" key.

### Common GET parameters
* `since` parameter, whose value is datetime in format standard for 
  timestamps (see section below) can be used to retrieve elements with 
  `timestamp` higher than the value of the parameter. It is the preferred way
   to get model updates since specified point in time.

### POST/PUT behavior
Both POST and PUT responses include JSON representation of the newly added 
object.

### Timestamps
All models have `timestamp` column. Internally in database it is stored as 
DATETIME (year-month-day + hour-minute-second-microseconds). Since there is 
no standard for storing datetime objects in JSON nor sending them via POST, 
ISO 8601 without timezone info was chosen as a format for both use cases. In 
other words, the format is:

`%Y-%m-%dT%H:%M:%S.%f`

### Status codes
* All GET requests should return 200 OK status code. Everything else is an 
  error. 
* All POST and PUT requests should return 201 CREATED status code. Everything
  else is an error.
* 400 BAD REQUEST is often returned when parameter values are invalid.
* In case of errors, value of "message" in returned JSON may be helpful in 
  identifying the cause.

### Authentication
All POST or PUT requests *must* use HTTP basic authentication, otherwise 401 
status code is returned. Valid username and password are stored in `config.py`.

### Bulk retrieval
* `/bulk/<comma-separated list of models to get>`

Data from multiple models can be retrived in single request using Bulk 
retrieval. By and large it gets data from each model, and then packs it to 
single JSON object, with key names equal to model names, and values equal to 
what would GET normally provide. In other words - what, for instance, would 
`/bulk/sht,gps` return is:

```
{
    'sht': <contents of /sht>,
    'gps': <contents of /gps>
}
```

Bulk retrieval can be used with GET parameters, like `since`, as well - in this 
case, the parameter is passed to all models.

List of models which can be "bulk retrieved":

* `status`
* `gsinfo`
* `photo`
* `imu`
* `sht`
* `gps`
* `planetarydata`

### Tests
Since techswarm-server uses BDD framework for testing, and therefore, 
tests are actually written in "almost-natural" language, reading .feature files
(in `tsserver/features`) may be helpful in understanding how API works.
