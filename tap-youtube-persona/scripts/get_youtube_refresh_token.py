# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-auth-oauthlib"
# ]
# ///

# Inline-dependencies Python script to save Google API token locally
# Run using `uv run get_youtube_refresh_token.py`
import os

import google_auth_oauthlib.flow

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


# TODO: Maybe adding DPoP in the future?
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secrets_file = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET_FILE_NAME", "YOUR_CLIENT_SECRET_FILE.json")

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(
        port=9797,
        prompt="consent"
    )

    print(f"Refresh Token: {credentials.refresh_token}")

if __name__ == "__main__":
    main()
