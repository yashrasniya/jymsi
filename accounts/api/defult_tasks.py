
import django
from about_zymsi.models import GoogleLoginConfig
redirect_uri="http://localhost:3000/google/callback/"
client_id="549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com"
client_secret="MTB2VGfXaqx0iHLPfrWqgc6E"
try:
    if GoogleLoginConfig.objects.filter():
        GLC_obj=GoogleLoginConfig.objects.first()
    else:
        GLC_obj = GoogleLoginConfig.objects.create(
            client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
        )
except django.db.utils.OperationalError as e:
    print(e)
    GLC_obj=None