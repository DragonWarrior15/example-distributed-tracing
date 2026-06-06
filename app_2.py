"""Trivial instrumentation example."""

import logging
import sqlite3

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

        # get the square of this number from db
        s = get_square_from_db(r)

        span.set_attribute("function.square", s)

        logger.info(f"Square of random int is {s}")

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

def get_square_from_db(num: int) -> int:
    connection = sqlite3.connect("local_db_setup/local_db.db")
    cursor = connection.cursor()

    data = cursor.execute(f"SELECT square FROM squares where num = {num}")

    if not data:
        connection.close()
        return None
    
    for row in data:
        x = row[0]
        connection.close()
        return x
