import json
import urllib
from urllib import request
from urllib.error import HTTPError


class PushyAPI:

    @staticmethod
    def sendPushNotification(data, to, options, api_key):
        # Insert your Pushy Secret API Key here
        # Default post data to provided options or empty object
        postData = options or {}

        # Set notification payload and recipients
        postData["to"] = to
        postData["data"] = data

        # Set URL to Send Notifications API endpoint
        req = request.Request('https://api.pushy.me/push?api_key=' + api_key)

        # Set Content-Type header since we're sending JSON
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(postData)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        try:
            # Actually send the push
            request.urlopen(req, jsondataasbytes)
            # urlopen(req.full_url + json.dumps(postData))
        except HTTPError as e:
            # Print response errors
            print("Pushy API returned HTTP error " + str(e.code) + ": " + str(e))
            print(str(jsondata))
