"""Trivial instrumentation example."""

import logging
import random

from fastapi import FastAPI
import httpx

from opentelemetry import trace


# create the logger
logger = logging.getLogger("uvicorn.error")

# create the app
app = FastAPI()

# set the tracer
tracer = trace.get_tracer(__name__)


@app.get("/run")
def run():
    """Generate a random number and return the response."""

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run_custom_logic") as span:
        r = random.randint(1, 20)

        # set a custom span attribute
        span.set_attribute("math.result", r)

        logger.info(f"Generated random int {r}")

        route = None
        if r < 10:
            route = "http://localhost:8081/run1"
        else:
            route = "http://localhost:8081/run2"

        with httpx.Client() as client:
            response = client.post(route, json={"r": r})
            body = response.json()
            return body["r"]

@app.get("/run_simple")
def run_simple():
    """Generate a random number and return the response."""

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run_simple_custom_logic") as span:
        r = random.randint(1, 20)

        # set a custom span attribute
        span.set_attribute("math.result", r)

        logger.info(f"Generated random int {r}")

        return r
