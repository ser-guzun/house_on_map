import json

import requests
from behave import step

ROOT_URL = r"http://localhost:8000"


@step('I make POST request to "{path}" with body')
def make_post_request_step(context, path):
    body = json.loads(context.text or "{}")
    url = ROOT_URL + path
    context.response = requests.post(url, json=body)


@step("Response is {status_code:d}")
def assert_response_step(context, status_code):
    assert (
        context.response.status_code == status_code
    ), f"Expected {status_code}, got {context.response.status_code}"
