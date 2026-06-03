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

        if r < 10:
            return run1(r)
        else:
            return run2(r)


# more endpoints to run trace across multiple hops
@app.get("/run1")
def run1(r: int):
    """Sets a custom field value to the double of input."""

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run1_custom_logic") as span:
        r *= 2

        # set a custom span attribute
        span.set_attribute("function.result", r)

        logger.info(f"Doubled random int to {r}")

        return r


# more endpoints to run trace across multiple hops
@app.get("/run2")
def run2(r: int):
    """Sets a custom field value to the double of input."""

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run2_custom_logic") as span:
        r //= 2

        # set a custom span attribute
        span.set_attribute("function.result", r)

        logger.info(f"Halved random int to {r}")

        return r
