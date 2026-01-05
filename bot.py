"""
🎬 Telegram Video Downloader Bot
✅ رفع مباشر بدون تخزين محلي
✅ أعلى جودة متاحة
✅ يعمل على Render 24/7
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
bot = telebot.TeleBot(TOKEN, parse_mode='HTML', timeout=30)

# ============== مجلد التخزين المؤقت ==============
TEMP_DIR = Path("/tmp/temp_videos") if os.environ.get('RENDER') else Path("temp_videos")
TEMP_DIR.mkdir(exist_ok=True, parents=True)

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
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'socket_timeout': 120,  # زيادة وقت الانتظار
            'max_filesize': 48000000,  # 48MB - قرب الحد الأقصى لتليجرام
            'retries': 10,
            'fragment_retries': 10,
        }
        
        # إعدادات خاصة لتيك توك
        if 'tiktok' in url.lower():
            ydl_opts.update({
                'format': 'best[ext=mp4][height<=1080]/best[ext=mp4]/best',
                'referer': 'https://www.tiktok.com/',
                'cookies': None,
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            final_path = output_path
            
            # التأكد من وجود الملف
            if os.path.exists(final_path) and os.path.getsize(final_path) > 0:
                return final_path, info.get('title', 'فيديو')
        
        return None, None
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None, None

# ============== معالجات الأوامر ==============
@bot.message_handler(commands=['start'])
def start_command(message):
    """أمر البدء البسيط"""
    welcome = "🚀 **مرحباً!**\n\nأرسل رابط فيديو من:\n• يوتيوب\n• تيك توك\n• إنستقرام\n• فيسبوك\n• تويتر\n• ريديت\n• تويتش\n وغيرها\n\nسأقوم بتحميله لك بأعلى جودة ممكنة (حتى 48 ميجابايت)!"
    bot.reply_to(message, welcome)

# ============== معالجة الروابط ==============
@bot.message_handler(func=lambda message: True)
def handle_video_url(message):
    """معالجة رابط الفيديو"""
    chat_id = message.chat.id
    url = message.text.strip()
    
    # تجاهل الأوامر
    if url.startswith('/'):
        bot.reply_to(message, "❌ الأمر غير معروف. استخدم /start للبدء")
        return
    
    # التحقق من صحة الرابط
    if not re.match(r'^https?://', url):
        bot.reply_to(message, "❌ الرابط غير صالح. تأكد من كتابة رابط كامل يبدأ بـ http:// أو https://")
        return
    
    if not is_valid_url(url):
        bot.reply_to(message, "❌ هذا الموقع غير مدعوم حالياً. أرسل رابط فيديو من يوتيوب، تيك توك، إنستقرام، فيسبوك، أو تويتر")
        return
    
    # إرسال رسالة الانتظار
    wait_msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو... \n(قد يستغرق حتى 3 دقائق حسب حجم الفيديو)")

    try:
        # تحميل الفيديو
        video_file, title = download_video(url)
        
        if not video_file or not os.path.exists(video_file):
            bot.edit_message_text("❌ فشل في تحميل الفيديو. قد يكون الرابط غير صالح أو الفيديو كبير جداً.", chat_id, wait_msg.message_id)
            return
        
        file_size = os.path.getsize(video_file)
        if file_size > 50000000:  # 50MB limit for Telegram bots
            bot.edit_message_text("❌ الفيديو كبير جداً. الحد الأقصى المسموح به هو 50 ميجابايت.", chat_id, wait_msg.message_id)
            return
        
        # تقدير وقت الإرسال
        estimated_time = min(30, int(file_size / 1000000) + 5)
        
        # تحديث رسالة الانتظار
        bot.edit_message_text(f"✅ تم التحميل! جاري رفع الفيديو إلى تليجرام...\n(سيستغرق حوالي {estimated_time} ثانية)", chat_id, wait_msg.message_id)
        
        # إرسال الفيديو
        with open(video_file, 'rb') as f:
            video_message = bot.send_video(
                chat_id,
                f,
                caption=f"✅ {title[:50]}...",
                supports_streaming=True,
                timeout=300  # زيادة وقت الانتظار للإرسال
            )
        
        # حذف رسالة الانتظار
        bot.delete_message(chat_id, wait_msg.message_id)
        
        # إرسال معلومات إضافية
        file_size_mb = round(file_size / 1048576, 1)
        bot.reply_to(video_message, f"📦 حجم الفيديو: {file_size_mb} ميجابايت")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        error_msg = f"❌ حدث خطأ أثناء المعالجة: {str(e)[:100]}"
        if "413" in str(e) or "Request Entity Too Large" in str(e):
            error_msg = "❌ الفيديو كبير جداً. تليجرام يسمح بحد أقصى 50 ميجابايت للفيديوهات."
        bot.edit_message_text(error_msg, chat_id, wait_msg.message_id)
        
    finally:
        # حذف الملف المؤقت
        try:
            if 'video_file' in locals() and video_file and os.path.exists(video_file):
                os.remove(video_file)
        except Exception as e:
            logger.error(f"خطأ أثناء حذف الملف المؤقت: {e}")

# ============== تنظيف الملفات المؤقتة ==============
def cleanup():
    """تنظيف الملفات المؤقتة"""
    try:
        for file in TEMP_DIR.glob("*"):
            if time.time() - os.path.getmtime(file) > 3600:  # أقدم من ساعة
                if os.path.exists(file):
                    os.remove(file)
    except Exception as e:
        logger.error(f"خطأ أثناء التنظيف: {e}")

# ============== تشغيل البوت ==============
if __name__ == "__main__":
    print("🚀 البوت يعمل على Render...")
    
    # تنظيف عند البدء
    cleanup()
    
    # جدولة التنظيف الدوري (كل ساعة)
    last_cleanup = time.time()
    
    # تشغيل البوت مع إعادة المحاولة
    while True:
        try:
            # تنظيف دوري
            if time.time() - last_cleanup > 3600:
                cleanup()
                last_cleanup = time.time()
                
            bot.polling(none_stop=True, interval=1, timeout=120)
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("🔄 إعادة التشغيل بعد 5 ثواني...")
            time.sleep(5)
            cleanup()
