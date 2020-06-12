# Messenger-Bot

An implementation of a bot for Facebook Messenger. The bot successfully logs into an Facebook account (called **Botu Robotu**) and can access all the message threads. 

It is capable of sending messages, seeing other messages and currently can send weather data through the use of an API (OpenWeather API https://openweathermap.org/api).

This bot will be used as an 'Group chat' without the need to actually create a group. All will be done in a single user thread.

Our goal is to implement some form of logging (when a new user sends a message to our bot, he will be asked to tell his name), implement more functionalities (basic infomation that can be asked directly) and the capability to post things on Facebook. Also we would like to move the app to a cloud platform (Microsoft Azure or Amazon AWS).

All our Bot commands must contain the word 'Botule' and a certain keyword specific to an action ('vremea').

## Requirements:

- Python 3
- Pip
- Following Python Modules: requests, fbchat, pyshorteners
- OpenWeather API key
- Facebook/Messenger account

## Functionality

The fbchat module acts as an browser and manages to connect to the Facebook page.

This is a demonstration of the capabilities of our bot:
![alt text](https://github.com/florinalexandrunecula/Messenger-Bot/blob/master/Photos/Demo.PNG)
