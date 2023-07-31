import random
import binascii
import base64
from django.core.files.base import ContentFile
import datetime


def image_add_db(file_array, validated_data,instance=None):
    for i in file_array:
        if validated_data.get(i, ''):

            image_data = validated_data.get(i)
            if image_data=='none':
                file_array[i].delete()
                # instance.save()
            else:
                try:
                    data = ContentFile(base64.b64decode(image_data))
                except binascii.Error as e:
                    print(e)
                    raise binascii.Error(f'{i} send data is in incorrect format it should be in bash 64')
                file_name = str(datetime.datetime.now()) + '.' + 'png'
                file_array[i].save(file_name, data, save=True)
