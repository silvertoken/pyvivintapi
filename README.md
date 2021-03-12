# pyVivintSky

A Python library for interacting with Vivint Sky API.

I own a system by Vivint and was annoyed when I found they didn't post any information about how the API works.
After looking over the internet I was able to find a few pieces of information and one gem written by Tim Harper. The homebridge site makes a claim that Tim used to be
a Vivint employee which I have no reason to doubt and honestly his work would require some type of inside knowledge to the API.

My intent here was to combine all the work that has been done over the last couple of years and combine them into a working library so I can add an integration to the
Home Automation System called Home Assistant (https://www.home-assistant.io/).

## Credit

| Name       |                                                                       Description                                                                       | Link                                            |
| :--------- | :-----------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------- |
| Tim Harper | Tim released a version for Homebridge with very useful information on how the API works. This served as the main basis for how I wrote the integration. | https://github.com/timcharper/homebridge-vivint |
| Reibart    |            Reibart did a lot work trying to reverse the API via browser calls. I used the information from this project to enhance this one.            | https://github.com/Riebart/vivint.py            |
| Ovirs      |                          Ovirs has some additions he made to Reibart work above and it contains information on other devices.                           | https://github.com/ovirs/pyvivint               |
| jhutchins  |                 JHutchins did a homework project using the devices and his site contains some infmormatio on the thermostat API calls.                  | https://github.com/jhutchins/vivint             |

## Features

### Authentication

Authentication is handled currently via username and password. I would recommend setting up a user on Vivint for just this purpose. This makes it easy to
distinguish when events are coming from automation.

This does direct calls to the Vivint API and stores a session key that last 20 mins by default. I then check for the expiration of this key on each call in the future
login again if its expired.

### PubNub

Message states and changes to devices are handled by PubNub. This API subscribes to the panels PubNub channel and is able to handle messages like doors opening
and closing.

## Devices

### Panel

This is the root device and all child devices are attached to it. Looking at the API its possible for an account to have more than one panel and this makes attempts to handle that.

| Feature      |  Status |
| :----------- | ------: |
| Armed State  | Working |
| Update State | Working |
| PubNub       | Working |

### Wireless Sensors

Devices that remotely connect to the sytem via 345 MHz wireless frequency. This includes door sensors, glass breaks, and motion detectors.

| Feature |  Status |
| :------ | ------: |
| Name    | Working |
| State   | Working |
| PubNub  | Working |

### Thermostat

I don't own one of these yet but there is enough information on the other sites I think to implement the features.

| Feature | Status |
| :------ | -----: |
|         |        |

### Door Locks

Door locks that connect to the system via Z-Wave

| Feature     |  Status |
| :---------- | ------: |
| Name        | Working |
| State       | Working |
| Lock/Unlock | Working |
| PubNub      | Working |

### Garage Doors

Garage doors that connect to the system via Z-Wave

| Feature    |  Status |
| :--------- | ------: |
| Name       | Working |
| State      | Working |
| Open/Close | Working |
| PubNub     | Working |
