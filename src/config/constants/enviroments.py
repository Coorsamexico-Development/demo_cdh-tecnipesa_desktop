from dotenv import load_dotenv, dotenv_values

# Load the environment variables
load_dotenv()
config = dotenv_values(".env")

# Define the environment variables as module-level variables
apiUrl = config['API_URL']
# pusherAppId = config['PUSHER_APP_ID']
# pusherAppkey = config['PUSHER_APP_KEY']
# pusherCluster = config['PUSHER_APP_CLUSTER']

# gcKeyFile = config['GOOGLE_CLOUD_KEY_FILE']
# gcProjectId = config['GOOGLE_CLOUD_PROJECT_ID']
# gcStorageBucket = config['GOOGLE_CLOUD_STORAGE_BUCKET']