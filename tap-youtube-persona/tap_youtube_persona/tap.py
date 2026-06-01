"""YoutubePersona tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_youtube_persona import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapYoutubePersona(Tap):
    """Singer tap for YoutubePersona."""

    name = "tap-youtube-persona"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "oauth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="OAuth Token",
            description="The token to authenticate against Youtube API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=True),
            description="The earliest record date to sync",
        ),
        th.Property(
            "youtube_api_url",
            th.StringType(nullable=False),
            title="API URL",
            default="https://youtube.googleapis.com/youtube/v3",
            description="The url for the API service",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.YoutubePersonaStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.SubscriptionsStream(self),
            streams.LikedVideosStream(self),
        ]


if __name__ == "__main__":
    TapYoutubePersona.cli()
