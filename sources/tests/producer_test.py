import pytest
import json


def test_basic_route(app, client):
    response = client.get("/")
    assert response.status_code == 404, f"Something went wrong if you didn't get 404 response: {response.status_code}"
    assert response.json['message'] == "not supported", f"Response body is: {response.json['message']}"


# def test_url_converter_endpoint(app, client):
#     response = client.post("/api/v1/url-converter", )