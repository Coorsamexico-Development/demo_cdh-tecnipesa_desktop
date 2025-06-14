from dotenv import load_dotenv, dotenv_values
from config.resource_path import resource_path

# Load the environment variables
load_dotenv()
config = dotenv_values(resource_path(".env"))

# Define the environment variables as module-level variables
apiUrl = config['API_URL']
apiIMPINJ = config['API_IMPINJ']
IMPINJ_USER = config['IMPINJ_USER']
IMPINJ_PASSWORD = config['IMPINJ_PASSWORD']
websocket_host = config['WEBSOCKET_HOST']
websocket_port = config['WEBSOCKET_PORT']

pusherAppId = config['PUSHER_APP_ID']
pusherAppkey = config['PUSHER_APP_KEY']
pusherCluster = config['PUSHER_APP_CLUSTER']
pusherSecret = config['PUSHER_APP_SECRET']
presetId= config['PRESET_ID']

# gcKeyFile = config['GOOGLE_CLOUD_KEY_FILE']
# gcProjectId = config['GOOGLE_CLOUD_PROJECT_ID']
# gcStorageBucket = config['GOOGLE_CLOUD_STORAGE_BUCKET']