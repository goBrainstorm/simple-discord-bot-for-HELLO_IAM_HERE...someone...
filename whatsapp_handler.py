import pywhatkit as kit
import time
import logging
from datetime import datetime, timedelta
from config import WHATSAPP_GROUP_ID, MESSAGE_FORMAT

logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.group_id = WHATSAPP_GROUP_ID
        
    async def send_message(self, username: str):
        """
        Sendet eine Nachricht an die WhatsApp-Gruppe
        
        WICHTIG: Diese Methode verwendet pywhatkit, welches WhatsApp Web automatisiert.
        Das bedeutet:
        1. WhatsApp Web muss im Browser eingeloggt sein
        2. Der Browser darf nicht minimiert sein
        3. Es ist etwas instabil und kann brechen
        
        Für Produktionsumgebungen sollte die offizielle WhatsApp Business API verwendet werden.
        """
        try:
            message = MESSAGE_FORMAT.format(username=username)
            
            # Berechne Zeit für sofortiges Senden (1 Minute in der Zukunft)
            now = datetime.now()
            send_time = now + timedelta(minutes=1)
            
            # pywhatkit erwartet Stunde und Minute
            hour = send_time.hour
            minute = send_time.minute
            
            logger.info(f"Plane WhatsApp-Nachricht für {username} um {hour}:{minute}")
            
            # Sende Nachricht über WhatsApp Web
            # ACHTUNG: Dies öffnet den Browser und automatisiert WhatsApp Web
            kit.sendwhatmsg_to_group(
                group_id=self.group_id,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=10,  # Wartezeit in Sekunden
                tab_close=True  # Schließt Tab nach dem Senden
            )
            
            logger.info(f"WhatsApp-Nachricht für {username} erfolgreich geplant")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Senden der WhatsApp-Nachricht: {e}")
            return False
    
    async def send_message_alternative(self, username: str):
        """
        Alternative Methode für WhatsApp Business API
        
        Diese Methode würde die offizielle WhatsApp Business API verwenden,
        welche stabiler und für Produktionsumgebungen geeignet ist.
        
        Benötigt:
        - WhatsApp Business Account
        - Verifizierte Telefonnummer
        - API-Schlüssel
        - Approved Message Templates
        """
        # Implementierung für WhatsApp Business API
        # Hier würde eine HTTP-Anfrage an die WhatsApp Business API gemacht
        pass 