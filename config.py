import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
VOICE_CHANNEL_ID = int(os.getenv('VOICE_CHANNEL_ID', '0'))

# WhatsApp Configuration  
WHATSAPP_GROUP_ID = os.getenv('WHATSAPP_GROUP_ID')

# Bot Settings
WAIT_TIME_MINUTES = int(os.getenv('WAIT_TIME_MINUTES', '1'))
MESSAGE_FORMAT = "{username} ist on 🎧" 