# Berlin Appointments

Simple fastapi that scrapes appointments for Berlin Bürgerämter. Provides a post and a get endpoint. The post lets you pass in a discord webhook url.
This is the setup I'm using, it will notify @everyone in a specific channel with all new appointments.

## Deployment

I set this up to be as simple to run as possible, you can modify it to whatever you need.

I have this repo deployed on hop.io (literally just select it and that's it). From there you can add a gateway (also a one click thing) and use that url with something like upstash. With that I just hit the endpoint every 3 minutes which sends me a message if there are new appointments. It's super easy to turn on when needed and to configure the post request on upstash.
