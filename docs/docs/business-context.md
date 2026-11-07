# HomeSense: Business Context

## What is HomeSense?

HomeSense is a small smart home system I built for the IoT & Cloud Computing course. A device in the living room measures temperature, humidity and motion and sends the data to the cloud every 5 seconds. The owner can read this data through a REST API and can also send a command back to switch the heater on or off. In this project the device is simulated with a Python script, but the rest of the system works the same way it would with real hardware.

## The problem

When people are away from home they usually have no idea how warm it is inside. Leaving the heating on all day wastes energy and money, but turning it off completely can make the home cold or damp. A simple way to check the situation and react remotely would help with both. Many smart home products are also closed, so it is hard for other developers to connect their own apps to them. HomeSense tries to solve this with an open REST API.

## Who uses it

- **Homeowner:** wants to check the home and control the heater from anywhere
- **Business owner:** the company that would offer HomeSense, wants to see how it is used and keep the costs low
- **Developer:** wants to connect HomeSense to another application and needs a simple API

## Use cases

**1. Check the current situation at home**
The homeowner asks for the latest reading. The backend takes the newest file from cloud storage and returns temperature, humidity, motion and the heater status. If the device has not sent anything yet, the API says that no readings were found.

**2. Look at older data**
The user asks for the last N readings and gets them in time order. With this they can see, for example, how quickly the room cools down when the heater is off.

**3. Turn the heater on or off**
The homeowner sends `heater_on` or `heater_off`. The backend checks the command and saves it in cloud storage. The device looks for new commands every few seconds, so it picks it up and changes the heater. After that the readings show the new heater state and the temperature starts to go up or down. If the command is not valid, the API returns an error and nothing is saved.

**4. Connect another app**
A developer reads the README and tries the requests from the Postman collection, then calls the same endpoints from their own application. They don't need to change anything on the device.

## User stories

1. As a **homeowner**, I want to see the current temperature and humidity of my home so that I can check the comfort level when I am away.
   *Done when:* the latest reading is returned with temperature, humidity and timestamp.
2. As a **homeowner**, I want to see historical sensor data so that I can find trends and save energy.
   *Done when:* I can request the last N readings in time order.
3. As a **homeowner**, I want to send a heater command to my device so that I can control my home remotely.
   *Done when:* the device applies a valid command and the next readings show the new heater state.
4. As a **business owner**, I want to access the data stored in the cloud so that I can understand how the product is used and make decisions.
   *Done when:* all readings are stored as JSON files and can be read back through the API.
5. As a **developer**, I want clear REST API documentation so that I can integrate the device with other applications.
   *Done when:* the README lists the endpoints and there is a Postman collection with examples.
6. As a **business owner**, I want to know the cloud costs in advance so that I can plan the budget.
   *Done when:* a cost estimate for the Azure resources is in the repository (about $4 per month for one device).

## Scope

**Included:** the device simulator, cloud storage for readings and commands, a REST API (latest reading, history, send command), documentation, the architecture diagram and the cost estimate.

## Assumptions

- The device is simulated and sends one reading every 5 seconds.
- The demo uses one device (`livingroom-01`).
- Data is stored as JSON files in Azure Blob Storage.
- The backend runs on my computer for the demo. It could be moved to a cloud service like Azure App Service later.
