"""Stream type classes for tap-youtube-persona."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_youtube_persona.client import YoutubePersonaStream

# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class SubscriptionsStream(YoutubePersonaStream):
    """Extract user subscriptions data"""
    
    name = "subscriptions"
    path = "/subscriptions"
    primary_keys = ["id"]
    #replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("snippet", th.ObjectType(
            th.Property("title", th.StringType),
            th.Property("description", th.StringType),
            th.Property("resourceId", th.ObjectType(
                th.Property("channelId", th.StringType)
            ))
        ))
    ).to_dict()


    def get_http_request(self, *, page):
        request = super().get_http_request(page=page)
        request.params["part"] = "snippet"
        request.params["mine"] = "true"

        return request
    

class LikedVideosStream(YoutubePersonaStream):
    """Extract Liked Videos data"""

    name = "liked_videos"
    path = "/videos"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("snippet", th.ObjectType(
            th.Property("title", th.StringType),
            th.Property("categoryId", th.StringType)
        )),
        th.Property("contentDetails", th.ObjectType(
            th.Property("duration", th.StringType)
        ))
    ).to_dict()

    def get_http_request(self, *, page):
        request = super().get_http_request(page=page)
        request.params["part"] = "snippet,contentDetails"
        request.params["myRating"] = "like"
        
        return request
