"""LiquipediaDota2 tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_liquipedia_dota2 import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapLiquipediaDota2(Tap):
    """Singer tap for LiquipediaDota2."""

    name = "tap-liquipedia-dota2"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "user_agent",
            th.StringType(nullable=False),
            required=True,
            title="User Agent",
            description="User Agent description required by Liquipedia terms of uses",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            title="API URL",
            default="https://liquipedia.net/dota2",
            description="The base url for the Liquipedia API service",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.LiquipediaDota2Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.HeroesStream(self)
        ]


if __name__ == "__main__":
    TapLiquipediaDota2.cli()
