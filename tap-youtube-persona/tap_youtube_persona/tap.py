"""YoutubePersona tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_youtube_persona import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class TapYoutubePersona(Tap):
    """Singer tap for YoutubePersona."""

    name = "tap-youtube-persona"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "refresh_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="OAuth Refresh Token",
            description="The refresh token that Tap will use to acquire access token to request to Youtube API",
        ),
        th.Property(
            "google_client_id",
            th.StringType(nullable=False),
            required=True,
            secret=True,
            title="Google Console Client ID",
            description="A client ID created from Google Console"
        ),
        th.Property(
            "google_client_secret",
            th.StringType(nullable=False),
            required=True,
            secret=True,
            title="Google Console Client Secret",
            description="A client secret created from Google Console"
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._obtain_fresh_access_token()


    def _obtain_fresh_access_token(self):
        """Automatically refresh Google access token if expired"""
        self.logger.info("Obtaining Google access token to use in pipeline...")
        for k,v in self.config.items():
            self.logger.info(f"{k}: {v}")
        try:
            self.logger.info(f"Reading refresh token from config: {self.config["refresh_token"]}")
            creds = Credentials(
                token=None,
                refresh_token=self.config["refresh_token"],
                client_id=self.config["google_client_id"],
                client_secret=self.config["google_client_secret"],
                token_uri="https://oauth2.googleapis.com/token"
            )

            if not creds.valid:
                creds.refresh(Request())

            self.access_token = creds.token
            self.logger.info("Google access token retrieved successfully!")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve Google access token: {e}")


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
