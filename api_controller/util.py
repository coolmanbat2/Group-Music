from api_controller.credentials import CLIENT_ID, CLIENT_SECRET
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post


def get_user_tokens(session_key):
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_key, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_key)

    # converts into a Time Stamp, for better readability
    print("expires in value: " + str(expires_in) + "\n")
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    # If token was created into the database, update it
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                    'refresh_token', 'expires_in', 'token_type'])
    # Otherwise, create a new token
    else:
        tokens = SpotifyToken(user=session_key, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

# Takes in a session key and returns a boolean to determine if the user is authenitcated or not.


def is_auth(session_key):
    tokens = get_user_tokens(session_key)
    if tokens:
        expiry = tokens.expires_in
        # if the current time is expired, then reset the token.
        if expiry <= timezone.now():
            refresh_token(session_key)
        return True

    return False

# Given a token, return a refreshed token that allows the user to be authenticated.


def refresh_token(session_key):
    refresh_token = get_user_tokens(session_key).refresh_token

    response = post('https://acccounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }, headers={
        'Authorization': "Basic " + CLIENT_ID.encode('ascii') + ":" + CLIENT_SECRET.encode('ascii'),
        'Content-Type': "application/x-www-form-urlencoded"
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        session_key, access_token, token_type, expires_in, refresh_token)
