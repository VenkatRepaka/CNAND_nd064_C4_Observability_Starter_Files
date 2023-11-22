**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

## Describe SLO/SLI
Below are the SLOs for a monthly uptime and request response time:
1. 99.5% uptime in a month
2. 99% of the requests are served under 200 milliseconds

Below are the actual metrics for the current year (SLI): 
1. We had 99.8% uptime current year
2. 99% of the API calls had request response time of 150 milliseconds

## Creating SLI metrics.
1. Latency: Request response time 
2. 40X & 50X Errors: Number of requests that have errors/failed
3. CPU & Memory Usage: Average CPU and Memory, this indicates the overall capacity at which the service is running.
4. Uptime: Percentage of the time service is hosted/running
5. Traffic: Number of incoming requests to the service 

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

TROUBLE TICKET

Name: Venkat Repaka

Date: 22-Nov-2023

Subject: Service - trial, Endpoint - /trace failed with 500 errors 

Affected Area: Trial service trace

Severity: High

Description: endpoint /trace in trial service is failing with 500 error. 


## Creating SLIs and SLOs
1. Service uptime of 99.8%
2. Average latency under 200 milliseconds
3. Error rate (40X or 50X) to be under 0.1% or success rate (20X) above 99.5%


## Building KPIs for our plan
1. Latency - 90 percentile of request durations are under 200ms and average response time is under 200ms
2. Uptime - Service uptime of at least 99.9%
3. Errors - Number of failed responses is below 0.5%


## Final Dashboard 
Final Dahsboard
![final dashboard](ans-img/Final%20Dashboard.png)