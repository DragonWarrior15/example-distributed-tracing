"""Trivial instrumentation example."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from opentelemetry import trace

# create the logger
logger = logging.getLogger("uvicorn.error")

# create the app
app = FastAPI()

# set the tracer
tracer = trace.get_tracer(__name__)


# more endpoints to run trace across multiple hops
@app.post("/run1")
async def run1(request: Request) -> JSONResponse:
    """Sets a custom field value to the double of input."""

    # get r from request, this has to be awaited
    body = await request.json()
    # do a get only after awaited response is received
    r = body["r"]

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run1_custom_logic") as span:
        r *= 2

        # set a custom span attribute
        span.set_attribute("function.result", r)

        logger.info(f"Doubled random int to {r}")

        return JSONResponse(content={"r": r})


# more endpoints to run trace across multiple hops
@app.post("/run2")
async def run2(request: Request) -> JSONResponse:
    """Sets a custom field value to the double of input."""

    # get r from request, this has to be awaited
    body = await request.json()
    # do a get only after awaited response is received
    r = body["r"]

    # to see attributes from function, we need custom spans
    with tracer.start_as_current_span("route_run2_custom_logic") as span:
        r //= 2

        # set a custom span attribute
        span.set_attribute("function.result", r)

        logger.info(f"Halved random int to {r}")

        return JSONResponse(content={"r": r})
