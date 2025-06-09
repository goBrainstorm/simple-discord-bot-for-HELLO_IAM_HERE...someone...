import discord
from discord.ext import commands, tasks
import asyncio
import logging
from datetime import datetime, timedelta
from config import DISCORD_TOKEN, VOICE_CHANNEL_ID, WAIT_TIME_MINUTES
from whatsapp_handler import WhatsAppHandler

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot Setup
intents = discord.Intents.default()
intents.voice_states = True  # Wichtig für Voice Channel Events
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
whatsapp = WhatsAppHandler()

# Dictionary um zu tracken, wer wann einem Voice Channel beigetreten ist
voice_join_times = {}

@bot.event
async def on_ready():
    logger.info(f'{bot.user} ist online und bereit!')
    logger.info(f'Überwache Voice Channel ID: {VOICE_CHANNEL_ID}')
    
    # Starte den Timer-Check-Task
    check_voice_timers.start()

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Wird ausgelöst, wenn sich der Voice-Status eines Users ändert
    (Beitritt, Verlassen, Mute, etc.)
    """
    
    # Überspringe Bots
    if member.bot:
        return
    
    # Überwache nur den spezifizierten Voice Channel
    target_channel_id = VOICE_CHANNEL_ID
    
    # User ist einem Voice Channel beigetreten
    if before.channel is None and after.channel is not None:
        if after.channel.id == target_channel_id:
            logger.info(f"{member.display_name} ist dem Voice Channel beigetreten")
            
            # Speichere Beitrittszeit
            voice_join_times[member.id] = {
                'username': member.display_name,
                'join_time': datetime.now(),
                'channel_id': after.channel.id,
                'notified': False
            }
    
    # User hat Voice Channel verlassen
    elif before.channel is not None and after.channel is None:
        if before.channel.id == target_channel_id and member.id in voice_join_times:
            logger.info(f"{member.display_name} hat den Voice Channel verlassen")
            
            # Entferne aus Tracking
            del voice_join_times[member.id]
    
    # User hat Channel gewechselt
    elif before.channel != after.channel:
        # Wenn User den überwachten Channel verlassen hat
        if before.channel and before.channel.id == target_channel_id and member.id in voice_join_times:
            logger.info(f"{member.display_name} hat den überwachten Voice Channel verlassen")
            del voice_join_times[member.id]

@tasks.loop(seconds=30)  # Überprüfe alle 30 Sekunden
async def check_voice_timers():
    """
    Überprüft regelmäßig, ob User lange genug im Voice Channel sind
    """
    current_time = datetime.now()
    wait_duration = timedelta(minutes=WAIT_TIME_MINUTES)
    
    users_to_notify = []
    
    for user_id, data in voice_join_times.items():
        # Überprüfe, ob genug Zeit vergangen ist und noch nicht benachrichtigt wurde
        if (current_time - data['join_time'] >= wait_duration and 
            not data['notified']):
            
            logger.info(f"Timer abgelaufen für {data['username']}")
            users_to_notify.append((user_id, data['username']))
            
            # Markiere als benachrichtigt
            voice_join_times[user_id]['notified'] = True
    
    # Sende WhatsApp-Nachrichten für alle fälligen User
    for user_id, username in users_to_notify:
        try:
            success = await whatsapp.send_message(username)
            if success:
                logger.info(f"WhatsApp-Nachricht für {username} erfolgreich versendet")
            else:
                logger.error(f"Fehler beim Versenden der WhatsApp-Nachricht für {username}")
        except Exception as e:
            logger.error(f"Unerwarteter Fehler bei WhatsApp-Nachricht für {username}: {e}")

@bot.command(name='status')
async def voice_status(ctx):
    """Debug-Befehl um aktuellen Voice Channel Status zu sehen"""
    if not voice_join_times:
        await ctx.send("Niemand wird aktuell im Voice Channel überwacht.")
        return
    
    status_msg = "**Aktuelle Voice Channel Überwachung:**\n"
    current_time = datetime.now()
    
    for user_id, data in voice_join_times.items():
        time_elapsed = current_time - data['join_time']
        minutes_elapsed = int(time_elapsed.total_seconds() / 60)
        
        status = "✅ Benachrichtigt" if data['notified'] else f"⏳ {minutes_elapsed}/{WAIT_TIME_MINUTES} Min"
        status_msg += f"• {data['username']}: {status}\n"
    
    await ctx.send(status_msg)

@bot.command(name='test_whatsapp')
async def test_whatsapp(ctx, *, username: str = None):
    """Test-Befehl für WhatsApp-Nachrichten"""
    if username is None:
        username = ctx.author.display_name
    
    await ctx.send(f"Teste WhatsApp-Nachricht für {username}...")
    
    try:
        success = await whatsapp.send_message(username)
        if success:
            await ctx.send("✅ WhatsApp-Nachricht erfolgreich geplant!")
        else:
            await ctx.send("❌ Fehler beim Senden der WhatsApp-Nachricht.")
    except Exception as e:
        await ctx.send(f"❌ Fehler: {e}")

# Bot Error Handler
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: {error}")
    await ctx.send(f"Ein Fehler ist aufgetreten: {error}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN ist nicht gesetzt!")
        exit(1)
    
    if not VOICE_CHANNEL_ID:
        logger.error("VOICE_CHANNEL_ID ist nicht gesetzt!")
        exit(1)
    
    logger.info("Starte Discord Bot...")
    bot.run(DISCORD_TOKEN) 