#!/usr/bin/python
# coding: utf-8

import facebook
import urllib
import urlparse
import subprocess
import warnings

# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)


# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = 'XXXXXXXXXXXXXXX'
FACEBOOK_APP_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
FACEBOOK_PROFILE_ID = 'XXXXXX'


# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')

#Here we are getting this type of string: access_token=1182684665116824|v06FYJdsX4fOO3oJ4ELmllaJ1EQ
##	urllib.urlencode putting parameters from oauth_args in a nice URL style with & and ?	  
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]

##This send the request online to acutally get data. Not really sure how this cool stuff is working.
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

#This thing cleans oauth_response to get only the token. Very complex...
try:
    oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
except KeyError:
    print('Unable to grab an access token!')
    exit()

#Actuall authentification by facebook.
#Without doing all the above, insteed oauth_access_token get the token here as a text: https://developers.facebook.com/tools/explorer/
facebook_graph = facebook.GraphAPI(oauth_access_token)


# Try to post something on the wall of the profile 
try:
    fb_response = facebook_graph.put_wall_post('Hello from Python', \
                                               profile_id = FACEBOOK_PROFILE_ID)
    print fb_response
except facebook.GraphAPIError as e:
    print 'Something went wrong:', e.type, e.message