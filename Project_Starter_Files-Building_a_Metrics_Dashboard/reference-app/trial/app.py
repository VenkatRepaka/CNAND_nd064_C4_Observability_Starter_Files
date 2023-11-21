import logging
import re
import requests
import sys

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from jaeger_client import Config
# from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


app = Flask(__name__)
cors = CORS(app)

metrics = PrometheusMetrics(app)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

metrics.info("app_info", "Application info", version="1.0.3")

# logging.getLogger("").handlers = []
# logging.basicConfig(format="%(message)s", level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# def init_tracer(service):
#
#     config = Config(
#         config={
#             "sampler": {"type": "const", "param": 1},
#             "logging": True,
#             "reporter_batch_size": 1,
#         },
#         service_name=service,
#         validate=True,
#         metrics_factory=PrometheusMetricsFactory(service_name_label=service),
#     )
#
#     # this call also sets opentracing.tracer
#     return config.initialize_tracer()


# tracer = init_tracer("trial")

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "trial-new-service"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://simplest-collector-headless.observability.svc.cluster.local:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("trial-new")

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@app.route("/")
def homepage():
    return render_template("main.html")


@app.route("/trace")
def trace():
    def remove_tags(text):
        tag = re.compile(r"<[^>]+>")
        return tag.sub("", text)

    with tracer.start_span("get-startwars-people") as span:
        res = requests.get("https://swapi.dev/api/people")
        response = res.json()
        # span.log_kv({"event": "get people count", "count": response['count']})
        # span.set_tag("people-count", response['count'])
        logger.debug("event - {0} and count - {1}".format("get people count", response['count']))

        people_info = []
        for result in response['results']:
            character = {}
            with tracer.start_span("request-site") as site_span:
                logger.info(f"Getting details for {result['name']}")
                try:
                    # character["description"] = remove_tags(result["description"])
                    character["name"] = result["name"]
                    character["height"] = result["height"]
                    character["mass"] = result["mass"]
                    character["hair_color"] = result["hair_color"]
                    character["skin_color"] = result["skin_color"]
                    character["eye_color"] = result["eye_color"]
                    character["gender"] = result["gender"]
                    character["birth_year"] = result["birth_year"]

                    people_info.append(character)
                    site_span.set_attribute("http.status_code", res.status_code)
                    site_span.set_attribute("character-name", result["name"])
                except Exception:
                    logger.error(f"Unable to get details for {result['name']}")
                    site_span.set_attribute("http.status_code", res.status_code)
                    site_span.set_attribute("character-name", result["name"])

    return jsonify(people_info)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)