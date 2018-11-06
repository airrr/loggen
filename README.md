# Log generator

Provided with this project is a small python interactive command line tool to generate apache access log lines.

## Getting Started

Two ways to run the log monitor: Docker or Python and Pipenv
For both methods, be at the sources root directory

### Docker

```
docker build . -t loggen
```
The command above will build the log generator image.

You can simply run the application after with:
```
docker run -ti loggen
```
By default, the log generator will write to the container /tmp/access.log file.
It's better to have it write to your own /tmp/access.log by mounting it

```
docker run -ti -v /tmp:/tmp loggen
```

### Python & Pipenv

For this method, you need Python 3 and Pipenv installed

```
pipenv install --system --deploy
```

This will download the dependencies and build the virtual env.
Then run
```
pipenv run python main.py
```

## Usage

Once launched, you will have a prompt such as state | logfile >
```idle | /tmp/access.log >```

The different options are:
* start: start appending to the log file
* stop: stop appending to the log file
* truncate: truncate the current log file
* rotate: rotate the current log file to the same with .next appended
* file *fileName*: set the file to be written to
* exit: exits the command line

## Built With

* [Pipenv](https://pipenv.readthedocs.io/) - Dependency management & Virtual env
* [Cmd2](http://cmd2.readthedocs.io) - Interactive command line

## Authors

* **Gaetan Deputier**