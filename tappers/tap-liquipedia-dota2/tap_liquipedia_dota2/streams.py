"""Stream type classes for tap-liquipedia-dota2."""

from __future__ import annotations
from typing import Any, Dict, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_liquipedia_dota2.client import LiquipediaDota2Stream

class HeroesStream(LiquipediaDota2Stream):
    """Stream to get a list of Dota 2 Heroes main name"""

    name = "heroes"
    primary_keys = ["pageid"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("pageid", th.IntegerType),
        th.Property("ns", th.IntegerType),
        th.Property("title", th.StringType)
    ).to_dict()

    
    def get_url_params(self, context, next_page_token):
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Hero lore"
        }

        if next_page_token:
            # Next page token is a dict containing continue token
            params["cmcontinue"] = next_page_token["cmcontinue"]

        return params


    def parse_response(self, response) -> Iterable[dict]:
        data = response.json()
        for record in data.get("query", {}).get("categorymembers", []):
            record["title"] = record["title"].removesuffix("/Lore")

            # We only care getting a list of characters from mainstream Dota for now
            if not record["title"].endswith("/Dragon's Blood") and record["title"] != "User:Ecstasy Amphetamine/Sandbox":
                yield record


    def get_child_context(self, record, context):
        """Pass down hero names downstream to acquire further information"""
        return {
            "hero": record["title"]
        }
