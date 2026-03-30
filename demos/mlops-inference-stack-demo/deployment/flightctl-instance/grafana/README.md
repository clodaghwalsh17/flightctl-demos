# Instructions

This folder contains sample Grafana dashboards to monitor the performance of the model rolled out across the fleet. These dashboards can be configured by either:

1. Navigating to the Grafana UI (hosted on port 3000 on the same URL/IP as the FlightCtl instance) and importing the dashboard from file.

2. Logging into the FlighCtl instance via SSH, adding the json files to the ```/etc/flightctl/flightctl-grafana/provisioning/dashboards/flightctl``` directory and restarting the observability service, ```systemctl restart flightctl-observability.target```. 