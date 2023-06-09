import logging
import os
import telegram
from telegram.ext import CommandHandler, Updater
from pytube import YouTube
from moviepy.editor import *
from Token_Api import APItoken

# Set the logging level to display errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Specify HTTP bot token and enable update with user messages
os.environ['TELEGRAM_TOKEN'] = APItoken
updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a bot for downloading an audio track from a YouTube video. Just send me the link to the video and I'll send you the audio file.")

def download(update, context):
    url = context.args[0]
    yt = YouTube(url)

    video_formats = yt.streams.filter(file_extension='mp4').all()
    video = video_formats[0]

    video.download()
    
    video_file = VideoFileClip(video.default_filename)
    audio = video_file.audio
    
    audio_filename = f"{yt.title}.mp3"
    audio.write_audiofile(audio_filename)
    
    os.remove(video.default_filename)
    
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_filename, 'rb'))
    
    os.remove(audio_filename)

start_handler = CommandHandler('start', start)
download_handler = CommandHandler('download', download)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(download_handler)

updater.start_polling()
