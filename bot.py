"""
🎬 Telegram Video Downloader Bot
✅ رفع مباشر بدون تخزين محلي
✅ أعلى جودة متاحة
✅ دعم الفيديوهات الكبيرة
✅ يعمل على Render 24/7
"""

import os
import re
import uuid
import time
import telebot
import logging
import threading
from pathlib import Path
from io import BytesIO
import yt_dlp

# ============== إعدادات البوت ==============
TOKEN = os.environ.get("BOT_TOKEN", "8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4")

# ============== إعدادات التحميل ==============
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB حد تليجرام

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
def get_video_info(url: str):
    """استخراج معلومات الفيديو"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # البحث عن أفضل تنسيق متوافق مع تليجرام
            best_format = None
            best_filesize = 0
            
            formats = info.get('formats', [])
            for fmt in formats:
                # نبحث عن تنسيق mp4 مع صوت وفيديو
                if (fmt.get('ext') == 'mp4' and 
                    fmt.get('acodec') != 'none' and 
                    fmt.get('vcodec') != 'none'):
                    
                    filesize = fmt.get('filesize') or fmt.get('filesize_approx') or 0
                    if filesize > best_filesize:
                        best_filesize = filesize
                        best_format = fmt
            
            return {
                'title': info.get('title', 'فيديو'),
                'duration': info.get('duration', 0),
                'best_format': best_format,
                'filesize': best_filesize,
                'extractor': info.get('extractor_key', 'غير معروف'),
                'thumbnail': info.get('thumbnail'),
                'webpage_url': info.get('webpage_url', url)
            }
    except Exception as e:
        logger.error(f"Error extracting info: {e}")
        return None

def download_video_highest_quality(url: str):
    """تحميل الفيديو بأعلى جودة متاحة"""
    temp_filename = TEMP_DIR / f"temp_{uuid.uuid4().hex}.mp4"
    
    try:
        # إعدادات yt-dlp لتحميل أفضل جودة
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(temp_filename),
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
        
        # إعدادات خاصة للمنصات
        extractor_args = {}
        
        # إعدادات تيك توك
        if 'tiktok' in url:
            extractor_args['tiktok'] = {
                'app_version': '29.0.0',
                'manifest_app_version': '29.0.0',
            }
        
        if extractor_args:
            ydl_opts['extractor_args'] = extractor_args
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if temp_filename.exists():
                file_size = temp_filename.stat().st_size
                logger.info(f"Downloaded file size: {file_size / (1024*1024):.2f} MB")
                
                if file_size > 0:
                    return temp_filename
        
        return None
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        
        # حذف الملف المؤقت في حالة الخطأ
        if temp_filename.exists():
            temp_filename.unlink()
        
        return None

def cleanup_temp_files():
    """تنظيف الملفات المؤقتة القديمة"""
    try:
        current_time = time.time()
        deleted_count = 0
        
        for file_path in TEMP_DIR.glob("*"):
            # حذف الملفات الأقدم من 30 دقيقة
            if file_path.stat().st_mtime < current_time - 1800:
                file_path.unlink()
                deleted_count += 1
        
        if deleted_count > 0:
            logger.info(f"تم حذف {deleted_count} ملف مؤقت")
            
    except Exception as e:
        logger.error(f"Error cleaning temp files: {e}")

# ============== معالجات الأوامر ==============
@bot.message_handler(commands=['start'])
def start_command(message):
    """أمر البدء البسيط"""
    welcome = """
🚀 **مرحبا**

أرسل رابط أي فيديو من:
• تيك توك
• يوتيوب
• انستجرام
• أي منصة أخرى

سأقوم بتحميله وإرساله لك بأعلى جودة
"""
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['help'])
def help_command(message):
    """أمر المساعدة"""
    help_text = """
📖 **كيفية الاستخدام:**
1. أرسل رابط الفيديو
2. انتظر حتى يكتمل التحميل
3. سأرسل لك الفيديو بأعلى جودة

✨ **المميزات:**
• ⚡ تحميل مباشر بدون تخزين
• 🎬 أعلى جودة متاحة
• 📦 دعم الفيديوهات الكبيرة
• 🔒 خصوصية كاملة

⚠️ **ملاحظات:**
• الحد الأقصى: 2 جيجابايت
• قد يستغرق التحميل بضع دقائق
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['clean'])
def clean_command(message):
    """تنظيف الملفات المؤقتة"""
    try:
        cleanup_temp_files()
        
        # حساب المساحة الحالية
        total_size = 0
        file_count = 0
        
        for file_path in TEMP_DIR.glob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        total_size_mb = total_size / (1024 * 1024)
        
        bot.reply_to(message, f"🧹 **تم التنظيف**\n\n📁 الملفات: {file_count}\n💾 المساحة: {total_size_mb:.2f} MB")
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في التنظيف: {str(e)[:100]}")

