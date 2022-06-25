"""
https://httpdebugger.com/Tools/ViewHttpHeaders.aspx
"""

import logging

import requests


import json
from bs4 import BeautifulSoup


_logger = logging.getLogger(f"--> {__name__}  ")


def http_request(
    method: str, url: str, data: dict = None, headers: dict = None, timeout=10
):
    """send http request by httpdebugger.com proxy"""

    ContentDataBox = ""
    if data:
        for key, value in data.items():
            ContentDataBox += f"{key}={value}&"

    HeadersBox = ""
    if headers:
        for key, value in headers.items():
            HeadersBox += f"{key}: {value},"

    payload = {
        "MethodList": method,
        "UrlBox": url,
        "ContentDataBox": ContentDataBox,
        "HeadersBox": HeadersBox,
        "AgentList": "Mozilla Firefox",
        "VersionsList": "HTTP/1.1",
    }

    try:
        response = requests.post(
            url="https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx",
            data=payload,
            timeout=timeout,
        )

        if response.status_code == 200:
            _logger.debug("httpdebugger.response: 200")

            try:
                # clean response body
                response_source = response.text
                response_source = BeautifulSoup(response_source, "html.parser")
                response_source = response_source.find(
                    "div", id="ResultData"
                ).text.strip()
                response_source = response_source.replace("Response Content", "")
                response_source = response_source.replace("edited_message", "message")
                response_source = json.loads(response_source)["result"]
                return response_source

            except Exception as error:
                _logger.debug(f"clean response, error: {error}")
                return False

        else:
            _logger.debug(f"error, httpdebugger.response: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        _logger.debug(f"error: timeout ")
        return False

    except:
        _logger.debug(f"Unknown error")
        return False
