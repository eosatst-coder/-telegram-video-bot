import os
import re
import uuid
import time
import telebot
import logging
import asyncio
import aiohttp
import subprocess
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
import yt_dlp

# ============== إعدادات البوت ==============
TOKEN = os.environ.get("BOT_TOKEN", "8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4")
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x]

# ============== إعدادات التسجيل ==============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============== إنشاء البوت ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML', timeout=300)

# ============== مجلد التخزين المؤقت ==============
TEMP_DIR = Path("temp_videos")
TEMP_DIR.mkdir(exist_ok=True)

# ============== دوال المساعدة ==============
def get_video_info(url):
    """الحصول على معلومات الفيديو"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # البحث عن أفضل تنسيق (أعلى جودة)
            formats = info.get('formats', [])
            best_format = None
            max_filesize = 0
            
            for fmt in formats:
                filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                if filesize and filesize > max_filesize:
                    max_filesize = filesize
                    best_format = fmt
            
            return {
                'title': info.get('title', 'فيديو'),
                'duration': info.get('duration', 0),
                'best_format': best_format,
                'filesize': max_filesize,
                'extractor': info.get('extractor_key', 'غير معروف'),
                'webpage_url': info.get('webpage_url', url)
            }
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        return None

def download_highest_quality(url, output_path):
    """تحميل الفيديو بأعلى جودة"""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(output_path),
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'continuedl': True,
        'noprogress': True,
        'concurrent_fragment_downloads': 5,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return output_path.exists() and output_path.stat().st_size > 0
    except Exception as e:
        logger.error(f"Download error: {e}")
        return False

def cleanup_temp_files():
    """تنظيف الملفات المؤقتة القديمة"""
    try:
        current_time = time.time()
        for file_path in TEMP_DIR.glob("*.mp4"):
            if file_path.stat().st_mtime < current_time - 3600:  # أقدم من ساعة
                file_path.unlink()
                logger.info(f"تم حذف الملف المؤقت: {file_path.name}")
    except Exception as e:
        logger.error(f"Error cleaning temp files: {e}")

# ============== معالجات الأوامر ==============
@bot.message_handler(commands=['start'])
def start_command(message):
    """أمر البدء البسيط"""
    welcome = """
🚀 **بوت تحميل الفيديوهات**

أرسل رابط الفيديو من:
• تيك توك
• يوتيوب
• انستجرام
• أي منصة أخرى

سأقوم بتحميله وإرساله لك بأعلى جودة
"""
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """عرض إحصائيات البوت"""
    if message.from_user.id not in ADMIN_IDS and ADMIN_IDS:
        return
    
    cleanup_temp_files()
    
    temp_files = list(TEMP_DIR.glob("*.mp4"))
    total_size = sum(f.stat().st_size for f in temp_files) / (1024*1024)
    
    stats_text = f"""
📊 **إحصائيات البوت**
    
