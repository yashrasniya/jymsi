import requests
import json
#
# serverToken = 'AAAAf9SN4n8:APA91bG5jw7bqA-pPYCZ_FJTRJsXvdgCxKUbJaOR19OCAmnUKXE8Q_4cq3nNPuDcyUd54FiqOC4YPXq4l4OKJTAFWQ_GqLlQTMNKwj4YV3A53URX5q0KULJLhqLbTl3ZCNyW3L7V-UoK'
# deviceToken = '1234'
#
# headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'key=' + serverToken,
#       }
#
# body = {
#           'notification': {'title': 'Sending push form python script',
#                             'body': 'New Message'
#                             },
#           'to':
#               deviceToken,
#           'priority': 'high',
#         #   'data': dataPayLoad,
#         }
# response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
# print(response.status_code)
#
# print(response.json())

resp = requests.post('https://textbelt.com/text', {
            'phone': f'{+918938095294}',
            'message': f'hi how are u',
            'key': 'textbelt',
        })

print(resp.json())