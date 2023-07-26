import requests
from django.core.files.base import ContentFile


def get_empty_dict():
    return {}


def send_sms(number, otp):
    url = "https://2factor.in/API/V1/b9214bc2-f013-11ed-addf-0200cd936042/SMS/+91" + number + "/" + otp + "/"
    requests.get(url)


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