📁 الملفات المؤقتة: {len(temp_files)}
💾 المساحة المستخدمة: {total_size:.2f} MB
🔄 آخر تنظيف: الآن
"""
    bot.reply_to(message, stats_text)

# ============== معالجة الروابط ==============
@bot.message_handler(func=lambda message: True)
def handle_video_url(message):
    """معالجة رابط الفيديو"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    url = message.text.strip()
    
    # التحقق من الرابط
    if not re.match(r'^https?://', url):
        bot.reply_to(message, "❌ أرسل رابط صحيح")
        return
    
    # إرسال رسالة الانتظار
    wait_msg = bot.send_message(chat_id, "🔍 جاري التحقق من الرابط...")
    
    try:
        # الحصول على معلومات الفيديو
        video_info = get_video_info(url)
        
        if not video_info:
            bot.edit_message_text("❌ لا يمكن تحميل هذا الفيديو", chat_id, wait_msg.message_id)
            return
        
        # التحقق من حجم الفيديو
        filesize_mb = video_info.get('filesize', 0) / (1024 * 1024)
        
        if filesize_mb < 50:  # أقل من 50 ميجا
            bot.edit_message_text("⚠️ الفيديو صغير الحجم (أقل من 50 ميجابايت)\nسيتم تحميله بأعلى جودة...", chat_id, wait_msg.message_id)
        elif filesize_mb > 2000:  # أكثر من 2 جيجا
            bot.edit_message_text("❌ الفيديو كبير جداً (أكثر من 2 جيجابايت)", chat_id, wait_msg.message_id)
            return
        
        # إعلام المستخدم بالبدء
        info_text = f"""
📹 **جاري تحميل الفيديو**

🎬 **العنوان:** {video_info['title'][:100]}
⏱ **المدة:** {video_info['duration'] // 60}:{video_info['duration'] % 60:02d}
📦 **الحجم التقريبي:** {filesize_mb:.1f} MB
🌐 **المصدر:** {video_info['extractor']}

⏳ قد تستغرق العملية بضع دقائق...
"""
        bot.edit_message_text(info_text, chat_id, wait_msg.message_id)
        
        # إنشاء اسم ملف مؤقت فريد
        temp_filename = TEMP_DIR / f"{uuid.uuid4().hex}.mp4"
        
        # تحميل الفيديو
        bot.edit_message_text("⬇️ جاري تحميل الفيديو بأعلى جودة...", chat_id, wait_msg.message_id)
        
        download_success = download_highest_quality(url, temp_filename)
        
        if not download_success or not temp_filename.exists():
            bot.edit_message_text("❌ فشل في تحميل الفيديو", chat_id, wait_msg.message_id)
            return
        
        # التحقق من حجم الملف المحمل
        actual_size = temp_filename.stat().st_size / (1024 * 1024)
        
        if actual_size < 1:  # أقل من 1 ميجا
            bot.edit_message_text("❌ الفيديو المحمل صغير جداً أو تالف", chat_id, wait_msg.message_id)
            temp_filename.unlink()
            return
        
        # إرسال الفيديو
        bot.edit_message_text("📤 جاري رفع الفيديو إلى تليجرام...", chat_id, wait_msg.message_id)
        
        try:
            with open(temp_filename, 'rb') as video_file:
                bot.send_video(
                    chat_id,
                    video_file,
                    caption=f"🎬 {video_info['title'][:200]}\n\n✅ تم التحميل بأعلى جودة",
                    supports_streaming=True,
                    timeout=300,
                    parse_mode='HTML'
                )
            
            # إرسال رسالة النجاح
            success_msg = f"""
✅ **تم رفع الفيديو بنجاح!**

📊 **معلومات الرفع:**
• 📦 الحجم الفعلي: {actual_size:.1f} MB
• ⚡ الجودة: أعلى جودة متاحة
• 💾 التخزين: مؤقت (سيتم حذفه تلقائياً)

🚀 لإرسال فيديو آخر، أرسل الرابط مباشرة
"""
            bot.edit_message_text(success_msg, chat_id, wait_msg.message_id)
            
        except Exception as send_error:
            logger.error(f"Error sending video: {send_error}")
            bot.edit_message_text(f"❌ خطأ في إرسال الفيديو: {str(send_error)[:100]}", chat_id, wait_msg.message_id)
        
        # حذف الملف المؤقت بعد الإرسال
        try:
            temp_filename.unlink()
            logger.info(f"تم حذف الملف المؤقت: {temp_filename.name}")
        except Exception as e:
            logger.error(f"Error deleting temp file: {e}")
    
    except Exception as e:
        logger.error(f"General error: {e}")
        bot.edit_message_text(f"❌ حدث خطأ غير متوقع: {str(e)[:150]}", chat_id, wait_msg.message_id)
        
        # تنظيف الملفات المؤقتة في حالة الخطأ
        cleanup_temp_files()
    
    finally:
        # تنظيف دوري للملفات القديمة
        cleanup_temp_files()

# ============== معالجة الأخطاء ==============
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_invalid(message):
    """معالجة الرسائل غير الصالحة"""
    if not message.text.startswith('/'):
        bot.reply_to(message, "📨 أرسل رابط فيديو فقط")

# ============== دالة للحفاظ على تشغيل البوت ==============
def keep_alive():
    """إرسال نبضات حياة للبوت"""
    while True:
        try:
            # إرسال أمر بسيط للحفاظ على النشاط
            bot.get_me()
            time.sleep(60)  # كل دقيقة
        except Exception as e:
            logger.error(f"Keep alive error: {e}")
            time.sleep(10)

# ============== تشغيل البوت ==============
def run_bot():
    """تشغيل البوت مع إعادة المحاولة"""
    print("=" * 60)
    print("🚀 بوت تحميل الفيديوهات بأعلى جودة")
    print("📦 يدعم الفيديوهات فوق 100 ميجابايت")
    print("⚡ يعمل على Render بشكل دائم")
    print("=" * 60)
    
    # بدء thread للحفاظ على النشاط
    import threading
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # التشغيل المستمر مع إعادة المحاولة
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔄 جاري تشغيل البوت...")
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ خطأ في البوت: {e}")
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ⏱ انتظر 10 ثواني ثم إعادة التشغيل...")
            time.sleep(10)
            
            # تنظيف الملفات المؤقتة عند إعادة التشغيل
            cleanup_temp_files()

if __name__ == "__main__":
    # تنظيف الملفات المؤقتة عند البدء
    cleanup_temp_files()
    
    # تشغيل البوت
    run_bot()
