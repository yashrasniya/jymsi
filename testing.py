
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def send_sms_message(
        pinpoint_client, app_id, origination_number, destination_number, message,
        message_type):
    try:
        response = pinpoint_client.send_messages(
            ApplicationId=app_id,
            MessageRequest={
                'Addresses': {destination_number: {'ChannelType': 'SMS'}},
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message,
                        'MessageType': message_type,
                        # 'OriginationNumber': origination_number
                    }}})
    except ClientError:
        logger.exception("Couldn't send message.")
        raise
    else:
        return response['MessageResponse']['Result'][destination_number]['MessageId']


def main():
    app_id = "21d91c63ceae4c2db5eacc6d491992c6"
    origination_number = "+918938095294"
    destination_number = "+918938095294"
    message = (
        "This is a sample message sent from Amazon Pinpoint by using the AWS SDK for "
        "Python (Boto 3).")
    message_type = "TRANSACTIONAL"

    print("Sending SMS message.")
    message_id = send_sms_message(
        boto3.client('pinpoint',region_name='us-east-1',aws_access_key_id='AKIAU6PMEMPLLLNMFPTVCC',
                     aws_secret_access_key='zWiI8wfRtk+Oq3R+um5bMVe6S00/D3vojlPpULOgo1'), app_id, origination_number, destination_number,
        message, message_type)
    print(f"Message sent! Message ID: {message_id}.")


if __name__ == '__main__':
    main()
