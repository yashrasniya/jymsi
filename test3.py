from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    scopes=["https://www.googleapis.com/auth/userinfo.profile "])

flow.run_local_server()

session = flow.authorized_session()

profile_info = session.get(
    'https://www.googleapis.com/userinfo/v2/me').json()

print(profile_info)