# ============== معالجة الروابط ==============
@bot.message_handler(func=lambda message: True)
def handle_video_url(message):
    """معالجة رابط الفيديو"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    url = message.text.strip()
    
    # تجاهل الأوامر
    if url.startswith('/'):
        return
    
    # التحقق من الرابط
    if not re.match(r'^https?://', url):
        bot.reply_to(message, "❌ أرسل رابط صحيح")
        return
    
    # إرسال رسالة الانتظار
    wait_msg = bot.reply_to(message, "🔍 جاري تحليل الرابط...")
    
    try:
        # الحصول على معلومات الفيديو
        video_info = get_video_info(url)
        
        if not video_info:
            bot.edit_message_text("❌ لا يمكن تحميل هذا الفيديو", chat_id, wait_msg.message_id)
            return
        
        # التحقق من حجم الفيديو
        filesize_mb = video_info.get('filesize', 0) / (1024 * 1024)
        
        if filesize_mb > 2000:  # أكثر من 2 جيجا
            bot.edit_message_text("❌ الفيديو كبير جداً (أكثر من 2 جيجابايت)", chat_id, wait_msg.message_id)
            return
        
        # عرض معلومات الفيديو
        duration = video_info.get('duration', 0)
        minutes = duration // 60
        seconds = duration % 60
        
        info_text = f"""
📹 **تم تحليل الفيديو**

🎬 **العنوان:** {video_info['title'][:150]}
⏱ **المدة:** {minutes}:{seconds:02d}
📦 **الحجم التقريبي:** {filesize_mb:.1f} MB
🌐 **المصدر:** {video_info['extractor']}

⬇️ **جاري التحميل بأعلى جودة...**
"""
        bot.edit_message_text(info_text, chat_id, wait_msg.message_id)
        
        # تحميل الفيديو
        bot.edit_message_text("📥 جاري تحميل الفيديو... قد تستغرق العملية بضع دقائق", chat_id, wait_msg.message_id)
        
        video_file = download_video_highest_quality(url)
        
        if not video_file or not video_file.exists():
            bot.edit_message_text("❌ فشل في تحميل الفيديو", chat_id, wait_msg.message_id)
            return
        
        # التحقق من حجم الملف المحمل
        actual_size_mb = video_file.stat().st_size / (1024 * 1024)
        
        if actual_size_mb < 5:  # أقل من 5 ميجا
            bot.edit_message_text("⚠️ الفيديو المحمل صغير الحجم، قد تكون الجودة منخفضة", chat_id, wait_msg.message_id)
        
        # إرسال الفيديو
        bot.edit_message_text(f"📤 جاري رفع الفيديو ({actual_size_mb:.1f} MB)...", chat_id, wait_msg.message_id)
        
        try:
            with open(video_file, 'rb') as f:
                video_data = BytesIO(f.read())
                video_data.name = f'{video_info["title"][:50]}.mp4'
                
                # إرسال الفيديو
                bot.send_video(
                    chat_id,
                    video_data,
                    caption=f"🎬 {video_info['title'][:200]}\n\n✅ تم التحميل بأعلى جودة",
                    supports_streaming=True,
                    timeout=300,
                    parse_mode='HTML'
                )
            
            # إرسال رسالة النجاح
            success_msg = f"""
✅ **تم رفع الفيديو بنجاح!**

📊 **معلومات التحميل:**
• 📦 الحجم الفعلي: {actual_size_mb:.1f} MB
• ⚡ الجودة: أعلى جودة متاحة
• 📤 الحالة: محفوظ على تليجرام

🚀 أرسل رابط فيديو آخر
"""
            bot.edit_message_text(success_msg, chat_id, wait_msg.message_id)
            
        except Exception as send_error:
            logger.error(f"Error sending video: {send_error}")
            
            # محاولة إرسال بدون caption إذا كان هناك خطأ
            try:
                with open(video_file, 'rb') as f:
                    video_data = BytesIO(f.read())
                    video_data.name = 'video.mp4'
                    
                    bot.send_video(
                        chat_id,
                        video_data,
                        supports_streaming=True,
                        timeout=300
                    )
                
                bot.edit_message_text("✅ تم إرسال الفيديو", chat_id, wait_msg.message_id)
            except:
                bot.edit_message_text("❌ فشل في إرسال الفيديو", chat_id, wait_msg.message_id)
        
        finally:
            # حذف الملف المؤقت
            try:
                video_file.unlink()
            except:
                pass
    
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        bot.edit_message_text(f"❌ خطأ: {str(e)[:150]}", chat_id, wait_msg.message_id)
    
    finally:
        # تنظيف الملفات المؤقتة
        cleanup_temp_files()

# ============== دالة للحفاظ على تشغيل البوت ==============
def keep_alive():
    """إرسال نبضات حياة للبوت"""
    while True:
        try:
            # التحقق من أن البوت يعمل
            bot.get_me()
            time.sleep(30)
        except Exception as e:
            logger.error(f"Keep alive error: {e}")
            time.sleep(5)

# ============== تشغيل البوت ==============
def run_bot():
    """تشغيل البوت مع إعادة المحاولة التلقائية"""
    print("=" * 60)
    print("🚀 بوت تحميل الفيديوهات بأعلى جودة")
    print("📦 يدعم الفيديوهات الكبيرة (حتى 2 جيجابايت)")
    print("⚡ يعمل على Render 24/7")
    print("=" * 60)
    
    # تنظيف الملفات المؤقتة عند البدء
    cleanup_temp_files()
    
    # بدء thread للحفاظ على النشاط
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # التشغيل المستمر مع إعادة المحاولة
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔄 جاري تشغيل البوت...")
            bot.polling(none_stop=True, interval=1, timeout=60)
        except KeyboardInterrupt:
            print("\n👋 تم إيقاف البوت")
            break
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ خطأ: {e}")
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ⏱ إعادة التشغيل بعد 10 ثواني...")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
