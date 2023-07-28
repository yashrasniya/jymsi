import requests
from django.core.files.base import ContentFile
import logging
import boto3
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)



def get_empty_dict():
    return {}


def send_sms_message(
        pinpoint_client, app_id, destination_number, message,
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

def send_sms(destination_number, otp):

    # url = "https://2factor.in/API/V1/b9214bc2-f013-11ed-addf-0200cd936042/SMS/+91" + number + "/" + otp + "/123"
    # requests.get(url)
    region = "us-east-1"

    project_id = "21d91c63ceae4c2db5eacc6d491992c6"
    message_type = "TRANSACTIONAL"
    message = (f"your otp is {otp}!")

    message_id=send_sms_message(
        boto3.client('pinpoint',region_name=region,
                     aws_access_key_id='AKIAU6PMEMPLLLNMFPTV',
                     aws_secret_access_key='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'),
        project_id, f'+91{destination_number}',
        message, message_type)
    print(message_id)


def get_file_content_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content, name=url.split('/')[-1])  # this is the content of file

    raise Exception("Error while retrieving file from url:" + url)

default_error_msg = {
    'NO_PAYOUT_ACCOUNT' : "Please add bank account.",
    'CANNOT_RETURN_ORDER': 'Order cannot be returned.',
    'PAYOUT_ACCOUNT_CREATE_ERROR': 'Something went wrong while adding account. Please try again!',
    'PAYOUT_ACCOUNT_CREATE_SUCCESS': 'Account added successfully',
    'FIELD_MISSING_ERROR': r'Fill {{FIELD_NAME}} field.'
}