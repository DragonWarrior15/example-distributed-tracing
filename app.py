"""Trivial instrumentation example."""

import logging
import random

from fastapi import FastAPI

# create the logger
logger = logging.getLogger("uvicorn.error")

# create the app
app = FastAPI()


@app.get("/run")
def run():
    """Generate a random number and return the response."""
    r = random.randint(1, 20)
    logger.info(f"Generated random int {r}")
    return r
