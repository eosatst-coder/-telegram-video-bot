"""
🎬 Telegram Video Bot - Render Hosting
✅ 24/7 Online | ✅ Real Upload | ✅ All Platforms
"""

import os
import time
import telebot
import requests
import urllib3
import tempfile
import threading
import re
import traceback
from flask import Flask
from threading import Thread
from io import BytesIO
import yt_dlp

# ============== CONFIG ==============
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4')
PORT = int(os.environ.get('PORT', 10000))
MAX_VIDEOS_PER_PLAYLIST = 10  # زيادة الحد لـ 10 فيديوهات

print("=" * 60)
print("🎬 Telegram Video Bot - Render Hosting")
print("=" * 60)
print(f"🤖 Token: {TOKEN[:15]}...")
print(f"🌐 Port: {PORT}")

# ============== FLASK WEB SERVER ==============
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Video Bot</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }}
            h1 {{ color: #333; margin-bottom: 20px; }}
            .status {{ color: #4CAF50; font-size: 24px; margin: 20px 0; font-weight: bold; }}
            .bot-link {{
                display: inline-block;
                background: #0088cc;
                color: white;
                padding: 12px 30px;
                border-radius: 50px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Video Bot</h1>
            <div class="status">✅ ONLINE & WORKING</div>
            <p>Bot: @ishdmvfvzobot</p>
            <p>Host: Render.com</p>
            <p>Time: {time.ctime()}</p>
            <a href="https://t.me/ishdmvfvzobot" class="bot-link" target="_blank">
                🚀 Open in Telegram
            </a>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============== VIDEO DOWNLOAD FUNCTIONS ==============
def extract_playlist_info(url):
    """استخراج معلومات القائمة"""
    try:
        print(f"🔍 Extracting playlist info from: {url}")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': MAX_VIDEOS_PER_PLAYLIST,
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"✅ Playlist extracted: {info.get('title', 'Unknown')}")
            
            video_urls = []
            if 'entries' in info:
                for i, entry in enumerate(info['entries'][:MAX_VIDEOS_PER_PLAYLIST]):
                    if entry:
                        video_id = entry.get('id')
                        if video_id:
                            if 'youtube' in url:
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                            elif 'tiktok' in url:
                                video_url = f"https://www.tiktok.com/@user/video/{video_id}"
                            else:
                                video_url = entry.get('url', '')
                            
                            if video_url:
                                video_urls.append(video_url)
                                print(f"  Video {i+1}: {video_id}")
            
            return {
                'success': True,
                'title': info.get('title', 'Playlist'),
                'count': len(video_urls),
                'video_urls': video_urls
            }
    except Exception as e:
        print(f"❌ Error extracting playlist: {e}")
        return {'success': False, 'error': str(e)}

def download_and_upload_video(video_url, chat_id, caption=""):
    """تحميل ورفع فيديو واحد"""
    try:
        print(f"📥 Starting download: {video_url}")
        
        # إعدادات yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best[height<=720]',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': False,  # تغيير لـ False لرؤية الأخطاء
            'no_warnings': False,
            'noplaylist': True,
            'nooverwrites': True,
            'retries': 3,
            'fragment_retries': 3,
            'ignoreerrors': False,
            'no_check_certificate': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
        }
        
        # إنشاء مجلد مؤقت
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, 'video.mp4')
            ydl_opts['outtmpl'] = temp_file
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات أولاً
                info = ydl.extract_info(video_url, download=False)
                print(f"ℹ️ Video info: {info.get('title', 'Unknown')}")
                
                # تحميل الفيديو
                print("⬇️ Downloading video...")
                ydl.download([video_url])
                
                # التحقق من الملف
                if os.path.exists(temp_file):
                    file_size = os.path.getsize(temp_file)
                    print(f"✅ Downloaded: {file_size / (1024*1024):.1f} MB")
                    
                    # رفع الفيديو
                    print("⬆️ Uploading to Telegram...")
                    with open(temp_file, 'rb') as video:
                        bot.send_video(
                            chat_id,
                            video,
                            caption=caption,
                            supports_streaming=True,
                            timeout=300
                        )
                    print("✅ Video uploaded successfully!")
                    return True
                else:
                    # البحث عن أي ملف فيديو في المجلد
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp4', '.mkv', '.webm')):
                            actual_file = os.path.join(temp_dir, file)
                            print(f"📁 Found video file: {file}")
                            
                            file_size = os.path.getsize(actual_file)
                            print(f"✅ Downloaded: {file_size / (1024*1024):.1f} MB")
                            
                            # رفع الفيديو
                            print("⬆️ Uploading to Telegram...")
                            with open(actual_file, 'rb') as video:
                                bot.send_video(
                                    chat_id,
                                    video,
                                    caption=caption,
                                    supports_streaming=True,
                                    timeout=300
                                )
                            print("✅ Video uploaded successfully!")
                            return True
                    
                    print("❌ No video file found after download")
                    return False
                
    except Exception as e:
        print(f"❌ Download/upload error: {e}")
        traceback.print_exc()
        return False

def process_playlist(url, chat_id, message_id):
    """معالجة قائمة التشغيل"""
    try:
        # تحديث حالة البداية
        bot.edit_message_text(
            "🔍 <b>جاري تحليل قائمة التشغيل...</b>",
            chat_id, message_id
        )
        
        # استخراج معلومات القائمة
        playlist_info = extract_playlist_info(url)
        
        if not playlist_info['success']:
            bot.edit_message_text(
                "❌ <b>لا يمكن قراءة قائمة التشغيل</b>\n\n"
                f"خطأ: {playlist_info.get('error', 'غير معروف')}",
                chat_id, message_id
            )
            return
        
        video_urls = playlist_info['video_urls']
        total_videos = len(video_urls)
        
        if total_videos == 0:
            bot.edit_message_text(
                "❌ <b>لم يتم العثور على فيديوهات في القائمة</b>\n\n"
                "تأكد من أن القائمة عامة وتحتوي على فيديوهات",
                chat_id, message_id
            )
            return
        
        # تحديث بالعدد
        bot.edit_message_text(
            f"📁 <b>تم اكتشاف القائمة!</b>\n\n"
            f"🎬 <b>العنوان:</b> {playlist_info['title'][:50]}...\n"
            f"🔢 <b>عدد الفيديوهات:</b> {total_videos}\n\n"
            f"📥 <b>جاري رفع أول {min(5, total_videos)} فيديو...</b>",
            chat_id, message_id
        )
        
        # رفع الفيديوهات (أول 5 فقط)
        uploaded_count = 0
        videos_to_upload = min(5, total_videos)
        
        for i in range(videos_to_upload):
            try:
                video_url = video_urls[i]
                
                # تحديث حالة التقدم
                bot.edit_message_text(
                    f"📤 <b>جاري رفع الفيديو {i+1} من {videos_to_upload}...</b>\n\n"
                    f"✅ تم رفع: {uploaded_count}\n"
                    f"🔗 الرابط: {video_url[:50]}...",
                    chat_id, message_id
                )
                
                # تسمية الفيديو
                caption = f"🎬 الفيديو {i+1} من {videos_to_upload}\n📁 {playlist_info['title'][:30]}...\n⬆️ @ishdmvfvzobot"
                
                # تحميل ورفع الفيديو
                success = download_and_upload_video(video_url, chat_id, caption)
                
                if success:
                    uploaded_count += 1
                    print(f"✅ Successfully uploaded video {i+1}")
                else:
                    print(f"❌ Failed to upload video {i+1}")
                
                # انتظار بين الفيديوهات
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error processing video {i+1}: {e}")
                continue
        
        # النتيجة النهائية
        bot.edit_message_text(
            f"✅ <b>اكتمل رفع القائمة!</b>\n\n"
            f"📁 <b>القائمة:</b> {playlist_info['title'][:30]}...\n"
            f"🔢 <b>الفيديوهات:</b> {total_videos}\n"
            f"📤 <b>تم رفع:</b> {uploaded_count} من {videos_to_upload} فيديو\n\n"
            f"🎬 <b>جميع الفيديوهات في محادثتك الآن!</b>",
            chat_id, message_id
        )
        
    except Exception as e:
        print(f"❌ Playlist processing error: {e}")
        traceback.print_exc()
        bot.edit_message_text(
            f"❌ <b>حدث خطأ أثناء معالجة القائمة</b>\n\n{str(e)[:100]}",
            chat_id, message_id
        )

# ============== BOT MESSAGE HANDLERS ==============
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 <b>مرحباً! أنا بوت رفع الفيديوهات</b>

⚡ <b>المميزات:</b>
• رفع فيديوهات فردية من يوتيوب
• رفع قوائم تشغيل يوتيوب (أول 5 فيديوهات)
• يعمل 24/7 على السحابة
• الفيديوهات تبقى في محادثتك للأبد

🚀 <b>كيفية الاستخدام:</b>
1. أرسل رابط فيديو يوتيوب فردي
2. أو أرسل رابط قائمة يوتيوب
3. انتظر قليلاً
4. الفيديو/الفيديوهات تصل مباشرة

💡 <b>مثال:</b>
• فيديو: https://youtu.be/dQw4w9WgXcQ
• قائمة: https://youtube.com/playlist?list=...

🌐 <b>الاستضافة:</b> Render.com
🤖 <b>البوت:</b> @ishdmvfvzobot
    """
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['test'])
def test_command(message):
    """رابط تجريبي"""
    test_url = "https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"
    
    msg = bot.reply_to(message, """
🔗 <b>جرب هذا الرابط:</b>
https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj

📁 <b>هي قائمة يوتيوب قصيرة للتجربة</b>
    """)

@bot.message_handler(commands=['ping'])
def ping_command(message):
    bot.reply_to(message, "🏓 Pong! البوت يعمل")

@bot.message_handler(func=lambda message: message.text and 'youtube.com' in message.text)
def handle_youtube(message):
    """معالجة روابط يوتيوب"""
    url = message.text.strip()
    
    # التحقق إذا كان قائمة تشغيل
    is_playlist = 'playlist' in url or 'list=' in url
    
    if is_playlist:
        msg = bot.reply_to(message, """
📁 <b>تم اكتشاف قائمة تشغيل يوتيوب!</b>

🔍 <b>جاري التحليل...</b>
⏳ <b>الرجاء الانتظار...</b>
        """)
        
        # استخدام thread للتحميل
        thread = threading.Thread(
            target=process_playlist,
            args=(url, message.chat.id, msg.message_id),
            daemon=True
        )
        thread.start()
    else:
        # فيديو فردي
        msg = bot.reply_to(message, """
🎬 <b>تم اكتشاف فيديو يوتيوب فردي</b>

📥 <b>جاري التحميل...</b>
⏳ <b>قد يستغرق دقيقة...</b>
        """)
        
        thread = threading.Thread(
            target=lambda: download_and_upload_video(
                url, 
                message.chat.id, 
                "🎬 فيديو يوتيوب\n⬆️ @ishdmvfvzobot"
            ),
            daemon=True
        )
        thread.start()

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """معالجة الرسائل الأخرى"""
    bot.reply_to(message, """
📌 <b>أرسل رابط يوتيوب</b>

🎬 <b>فيديوهات فردية:</b>
https://youtu.be/dQw4w9WgXcQ
https://www.youtube.com/watch?v=...

📁 <b>قوائم تشغيل:</b>
https://youtube.com/playlist?list=...

💡 <b>ملاحظة:</b> يدعم البوت يوتيوب فقط حالياً
    """)

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء البوت نشطاً"""
    while True:
        try:
            requests.get(f'https://telegram-video-bot-n4aj.onrender.com/health', timeout=10)
            print(f"❤️ Keep-alive at {time.ctime()}")
        except:
            pass
        time.sleep(240)

# ============== RUN FUNCTIONS ==============
def run_flask():
    """تشغيل سيرفر Flask"""
    print(f"🌐 Starting Flask on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_telegram():
    """تشغيل بوت تلجرام"""
    print("🤖 Starting Telegram Bot...")
    
    # إعادة المحاولة عند الفشل
    while True:
        try:
            bot.polling(
                none_stop=True,
                timeout=30,
                long_polling_timeout=25
            )
        except Exception as e:
            print(f"⚠️ Bot error: {e}")
            time.sleep(5)
            print("🔄 Restarting bot...")

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting all services...")
    
    # إبقاء البوت نشطاً
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # تشغيل سيرفر Flask
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)
    print("✅ Web server started!")
    
    # تشغيل البوت
    run_telegram()
