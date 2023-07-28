import google.oauth2.credentials
import google_auth_oauthlib.flow
#
# # Use the client_secret.json file to identify the application requesting
# # authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile'],)
# # https://accounts.google.com/o/oauth2/v2/auth
# # https://accounts.google.com/o/oauth2/v2/auth?
# # client_id=549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com
# # redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F
# # scope=profile+email
# # &response_type=code&
# # state=xLTMs8ciNbQV&
# # access_type=online
# # http://127.0.0.1:8000/?state=QdaNwm5SjkSK7Cwt7md5eTSNjOLt5k&code=4%2F0AZEOvhUhijcyAlr2mTHJPrL-TU3SDHanlmRbxCtFhlmprktZ8XCThmSmZvaY5ECdilKUPQ&scope=profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile
# # Indicate where the API server will redirect the user after the user completes
# # the authorization flow. The redirect URI is required. The value must exactly
# # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# # configured in the API Console. If this value doesn't match an authorized URI,
# # you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = 'http://127.0.0.1:8000/accounts/google/login/callback/'
flow.redirect_uri = 'http://localhost:8080/'


authorization_url, state = flow.authorization_url(

    access_type='online',

)

print(authorization_url,state)
# print(flow.client_config)
# pp=flow.fetch_token(code='0AZEOvhUs99fUSD-Tsm-pG8n3c_2Wu5Vob2iqrQtMNCscXVfMaoKhrdihrSTgin7t-yxiFg')
# print(pp)
#
# # https://accounts.google.com/o/oauth2/v2/auth?client_id=549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=profile+email&response_type=code&state=xLTMs8ciNbQV&access_type=online

import requests
req=requests.post("https://oauth2.googleapis.com/token",
    data={"code": "4/0AZEOvhU_Wo0UREkoHjoLUAon8fOfPCPDMNtHZmpKv_ApBkFxWH4K3PPj05RVrIMUawJxXw",
            "client_id":"549026914943-7v02pt7ng4kt8kiq1ecpsmolo1k1413b.apps.googleusercontent.com",
            "client_secret":"MTB2VGfXaqx0iHLPfrWqgc6E",
            "redirect_uri":"http://localhost:8080/",
            "grant_type":"authorization_code",
            },
    headers = {"content-type": "application/x-www-form-urlencoded"}
                  )

print(req.text)

