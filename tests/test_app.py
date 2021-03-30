#!/usr/bin/env python
from app import app
import logging


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"html" in response.data
