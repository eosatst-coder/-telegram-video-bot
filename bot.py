"""
🎬 Telegram Video Bot - Render Hosting
✅ 24/7 Online | ✅ Cloud Hosted | ✅ Playlist Support
"""

import os
import time
import telebot
import requests
import urllib3
import tempfile
import threading
from flask import Flask
from threading import Thread
from io import BytesIO
import yt_dlp

# ============== CONFIG ==============
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4')
PORT = int(os.environ.get('PORT', 10000))
MAX_VIDEOS_PER_PLAYLIST = 10  # تحديد عدد الفيديوهات في القائمة

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
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
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
            
            .status-icon {{
                font-size: 80px;
                margin-bottom: 20px;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            
            h1 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 28px;
            }}
            
            .status {{
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 50px;
                display: inline-block;
                margin: 20px 0;
                font-weight: bold;
                font-size: 18px;
            }}
            
            .info-box {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
                text-align: left;
            }}
            
            .info-item {{
                margin: 10px 0;
                padding: 10px;
                border-bottom: 1px solid #eee;
            }}
            
            .info-label {{
                font-weight: bold;
                color: #555;
                display: inline-block;
                width: 150px;
            }}
            
            .info-value {{
                color: #333;
            }}
            
            .bot-link {{
                display: inline-block;
                background: #0088cc;
                color: white;
                text-decoration: none;
                padding: 12px 30px;
                border-radius: 50px;
                margin-top: 20px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .bot-link:hover {{
                background: #006699;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,136,204,0.4);
            }}
            
            .footer {{
                margin-top: 30px;
                color: #777;
                font-size: 14px;
            }}
            
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            
            .feature {{
                background: #e3f2fd;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }}
            
            .feature-icon {{
                font-size: 30px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-icon">🤖</div>
            <h1>Telegram Video Upload Bot</h1>
            <div class="status">✅ ONLINE & WORKING</div>
            
            <div class="info-box">
                <div class="info-item">
                    <span class="info-label">Bot Name:</span>
                    <span class="info-value">@ishdmvfvzobot</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="info-value">Active 24/7</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Host:</span>
                    <span class="info-value">Render.com</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Uptime:</span>
                    <span class="info-value">Always Online</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Features:</span>
                    <span class="info-value">Single Videos & Playlists</span>
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎬</div>
                    <div>Single Videos</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📁</div>
                    <div>Playlists</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div>Direct Upload</div>
                </div>
            </div>
            
            <a href="https://t.me/ishdmvfvzobot" class="bot-link" target="_blank">
                🚀 Open Telegram Bot
            </a>
            
            <div class="footer">
                <p>This bot runs permanently on Render cloud hosting</p>
                <p>Last checked: {time.ctime()}</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "time": time.time()}, 200

@app.route('/ping')
def ping():
    return "🏓 Pong! Bot is alive", 200

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Reset webhook to avoid conflicts
try:
    bot.remove_webhook()
    time.sleep(0.5)
    print("✅ Webhook cleared")
except Exception as e:
    print(f"⚠️ Could not clear webhook: {e}")

# ============== VIDEO DOWNLOAD FUNCTIONS ==============
def is_playlist(url):
    """التحقق إذا كان الرابط قائمة تشغيل"""
    return 'playlist' in url or 'list=' in url

def get_playlist_info(url):
    """الحصول على معلومات قائمة التشغيل"""
    try:
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'playlistend': MAX_VIDEOS_PER_PLAYLIST
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"❌ Playlist info error: {e}")
        return None

def download_single_video(url, chat_id, message_id):
    """تحميل فيديو فردي"""
    try:
        bot.edit_message_text(
            "🔍 <b>جاري فحص رابط الفيديو...</b>",
            chat_id, message_id
        )
        
        # إعدادات yt-dlp المبسطة
        ydl_opts = {
            'format': 'best[ext=mp4]/best[height<=720]',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,  # تأكيد عدم تحميل قوائم التشغيل
            'nooverwrites': True,
            'retries': 3,
            'fragment_retries': 3,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        # إنشاء مجلد مؤقت في الذاكرة
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو أولاً
                info = ydl.extract_info(url, download=False)
                
                # إذا كان الرابط قائمة تشغيل، استخراج أول فيديو
                if 'entries' in info:
                    if info['entries']:
                        # أخذ أول فيديو في القائمة
                        first_video = info['entries'][0]
                        if 'url' in first_video:
                            url = first_video['url']
                        elif 'id' in first_video:
                            # بناء رابط الفيديو الفردي
                            url = f"https://www.youtube.com/watch?v={first_video['id']}"
                        # إعادة استخراج المعلومات للفيديو الجديد
                        info = ydl.extract_info(url, download=False)
                
                video_title = info.get('title', 'فيديو')[:50]
                duration = info.get('duration', 0)
                
                bot.edit_message_text(
                    f"📥 <b>جاري تحميل الفيديو...</b>\n\n"
                    f"🎬 <b>العنوان:</b> {video_title}\n"
                    f"⏱ <b>المدة:</b> {duration // 60}:{duration % 60:02d}",
                    chat_id, message_id
                )
                
                # تحميل الفيديو
                ydl.download([url])
                
                # العثور على الملف المحمل
                video_file = ydl.prepare_filename(info)
                if not video_file.endswith('.mp4'):
                    video_file = video_file.rsplit('.', 1)[0] + '.mp4'
                
                # البحث عن الملف إذا لم يوجد بالاسم الدقيق
                if not os.path.exists(video_file):
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov')):
                            video_file = os.path.join(temp_dir, file)
                            break
                
                if os.path.exists(video_file):
                    file_size = os.path.getsize(video_file)
                    file_size_mb = file_size / (1024 * 1024)
                    
                    bot.edit_message_text(
                        f"📤 <b>جاري رفع الفيديو...</b>\n\n"
                        f"📦 <b>الحجم:</b> {file_size_mb:.1f}MB",
                        chat_id, message_id
                    )
                    
                    # رفع الفيديو إلى تليجرام
                    with open(video_file, 'rb') as video:
                        bot.send_video(
                            chat_id,
                            video,
                            caption=f"🎬 {info.get('title', 'فيديو')}\n\n"
                                   f"📥 تم الرفع بواسطة @ishdmvfvzobot\n"
                                   f"🌐 استضافة Render.com 24/7",
                            supports_streaming=True,
                            timeout=300,
                            parse_mode='HTML'
                        )
                    
                    bot.edit_message_text(
                        "✅ <b>تم رفع الفيديو بنجاح!</b>\n\n"
                        "🎬 الفيديو الآن في محادثتك\n"
                        "💾 مخزن على تليجرام للأبد",
                        chat_id, message_id
                    )
                    
                    return True
                else:
                    bot.edit_message_text(
                        "❌ <b>لم يتم العثور على ملف الفيديو</b>\n\n"
                        "💡 حاول رابط فيديو فردي مباشر",
                        chat_id, message_id
                    )
                    return False
                
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "Private video" in error_msg:
            bot.edit_message_text(
                "🔒 <b>الفيديو خاص ولا يمكن الوصول إليه</b>",
                chat_id, message_id
            )
        elif "Unsupported URL" in error_msg:
            bot.edit_message_text(
                "❌ <b>رابط غير مدعوم</b>\n\n"
                "💡 تأكد من صحة الرابط",
                chat_id, message_id
            )
        else:
            bot.edit_message_text(
                f"❌ <b>خطأ في التحميل:</b>\n\n{error_msg[:200]}",
                chat_id, message_id
            )
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        bot.edit_message_text(
            "❌ <b>حدث خطأ غير متوقع</b>\n\n"
            "💡 حاول مرة أخرى",
            chat_id, message_id
        )
        return False

def handle_playlist(url, chat_id, message_id):
    """معالجة قائمة التشغيل"""
    try:
        bot.edit_message_text(
            "📁 <b>تم اكتشاف قائمة تشغيل!</b>\n\n"
            "🔍 جاري تحليل القائمة...",
            chat_id, message_id
        )
        
        # الحصول على معلومات القائمة
        info = get_playlist_info(url)
        if not info or 'entries' not in info:
            bot.edit_message_text(
                "❌ <b>لا يمكن قراءة قائمة التشغيل</b>\n\n"
                "💡 تأكد من أن القائمة عامة",
                chat_id, message_id
            )
            return
        
        videos = info.get('entries', [])
        total_videos = len(videos)
        
        if total_videos == 0:
            bot.edit_message_text(
                "❌ <b>القائمة فارغة</b>\n\n"
                "💡 حاول قائمة تشغيل أخرى",
                chat_id, message_id
            )
            return
        
        bot.edit_message_text(
            f"📁 <b>قائمة تشغيل تم اكتشافها</b>\n\n"
            f"🎬 <b>العنوان:</b> {info.get('title', 'قائمة تشغيل')[:50]}...\n"
            f"🔢 <b>عدد الفيديوهات:</b> {total_videos}\n\n"
            f"📥 <b>سيتم رفع أول {min(3, total_videos)} فيديو...</b>",
            chat_id, message_id
        )
        
        # رفع أول 3 فيديوهات فقط لتجنب الحمل الزائد
        videos_to_upload = min(3, total_videos)
        uploaded_count = 0
        
        for i, video in enumerate(videos[:videos_to_upload], 1):
            try:
                bot.edit_message_text(
                    f"📥 <b>جاري رفع الفيديو {i} من {videos_to_upload}...</b>\n\n"
                    f"✅ تم رفع: {uploaded_count}",
                    chat_id, message_id
                )
                
                # الحصول على رابط الفيديو الفردي
                video_url = None
                if 'url' in video:
                    video_url = video['url']
                elif 'id' in video:
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                
                if video_url:
                    # تحميل ورفع الفيديو
                    with tempfile.TemporaryDirectory() as temp_dir:
                        ydl_opts = {
                            'format': 'best[ext=mp4]/best[height<=480]',
                            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                            'quiet': True,
                            'no_warnings': True,
                            'noplaylist': True
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            video_info = ydl.extract_info(video_url, download=True)
                            video_file = ydl.prepare_filename(video_info)
                            
                            if not video_file.endswith('.mp4'):
                                video_file = video_file.rsplit('.', 1)[0] + '.mp4'
                            
                            if os.path.exists(video_file):
                                with open(video_file, 'rb') as vf:
                                    bot.send_video(
                                        chat_id,
                                        vf,
                                        caption=f"🎬 {video_info.get('title', f'فيديو {i}')}\n"
                                               f"📁 جزء من قائمة التشغيل\n"
                                               f"🔢 {i} من {videos_to_upload}\n\n"
                                               f"📥 @ishdmvfvzobot",
                                        supports_streaming=True,
                                        timeout=300
                                    )
                                uploaded_count += 1
                
                # انتظار بين الفيديوهات
                if i < videos_to_upload:
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ Error uploading video {i}: {e}")
                continue
        
        # رسالة النجاح النهائية
        bot.edit_message_text(
            f"✅ <b>اكتمل رفع القائمة!</b>\n\n"
            f"📁 <b>القائمة:</b> {info.get('title', 'قائمة تشغيل')[:30]}...\n"
            f"🔢 <b>تم رفع:</b> {uploaded_count} من {videos_to_upload} فيديو\n\n"
            f"🎬 جميع الفيديوهات في محادثتك\n"
            f"💾 مخزنة على تليجرام للأبد",
            chat_id, message_id
        )
        
    except Exception as e:
        print(f"❌ Playlist error: {e}")
        bot.edit_message_text(
            f"❌ <b>خطأ في معالجة القائمة:</b>\n\n{str(e)[:100]}",
            chat_id, message_id
        )

def download_video_thread(url, chat_id, message_id, is_playlist=False):
    """تشغيل التحميل في thread منفصل"""
    if is_playlist:
        thread = threading.Thread(
            target=handle_playlist,
            args=(url, chat_id, message_id),
            daemon=True
        )
    else:
        thread = threading.Thread(
            target=download_single_video,
            args=(url, chat_id, message_id),
            daemon=True
        )
    thread.start()

# ============== BOT COMMANDS ==============
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 <b>مرحباً! أنا بوت رفع الفيديوهات</b>
🌐 <i>مستضاف على Render 24/7</i>

⚡ <b>المميزات:</b>
• رفع فيديوهات فردية
• رفع قوائم التشغيل (أول 3 فيديوهات)
• يعمل 24/7 على السحابة
• لا يحفظ ملفات على جهازك

🚀 <b>كيفية الاستخدام:</b>
1. أرسل رابط فيديو فردي
2. أو أرسل رابط قائمة تشغيل
3. انتظر قليلاً (1-5 دقائق)
4. الفيديو/الفيديوهات تصل مباشرة

📌 <b>الأوامر المتاحة:</b>
/start - بدء البوت
/status - حالة البوت
/test - رابط تجريبي
/playlist - رابط قائمة تجريبية

🌐 <b>الاستضافة:</b> Render.com

💡 <b>ملاحظة:</b>
• الحد الأقصى: 50MB للفيديو
• قوائم التشغيل: أول 3 فيديوهات فقط
• قد يستغرق التحميل وقتاً
    """
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['status'])
def status_command(message):
    status_msg = f"""
📊 <b>حالة البوت:</b>
✅ نشط ويعمل
🌐 استضافة: Render.com
⏰ وقت التشغيل: 24/7
🤖 البوت: @ishdmvfvzobot
🔗 الرابط: https://telegram-video-bot-n4aj.onrender.com
🕒 الوقت: {time.ctime()}
🎬 المميزات: فيديوهات فردية + قوائم
    """
    bot.reply_to(message, status_msg)

@bot.message_handler(commands=['ping'])
def ping_command(message):
    bot.reply_to(message, "🏓 Pong! البوت يعمل بنجاح")

@bot.message_handler(commands=['test'])
def test_command(message):
    """إرسال رابط تجريبي"""
    test_links = """
🔗 <b>روابط تجريبية:</b>

🎬 <b>فيديوهات فردية:</b>
https://youtube.com/shorts/Aa7KcUfN7Fc
https://youtu.be/dQw4w9WgXcQ

📁 <b>قوائم تشغيل:</b>
https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj
https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr

🚀 <b>أرسل أي رابط وسيتم رفعه!</b>
    """
    bot.reply_to(message, test_links)

@bot.message_handler(commands=['playlist'])
def playlist_test_command(message):
    """رابط قائمة تجريبية مباشر"""
    playlist_url = "https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"
    
    msg = bot.reply_to(message, """
📁 <b>جاري معالجة قائمة التشغيل التجريبية...</b>

⏳ <i>سيتم رفع أول 3 فيديوهات من القائمة</i>
    """)
    
    download_video_thread(playlist_url, message.chat.id, msg.message_id, is_playlist=True)

@bot.message_handler(func=lambda message: message.text and (
    'youtube.com' in message.text or 
    'youtu.be' in message.text or
    'tiktok.com' in message.text or
    'instagram.com' in message.text
))
def handle_video_url(message):
    """معالجة روابط الفيديوهات"""
    url = message.text.strip()
    
    # التحقق إذا كان رابط قائمة تشغيل
    is_playlist_url = is_playlist(url)
    
    if is_playlist_url:
        msg = bot.reply_to(message, """
📁 <b>تم اكتشاف رابط قائمة تشغيل!</b>

🔍 <b>جاري تحليل القائمة...</b>
⏳ <i>سيتم رفع أول 3 فيديوهات</i>
📦 <i>قد يستغرق 5-10 دقائق</i>
        """)
        download_video_thread(url, message.chat.id, msg.message_id, is_playlist=True)
    else:
        msg = bot.reply_to(message, """
🎬 <b>تم اكتشاف رابط فيديو فردي</b>

🔍 <b>جاري فحص الفيديو...</b>
⏳ <i>قد يستغرق 1-3 دقائق</i>
        """)
        download_video_thread(url, message.chat.id, msg.message_id, is_playlist=False)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """معالجة الرسائل الأخرى"""
    bot.reply_to(message, """
📌 <b>أرسل رابط فيديو أو قائمة تشغيل</b>

🎬 <b>فيديوهات فردية:</b>
• يوتيوب
• تيك توك
• إنستجرام

📁 <b>قوائم تشغيل:</b>
• يوتيوب بلايليست

💡 <b>جرب:</b> /test لروابط تجريبية
📁 <b>قائمة:</b> /playlist لقائمة تجريبية
❓ <b>مساعدة:</b> /start للبدء
    """)

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء البوت نشطاً على الخطة المجانية"""
    import urllib3
    http = urllib3.PoolManager()
    
    while True:
        try:
            response = http.request('GET', f'https://telegram-video-bot-n4aj.onrender.com/ping', timeout=10)
            if response.status == 200:
                print(f"❤️ Keep-alive ping successful at {time.ctime()}")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        
        time.sleep(270)

# ============== RUN FUNCTIONS ==============
def run_flask():
    """تشغيل سيرفر Flask"""
    print(f"🌐 Starting Flask on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_telegram():
    """تشغيل بوت تلجرام"""
    print("🤖 Starting Telegram Bot...")
    
    time.sleep(2)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_attempts}...")
            
            try:
                bot.remove_webhook()
                time.sleep(0.5)
            except:
                pass
            
            bot.polling(
                none_stop=True,
                timeout=30,
                long_polling_timeout=25,
                allowed_updates=None,
                interval=0.5
            )
            
            print("✅ Bot polling started successfully")
            break
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Bot error (attempt {attempt + 1}): {error_msg[:100]}")
            
            if "409" in error_msg:
                print("🔄 Conflict detected, trying to reset webhook...")
                try:
                    import urllib3
                    http = urllib3.PoolManager()
                    reset_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true"
                    response = http.request('GET', reset_url)
                    print(f"Webhook reset response: {response.status}")
                except Exception as reset_error:
                    print(f"Webhook reset error: {reset_error}")
                
                wait_time = (attempt + 1) * 10
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
    
    if attempt == max_attempts - 1:
        print("❌ Failed to start bot after multiple attempts")

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting all services...")
    
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(3)
    print("✅ Web server started successfully!")
    
    run_telegram()
