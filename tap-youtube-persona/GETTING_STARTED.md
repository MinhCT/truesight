Simple step-by-step guide of how to run Youtube Persona Tap
## Prerequesites
Make sure your local environment already has the following:
- uv
- Python >= 3.10

## How-tos
1. Navigate to [Google Console](https://console.cloud.google.com).
2. Create new project if you have not already
3. Go to [Credentials Page](https://console.cloud.google.com/apis/credentials), create new OAuth 2.0 client, select Desktop App as client type
4. Save the client secret file somewhere safe locally, also the client ID and client secret value
5. Go to [APIs & Services Page](https://console.cloud.google.com/apis/dashboard), enable Youtube Data API V3
6. Grant a Python script permission to run:
```shell
chmod +x scripts/get_youtube_refresh_token.py
```
7. Run the script
```shell
uv sync
GOOGLE_OAUTH_CLIENT_SECRET_FILE_NAME=path_to_your_client_secret_file uv run scripts/get_youtube_refresh_token.py
```
8. Copy the printed refresh_token
9. Run:
```shell
cp .env.example .env

# Fill in the following information
# TAP_YOUTUBE_PERSONA_REFRESH_TOKEN
# TAP_YOUTUBE_PERSONA_GOOGLE_CLIENT_ID
# TAP_YOUTUBE_PERSONA_GOOGLE_CLIENT_SECRET
```
10. Finally run meltano to invoke the pipeline:
```shell
source .env
meltano install
meltano run tap-youtube-persona target-jsonl
```

That's it! The data is now pulled into `/output` folder
