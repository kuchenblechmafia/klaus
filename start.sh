#!/bin/sh

export KLAUS_SLACK_API_KEY=""
export KLAUS_SPOTIFY_PLAYLIST_USER=""
export KLAUS_SPOTIFY_PLAYLIST_ID=""
export KLAUS_SPOTIFY_API_CLIENT_ID=""
export KLAUS_SPOTIFY_API_CLIENT_SECRET=""
export KLAUS_SPOTIFY_API_CALLBACK_URL=""

./venv/bin/python slackklaus.py
