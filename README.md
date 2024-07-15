# Berlin Appointments

Simple script that scrapes appointments for Berlin Bürgerämter.
Lets you provide a discord webhook url and the service id. It will notify @everyone with a list of dates and a url.

If you provide an empty location id a list of all possible locations in berlin will be used. This only exists for some appointments though, for e.g. Personalausweis abholen you need to specify the one you want.

You can get the service id and location id by copying the url from the appointment page. Go to a page like [this](https://service.berlin.de/dienstleistung/324325/) for your service. In this case you would copy _324325_ from the page url as the service id. Right clicking one of the _Termin buchen_ buttons you can get the number after _dienstleister=_, for e.g. Schöneberg this would be _329863_.

This now also supports resend to send emails instead of discord messages. You can set the recepients and api key in the environment variables.

## Deployment

I set this up to be as simple to run as possible, you can modify it to your needs.

I have this repo deployed on hop.io (literally just select it and that's it). When you don't need it just delete the container and trigger a rollout when you need it. You can set the environment variables there. Make sure to trigger a rollout after you change them.
