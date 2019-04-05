'''
    PushBullet Notifications
    LACHLAN NEWMAN
'''

import json
import requests

class PushNotification:
    '''
    Object which is used to send notification
    via the pushbullet application
    '''
    ACCESS_TOKEN = "o.wmY4EKIUDwm3f1KeVnS43h9cfFRTXBHl"

    @staticmethod
    def send_notification_via_pushbullet(title, body):


        """ Sending notification via pushbullet.
            Args:
                title (str) : title of text.
                body (str) : Body of text.
        """


        data_send = {"type": "note", "title": title, "body": body}

        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                             headers={'Authorization': 'Bearer ' + PushNotification.ACCESS_TOKEN,
                                      'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')
        else:
            print('complete sending')
