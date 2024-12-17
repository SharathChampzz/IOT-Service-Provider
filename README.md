
[Watch Demo Here](https://www.youtube.com/watch?v=ayjD2xVzs2g)

# IOT-Service-Provider - Connect NodeMCU with Firebase using this middle man - web application
Like Blynk and Adafruit, This is a simple  IOT site. This site mainly helpful for app developers who want to integrate android app and device like NodeMCU using HTTP request.

## Overview
This project aims to remotely read sensor data from a NodeMCU via an Android app and send commands back to the NodeMCU to perform actions. Inspired by platforms like Blynk and Adafruit, this project leverages Flask as a mediator to establish communication between Firebase and NodeMCU.

## Description
The project is built using Flask to facilitate communication between Firebase and NodeMCU. Users need to obtain the Firebase secret and upload it to the Flask app. The NodeMCU sends sensor data via HTTP requests to the Flask app, which in turn sends the status of other commands set by the user. Unlike socket connections, this project uses polling from the web app to the client (NodeMCU) for communication. (Requires enhancement here)

### Key Features
- **Remote Sensor Data Reading**: Read sensor data from NodeMCU remotely via an Android app.
- **Command Execution**: Send commands from the Android app to the NodeMCU to perform specific actions.
- **Flask as Mediator**: Use Flask to mediate communication between Firebase and NodeMCU.
- **Firebase Integration**: Store and manage sensor data and commands using Firebase.
- **Polling Mechanism**: NodeMCU polls the Flask app for commands, eliminating the need for socket connections.

This project serves as a beginner-level implementation with room for enhancements to make it more robust and efficient.

- Note: Android part implementation is a separate project. This project aims to bridge the gap between firebase and nodemcu.
