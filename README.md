# Attendanceboard FR Extension

[![GitHub Release](https://img.shields.io/github/v/release/torbenkarlaa/attendanceboard-fr-extension.svg?style=flat)](https://github.com/torbenkarlaa/attendanceboard-fr-extension/releases)

## Introduction

Basic face recognition project for the attendanceboard using Python, cv2 and MongoDB

## Prerequisites

Make sure you have installed all the following prerequisites:

* Python Interpreter (build with 3.9.2) -
  [Download & Install Python](https://www.python.org/downloads/)
* Local MongoDB Server -
  [Download & Install MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
* Virtualenv for packages (or manually install all packages listed in the requirements.txt)  
  `pip3 install virtualenv`

## Run

* Add a none SockJS endpoint to a local instance of the attendanceboard and run it
* Run the MongoDB server
* Install all dependencies inside your virtualenv
* Run `main.py`

## Information

### Attendanceboard

* To enable websockets communication, an endpoint without SockJS is required. Simply add an endpoint in the _
  registerStompEndpoints()_ inside the _WebSocketConfig_ for this purpose.  
  `registry.addEndpoint("/attendanceBoard/websocket/none-sockjs").setAllowedOrigins(corsAPI, corsProxy);`

### Virtualenv & Pip3

* Build a virtualenv inside the repository - e.g. `virtualenv -p python3 .venv`
* Whenever a new shell is opened, activate the virtualenv
  (if not - packages will be installed globally, and the application eventually won't run)  
  `source .venv/bin/activate`
* Freeze requirements, whenever a new package is installed
  `pip3 freeze > requirements.txt`
* Install all packages listed in the requirements.txt
  `pip3 install -r requirements.txt`

### MongoDB

* Example of starting the server with brew `brew services start mongodb-community@4.4`
* Example of stopping the server with brew `brew services stop mongodb-community@4.4`