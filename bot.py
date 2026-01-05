"""
🎬 Telegram Video Downloader Bot
✅ يعمل 24/7 على Render
✅ يدعم يوتيوب، تيك توك، إنستقرام، وغيرها
✅ يدعم الفيديوهات حتى 48 ميجابايت
"""

import os
import re
import time
import telebot
import logging
from pathlib import Path
import yt_dlp

# ============== إعدادات البوت ==============
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("لم يتم تعيين BOT_TOKEN في متغيرات البيئة")

# ============== إعداد التسجيل ==============
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============== إنشاء البوت ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML', timeout=60)

# ============== مجلد التخزين المؤقت ==============
TEMP_DIR = Path("/tmp/temp_videos")
TEMP_DIR.mkdir(exist_ok=True, parents=True)
logger.info(f"مجلد التخزين المؤقت: {TEMP_DIR}")

# ============== دوال المساعدة ==============
def is_valid_url(url: str) -> bool:
    """التحقق من صحة الرابط"""
    valid_domains = [
        'youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com',
        'facebook.com', 'twitter.com', 'vimeo.com', 'dailymotion.com',
        'twitch.tv', 'reddit.com', 'pinterest.com'
    ]
    return any(domain in url.lower() for domain in valid_domains) and url.startswith('http')

def download_video(url: str):
    """تحميل الفيديو مباشرة"""
    try:
        video_id = re.sub(r'\W+', '', url.split('/')[-1])[:10]
        output_path = str(TEMP_DIR / f"{video_id}.mp4")
        
        # إعدادات yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4][height<=1080]/best[ext=mp4]/best',
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': False,
            'merge_output_format': 'mp4',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'socket_timeout': 180,
            'max_filesize': 48000000,  # 48MB
            'retries': 20,
            'fragment_retries': 20,
            'noplaylist': True,
            'verbose': True
        }
        
        # إعدادات خاصة لتيك توك
        if 'tiktok' in url.lower():
            ydl_opts.update({
                'format': 'best[ext=mp4][height<=1080]/best[ext=mp4]/best',
                'referer': 'https://www.tiktok.com/',
                'cookies': None,
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"جاري تحميل الفيديو من: {url}")
            info = ydl.extract_info(url, download=True)
            final_path = output_path
            
            # التأكد من وجود الملف
            if os.path.exists(final_path) and os.path.getsize(final_path) > 0:
                title = info.get('title', 'فيديو')
                logger.info(f"تم التحميل بنجاح: {title} - الحجم: {os.path.getsize(final_path)} bytes")
                return final_path, title
        
        logger.error("فشل التحميل: الملف غير موجود أو حجمه صفر")
        return None, None
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None, None

# ============== معالجات الأوامر ==============
@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    """أمر البدء"""
    welcome = """
🚀 **مرحباً!** أنا بوت تحميل الفيديوهات

📌 **أرسل روابط الفيديوهات مباشرة:**

🎬 فيديو يوتيوب
