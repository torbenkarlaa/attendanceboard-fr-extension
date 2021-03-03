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
* End Application with pressing _q_

## Information

### Attendanceboard

* To enable websockets communication, an endpoint without SockJS is required. Simply add an endpoint in
  _registerStompEndpoints()_ inside the _WebSocketConfig_ for this purpose.  
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

## Example benchmark results

The following numbers were achieved with the above settings. The application was run for exactly 60 seconds. The person
to be recognised moved slightly within the camera's field of view and tilted the face horizontally and vertically. The
data are only exemplary and can deviate (strongly), especially the values for the detection ratio are strongly dependent
on, among other things, the lighting conditions and the orientation of the face. If the detection ratio is high, the
number of recorded frames automatically decreases, as calculations are still carried out for identification.

### 1920 x 1080 - No frame rescaling

| Scale factor | CPU average | CPU peak | Memory average | Memory peak | Recorded frames | Detection ratio | FPS average | FPS highest | FPS lowest |
| ------------ | ----------- | -------- | -------------- | ----------- | --------------- | --------------- | ----------- | ----------- | ---------- |
| 1.1          | 464.1947%   | 547.2%   | 1.8671%        | 1.8921%     | 245             | 97.9592%        | 3.6923      | 5           | 3          |
| 1.2          | 415.0465%   | 478.2%   | 1.5666%        | 1.6071%     | 372             | 98.9247%        | 5.7778      | 6           | 5          |
| 1.3          | 377.1530%   | 496.2%   | 1.4261%        | 1.4751%     | 468             | 80.9829%        | 7.2857      | 9           | 6          |
| 1.4          | 312.2351%   | 441.0%   | 1.3914%        | 1.4148%     | 536             | 63.4328%        | 8.4286      | 10          | 7          |
| 1.5          | 324.1212%   | 417.5%   | 1.3487%        | 1.3875%     | 562             | 30.2491%        | 8.8750      | 11          | 7          |

### 1920 x 1080 - Frame rescaling

| Scale factor | CPU average | CPU peak | Memory average | Memory peak | Recorded frames | Detection ratio | FPS average | FPS highest | FPS lowest |
| ------------ | ----------- | -------- | -------------- | ----------- | --------------- | --------------- | ----------- | ----------- | ---------- |
| 1.1          | 341.4422%   | 518.8%   | 1.8331%        | 1.8512%     | 460             | 89.1304%        | 7.1607      | 10          | 5          |
| 1.2          | 279.0184%   | 482.1%   | 1.5512%        | 1.6035%     | 523             | 90.8222%        | 8.2500      | 10          | 6          |
| 1.3          | 245.5231%   | 458.3%   | 1.4206%        | 1.4411%     | 589             | 74.3633%        | 9.4107      | 12          | 8          |
| 1.4          | 193.7301%   | 392.2%   | 1.3350%        | 1.4074%     | 581             | 51.8072%        | 9.1754      | 12          | 6          |
| 1.5          | 187.0709%   | 365.9%   | 1.3202%        | 1.3416%     | 640             | 47.5000%        | 10.2105     | 13          | 8          |

### 960 x 540 - No frame rescaling

| Scale factor | CPU average | CPU peak | Memory average | Memory peak | Recorded frames | Detection ratio | FPS average | FPS highest | FPS lowest |
| ------------ | ----------- | -------- | -------------- | ----------- | --------------- | --------------- | ----------- | ----------- | ---------- |
| 1.1          | 346.9876%   | 490.9%   | 1.1301%        | 1.1713%     | 483             | 93.5818%        | 7.6545      | 11          | 5          |
| 1.2          | 298.6486%   | 453.2%   | 1.0400%        | 1.0591%     | 663             | 93.5143%        | 10.5439     | 12          | 7          |
| 1.3          | 243.1818%   | 394.2%   | 0.9637%        | 1.0294%     | 740             | 74.8649%        | 11.7719     | 13          | 9          |
| 1.4          | 195.3441%   | 353.6%   | 0.9475%        | 0.9682%     | 808             | 82.0545%        | 12.9474     | 16          | 11         |
| 1.5          | 209.0274%   | 351.8%   | 0.9431%        | 0.9924%     | 804             | 65.0498%        | 12.8421     | 16          | 11         |

### 960 x 540 - Frame rescaling

| Scale factor | CPU average | CPU peak | Memory average | Memory peak | Recorded frames | Detection ratio | FPS average | FPS highest | FPS lowest |
| ------------ | ----------- | -------- | -------------- | ----------- | --------------- | --------------- | ----------- | ----------- | ---------- |
| 1.1          | 251.3984%   | 432.1%   | 1.0725%        | 1.1358%     | 693             | 88.4560%        | 11.0702     | 16          | 9          |
| 1.2          | 217.7739%   | 418.3%   | 0.9954%        | 1.0599%     | 766             | 70.3655%        | 12.2456     | 16          | 10         |
| 1.3          | 166.0263%   | 346.1%   | 0.9953%        | 1.0300%     | 828             | 68.7198%        | 13.3334     | 19          | 12         |
| 1.4          | 131.4330%   | 357.5%   | 0.9438%        | 0.9671%     | 848             | 80.4245%        | 13.5965     | 18          | 12         |
| 1.5          | 156.2355%   | 359.5%   | 0.9420%        | 0.9628%     | 918             | 55.2288%        | 14.8421     | 19          | 12         |

### Scale factor 1.1

| Settings                            | Recorded frames | Detection ratio | Detected frames |
| ----------------------------------- | --------------- | --------------- | --------------- |
| 1920 x 1080<br />No frame rescaling | 245             | 97.9592%        | 240             |
| 1920 x 1080<br />Frame rescaling    | 460             | 89.1304%        | 410             |
| 960 x 540<br />No frame rescaling   | 483             | 93.5818%        | 452             |
| 960 x 540<br /> Frame rescaling     | 693             | 88.4560%        | 613             |

### Scale factor 1.2

| Settings                            | Recorded frames | Detection ratio | Detected frames |
| ----------------------------------- | --------------- | --------------- | --------------- |
| 1920 x 1080<br />No frame rescaling | 372             | 98.9247%        | 368             |
| 1920 x 1080<br />Frame rescaling    | 523             | 90.8221%        | 475             |
| 960 x 540<br />No frame rescaling   | 663             | 93.5143%        | 620             |
| 960 x 540<br /> Frame rescaling     | 766             | 70.3655%        | 539             |