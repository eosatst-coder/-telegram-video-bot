"""
🎬 Telegram Video Downloader Bot
✅ رفع مباشر بدون تخزين محلي
✅ أعلى جودة متاحة
✅ يعمل على Render 24/7
"""

import os
import re
import uuid
import time
import telebot
import logging
from pathlib import Path
from io import BytesIO
import yt_dlp

# ============== إعدادات البوت ==============
TOKEN = os.environ.get("BOT_TOKEN", "8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4")

# ============== إعداد التسجيل ==============
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============== إنشاء البوت ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML', timeout=300)

# ============== مجلد التخزين المؤقت ==============
TEMP_DIR = Path("temp_videos")
TEMP_DIR.mkdir(exist_ok=True)

# ============== دوال المساعدة ==============
def download_video_direct(url: str):
    """تحميل الفيديو مباشرة"""
    temp_filename = TEMP_DIR / f"temp_{uuid.uuid4().hex}.mp4"
    
    try:
        # إعدادات yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': str(temp_filename),
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'retries': 5,
            'fragment_retries': 5,
        }
        
        # إعدادات خاصة لتيك توك
        if 'tiktok' in url:
            ydl_opts.update({
                'format': 'best',
                'referer': 'https://www.tiktok.com/',
                'extractor_args': {
                    'tiktok': {
                        'app_version': '29.0.0',
                        'manifest_app_version': '29.0.0',
                    }
                }
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if temp_filename.exists():
                return temp_filename
        
        return None
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        if temp_filename.exists():
            temp_filename.unlink()
        return None

# ============== معالجات الأوامر ==============
@bot.message_handler(commands=['start'])
def start_command(message):
    """أمر البدء البسيط"""
    welcome = "🚀 **مرحبا**\n\nأرسل رابط أي فيديو وسأرفعه لك مباشرة"
    bot.reply_to(message, welcome)

# ============== معالجة الروابط ==============
@bot.message_handler(func=lambda message: True)
def handle_video_url(message):
    """معالجة رابط الفيديو"""
    chat_id = message.chat.id
    url = message.text.strip()
    
    if url.startswith('/'):
        return
    
    if not re.match(r'^https?://', url):
        bot.reply_to(message, "❌ أرسل رابط صحيح")
        return
    
    # إرسال رسالة الانتظار
    wait_msg = bot.reply_to(message, "⏳ جاري التحميل...")
    
    try:
        # تحميل الفيديو
        video_file = download_video_direct(url)
        
        if not video_file or not video_file.exists():
            bot.edit_message_text("❌ فشل في تحميل الفيديو", chat_id, wait_msg.message_id)
            return
        
        # إرسال الفيديو
        with open(video_file, 'rb') as f:
            video_data = BytesIO(f.read())
            video_data.name = 'video.mp4'
            
            bot.send_video(
                chat_id,
                video_data,
                caption="✅ تم الرفع بنجاح",
                supports_streaming=True,
                timeout=300
            )
        
        bot.delete_message(chat_id, wait_msg.message_id)
        
        # حذف الملف المؤقت
        video_file.unlink()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.edit_message_text(f"❌ خطأ: {str(e)[:100]}", chat_id, wait_msg.message_id)

# ============== تنظيف الملفات المؤقتة ==============
def cleanup():
    """تنظيف الملفات المؤقتة"""
    try:
        for file_path in TEMP_DIR.glob("*"):
            file_path.unlink()
    except:
        pass

# ============== تشغيل البوت ==============
if __name__ == "__main__":
    print("🚀 البوت يعمل على Render...")
    cleanup()
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("🔄 إعادة التشغيل بعد 5 ثواني...")
            time.sleep(5)
            cleanup()
