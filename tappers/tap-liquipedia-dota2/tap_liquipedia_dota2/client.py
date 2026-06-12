"""REST client handling, including LiquipediaDota2Stream base class."""

from __future__ import annotations

import time
import decimal
import sys
from typing import TYPE_CHECKING, Any, ClassVar

from singer_sdk import SchemaDirectory, StreamSchema
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

from tap_liquipedia_dota2 import schemas

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable

    import requests
    from singer_sdk.helpers.types import Context
    from singer_sdk.streams.rest import HTTPRequest, PageContext


class LiquipediaPaginator(BaseAPIPaginator):
    def get_next(self, response):
        data = response.json()
        if data.get("continue") is None:
            return None
        return data.get("continue")


class LiquipediaDota2Stream(RESTStream):
    """LiquipediaDota2 stream class."""

    path = "/api.php"

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        if self.config["api_url"]:
            return self.config["api_url"]
        return "https://liquipedia.net/dota2"

    @property
    @override
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # Adding gzip encoding to adhere to Liquipedia's terms of uses
        headers = { "Accept-Encoding": "gzip" }
        if self.config["user_agent"]:
            headers["User-Agent"] = self.config["user_agent"]
        return headers

    @override
    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        return LiquipediaPaginator(start_value=None)

    @override
    def get_http_request(self, *, page: PageContext[Any]) -> HTTPRequest:
        """Return a request object for this stream.

        Args:
            page: An object containing the stream partition or context dictionary,
                and the next page token if applicable.

        Returns:
            An HTTP request for this stream.
        """
        request = super().get_http_request(page=page)
        request.params["format"] = "json"
        request.params["formatversion"] = "2"

        if self.replication_key:
            request.params["sort"] = "asc"
            request.params["order_by"] = self.replication_key

        # Optionally, add the payload for a POST request
        # request.data = ...
        return request

    @override
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    @property
    def request_decorator(self):
        base_decorator = super().request_decorator

        def rate_limited_decorator(*args, **kwargs):
            """Enforce Liquipedia rate limit: Only one request made every 2 seconds"""
            self.logger.info("Sleeping for 2 seconds before making next request")
            time.sleep(2.1) # 0.1s lag to make sure
            return base_decorator(*args, **kwargs)
        
        return rate_limited_decorator
