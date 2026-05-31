"""Trivial instrumentation example."""

import logging
import random

from fastapi import FastAPI

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
        return r
