from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import Counter

import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://admin:secret@mongodb-svc.default.svc.cluster.local:27017/example-mongodb?authSource=admin"

mongo = PyMongo(app)

cors = CORS(app)

prom_metrics = PrometheusMetrics(app)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

prom_metrics.info("app_info", "Application info", version="1.0.3")

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "backend-service"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://simplest-collector-headless.observability.svc.cluster.local:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("backend")

# reader = PeriodicExportingMetricReader(
#     OTLPMetricExporter(endpoint="http://simplest-collector-headless.observability.svc.cluster.local:4317")
# )
# reader = PrometheusMetricReader()
# provider = MeterProvider(resource=resource, metric_readers=[reader])
# metrics.set_meter_provider(provider)
#
# meter = metrics.get_meter("backend-service-metrics")
# root_visits_counter = meter.create_counter(name="root-visits", description="Nuber of visits for root path")
# api_visits_counter = meter.create_counter(name="api-visits", description="Nuber of visits for root path")
root_visits_counter = Counter('root_visits', 'Number of visits for root path')
api_visits_counter = Counter('api_visits', 'Number of visits for api path')


@app.route("/")
def homepage():
    # root_visits_counter.add(1)
    root_visits_counter.inc(1)
    return "Hello World"


@app.route("/api")
def my_api():
    api_visits_counter.inc(1)
    answer = "something"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    print(request.json)
    name = request.json["name"]
    distance = request.json["distance"]
    star_doc = star.insert_one({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_doc.inserted_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run()
