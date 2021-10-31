# TagSpy
This project runs on the Flask lightweight server framework for Python.

## Installation & running the project locally
Clone the project and setup a Python virtual environment in a directory of your choosing. It's suggested to use the latest possible build of Python and pip, but anything past 3.7 *should* work. Note: You might have to replace `python` with `python3` or `pip` with `pip3` depending on your setup. These were tested on Mac but should also work on Linux.
```
python -m venv <path/to/venv>
```
and source it
```
source <path/to/venv>/bin/activate
```
Head into the cloned project folder and install dependencies by running
```
pip install -r requirements.txt
```

To run the project we need to set two environment variables for Flask:
```
export FLASK_APP=wsgi
export FLASK_ENV=development
```
We don't actually need the second one but it's pretty handy, because it allows us to see debug information.

Next up just hit
```
flask run
```
and we should be good to go. If everything went well you can now head over to the URL shown in the output log (default is `http://127.0.0.1:5000/`) and you should see the Following greeting message: `Hello and welcome. Please call a specific API.`

## Using the app
All APIs are provided under the path /api/ and currently the only service provided is one that fetches review analytics based on tags. As of right now there's no logic, only reviews are fetched. You can try this out by heading to for example the URL `http://127.0.0.1:5000/api/summary?tags=FPS,Multiplayer,Competitive,Military`. This should provide you with the first 100 reviews for all of the 26 games that have all the tags provided in the URL.

Analysis logic can be added to the file `src/service/__init__.py`.