# AZURE App Information
CLIENT_ID = "98145980-4a60-455a-9699-eacf4d339ee8" # Application (client) ID of app registration

CLIENT_SECRET = "yDVk163PQZm_hs_oU0~3hZHn~g-.FZ9Jxa" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

# AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITY = "https://login.microsoftonline.com/935ddf29-4b2b-4c23-8b83-b4dd0645ca6b"

REDIRECT_PATH = "/getAADToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
# SCOPE = ["User.ReadBasic.All"]
SCOPE = []

# MobileIron Configuration
API_TOKEN = "dmNydXotZW1tYWRtaW5AbW9iaWxlaXJvbi5jb206TWk0TWFuMTE="
UEMHOST = "https://na2.mobileiron.com"
MI_API = {"Cloud": "/api/v1", "Core": "/api/v2", "Connected Cloud": "/rest/api/v2"}
MI_API_URL = UEMHOST + MI_API.get("Cloud")
AUTH_HEADERS = {
    'Authorization': f'Basic {API_TOKEN}'
}
VERSION = "0.2b"
