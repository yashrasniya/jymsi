
import django
from about_zymsi.models import GoogleLoginConfig
redirect_uri="http://localhost:3000/google/callback/"
redirect_uri_partner="https://partner.zymsi.com/google/callback/"
client_id="549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com"
client_secret="MTB2VGfXaqx0iHLPfrWqgc6E"
def google_login():
    try:
        if GoogleLoginConfig.objects.filter():
            return GoogleLoginConfig.objects.first()
        else:
            return GoogleLoginConfig.objects.create(
                client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            redirect_uri_partner=redirect_uri_partner
            )
    except django.db.utils.OperationalError as e:
        print(e)
        return None