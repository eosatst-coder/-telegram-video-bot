"""
🎬 Telegram Video Bot - Render Hosting
✅ 24/7 Online | ✅ Cloud Hosted | ✅ TikTok & YouTube Playlists
"""

import os
import time
import telebot
import requests
import urllib3
import tempfile
import threading
import re
from flask import Flask
from threading import Thread
from io import BytesIO
import yt_dlp

# ============== CONFIG ==============
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4')
PORT = int(os.environ.get('PORT', 10000))
MAX_VIDEOS_PER_PLAYLIST = 5  # تحديد عدد الفيديوهات في القائمة

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
                    <span class="info-value">TikTok & YouTube Playlists</span>
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎬</div>
                    <div>Single Videos</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📁</div>
                    <div>TikTok Playlists</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎵</div>
                    <div>YouTube Playlists</div>
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
def get_platform(url):
    """تحديد نوع المنصة من الرابط"""
    if 'tiktok.com' in url or 'douyin.com' in url:
        return 'tiktok'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'instagram.com' in url or 'instagr.am' in url:
        return 'instagram'
    elif 'twitter.com' in url or 'x.com' in url:
        return 'twitter'
    else:
        return 'unknown'

def extract_video_urls_from_playlist(url, max_videos=MAX_VIDEOS_PER_PLAYLIST):
    """استخراج روابط الفيديوهات من قائمة التشغيل"""
    try:
        platform = get_platform(url)
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': max_videos,
        }
        
        # إعدادات خاصة بكل منصة
        if platform == 'tiktok':
            ydl_opts.update({
                'extractor_args': {
                    'tiktok': {
                        'skip': ['webpage'],
                        'approximate_rate': '500K'
                    }
                }
            })
        elif platform == 'youtube':
            ydl_opts.update({
                'extractor_args': {
                    'youtube': {
                        'skip': ['hls', 'dash']
                    }
                }
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_urls = []
            if 'entries' in info:
                for entry in info['entries'][:max_videos]:
                    if entry:
                        # استخراج رابط الفيديو
                        if 'url' in entry:
                            video_urls.append(entry['url'])
                        elif 'webpage_url' in entry:
                            video_urls.append(entry['webpage_url'])
                        elif 'id' in entry:
                            if platform == 'youtube':
                                video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
                            elif platform == 'tiktok':
                                video_urls.append(f"https://www.tiktok.com/@user/video/{entry['id']}")
            
            return {
                'success': True,
                'video_urls': video_urls,
                'title': info.get('title', 'قائمة تشغيل'),
                'count': len(video_urls),
                'platform': platform
            }
            
    except Exception as e:
        print(f"❌ Error extracting playlist: {e}")
        return {
            'success': False,
            'error': str(e),
            'video_urls': [],
            'platform': get_platform(url)
        }

def download_and_upload_single_video(video_url, chat_id, message_id=None, video_index=None, total_videos=None):
    """تحميل ورفع فيديو واحد"""
    try:
        platform = get_platform(video_url)
        
        # تحديث الرسالة إذا كان هناك message_id
        if message_id and video_index:
            try:
                bot.edit_message_text(
                    f"📥 <b>جاري تحميل الفيديو {video_index} من {total_videos}...</b>\n\n"
                    f"🌐 <b>المصدر:</b> {platform}",
                    chat_id, message_id
                )
            except:
                pass
        
        # إعدادات yt-dlp حسب المنصة
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'nooverwrites': True,
            'retries': 5,
            'fragment_retries': 5,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        # إعدادات خاصة بكل منصة
        if platform == 'tiktok':
            ydl_opts.update({
                'format': 'best',
                'extractor_args': {
                    'tiktok': {
                        'skip': ['webpage'],
                        'approximate_rate': '1M'
                    }
                }
            })
        elif platform == 'youtube':
            ydl_opts.update({
                'format': 'best[height<=720]/best',
            })
        
        # إنشاء مجلد مؤقت
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو أولاً
                info = ydl.extract_info(video_url, download=False)
                video_title = info.get('title', 'فيديو')[:100]
                duration = info.get('duration', 0)
                
                # تحديث الرسالة
                if message_id and video_index:
                    try:
                        bot.edit_message_text(
                            f"📥 <b>جاري تحميل الفيديو {video_index} من {total_videos}...</b>\n\n"
                            f"🎬 <b>العنوان:</b> {video_title}\n"
                            f"⏱ <b>المدة:</b> {duration // 60}:{duration % 60:02d}\n"
                            f"🌐 <b>المصدر:</b> {platform}",
                            chat_id, message_id
                        )
                    except:
                        pass
                
                # تحميل الفيديو
                ydl.download([video_url])
                
                # العثور على الملف المحمل
                video_file = ydl.prepare_filename(info)
                
                # البحث عن الملف إذا لم يكن mp4
                if not os.path.exists(video_file) or not video_file.endswith('.mp4'):
                    for file in os.listdir(temp_dir):
                        if any(file.endswith(ext) for ext in ['.mp4', '.mkv', '.webm']):
                            video_file = os.path.join(temp_dir, file)
                            break
                
                if os.path.exists(video_file):
                    file_size = os.path.getsize(video_file)
                    file_size_mb = file_size / (1024 * 1024)
                    
                    # تحديث الرسالة قبل الرفع
                    if message_id:
                        try:
                            bot.edit_message_text(
                                f"📤 <b>جاري رفع الفيديو {video_index if video_index else ''}...</b>\n\n"
                                f"📦 <b>الحجم:</b> {file_size_mb:.1f}MB",
                                chat_id, message_id
                            )
                        except:
                            pass
                    
                    # إعداد التسمية التوضيحية
                    caption = f"🎬 {video_title}\n\n"
                    if video_index:
                        caption += f"🔢 الفيديو {video_index} من {total_videos}\n"
                    caption += f"🌐 تم الرفع بواسطة @ishdmvfvzobot\n"
                    caption += f"⏱ المدة: {duration // 60}:{duration % 60:02d}"
                    
                    # رفع الفيديو إلى تليجرام
                    with open(video_file, 'rb') as video:
                        bot.send_video(
                            chat_id,
                            video,
                            caption=caption,
                            supports_streaming=True,
                            timeout=300,
                            parse_mode='HTML'
                        )
                    
                    return True
                else:
                    print(f"❌ File not found: {video_file}")
                    return False
                
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return False

def handle_video_playlist(url, chat_id, message_id):
    """معالجة قوائم التشغيل من جميع المنصات"""
    try:
        # تحديث الرسالة
        bot.edit_message_text(
            "🔍 <b>جاري تحليل قائمة التشغيل...</b>\n\n"
            "⏳ <i>قد يستغرق بضع ثواني</i>",
            chat_id, message_id
        )
        
        # استخراج روابط الفيديوهات من القائمة
        playlist_info = extract_video_urls_from_playlist(url)
        
        if not playlist_info['success'] or not playlist_info['video_urls']:
            bot.edit_message_text(
                "❌ <b>لا يمكن قراءة قائمة التشغيل</b>\n\n"
                f"💡 <i>{playlist_info.get('error', 'تأكد من أن القائمة عامة')}</i>",
                chat_id, message_id
            )
            return
        
        video_urls = playlist_info['video_urls']
        total_videos = len(video_urls)
        platform = playlist_info['platform']
        
        # تحديث الرسالة بالمعلومات
        bot.edit_message_text(
            f"📁 <b>قائمة تشغيل {platform.upper()} تم اكتشافها</b>\n\n"
            f"🎬 <b>العنوان:</b> {playlist_info['title'][:50]}...\n"
            f"🔢 <b>عدد الفيديوهات:</b> {total_videos}\n\n"
            f"📥 <b>جاري رفع {min(MAX_VIDEOS_PER_PLAYLIST, total_videos)} فيديو...</b>",
            chat_id, message_id
        )
        
        # رفع الفيديوهات
        uploaded_count = 0
        videos_to_upload = min(MAX_VIDEOS_PER_PLAYLIST, total_videos)
        
        for i, video_url in enumerate(video_urls[:videos_to_upload], 1):
            try:
                # تحديث تقدم الرفع
                try:
                    bot.edit_message_text(
                        f"📤 <b>جاري رفع الفيديو {i} من {videos_to_upload}...</b>\n\n"
                        f"✅ تم رفع: {uploaded_count}\n"
                        f"❌ فشل: {i - 1 - uploaded_count}",
                        chat_id, message_id
                    )
                except:
                    pass
                
                # تحميل ورفع الفيديو
                success = download_and_upload_single_video(
                    video_url, 
                    chat_id, 
                    message_id, 
                    video_index=i, 
                    total_videos=videos_to_upload
                )
                
                if success:
                    uploaded_count += 1
                
                # انتظار بين الفيديوهات لتجنب الحمل الزائد
                if i < videos_to_upload:
                    time.sleep(3)
                    
            except Exception as e:
                print(f"❌ Error processing video {i}: {e}")
                continue
        
        # رسالة النجاح النهائية
        success_rate = (uploaded_count / videos_to_upload) * 100 if videos_to_upload > 0 else 0
        
        bot.edit_message_text(
            f"✅ <b>اكتمل رفع القائمة!</b>\n\n"
            f"📁 <b>القائمة:</b> {playlist_info['title'][:30]}...\n"
            f"🌐 <b>المنصة:</b> {platform.upper()}\n"
            f"🔢 <b>إجمالي الفيديوهات:</b> {total_videos}\n"
            f"📤 <b>تم رفع:</b> {uploaded_count} من {videos_to_upload} فيديو\n"
            f"📊 <b>معدل النجاح:</b> {success_rate:.0f}%\n\n"
            f"🎬 <b>جميع الفيديوهات في محادثتك</b>\n"
            f"💾 <b>محفوظة على تليجرام للأبد</b>",
            chat_id, message_id
        )
        
    except Exception as e:
        print(f"❌ Playlist processing error: {e}")
        try:
            bot.edit_message_text(
                f"❌ <b>حدث خطأ أثناء معالجة القائمة:</b>\n\n{str(e)[:100]}",
                chat_id, message_id
            )
        except:
            pass

# ============== BOT MESSAGE HANDLERS ==============
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 <b>مرحباً! أنا بوت رفع الفيديوهات</b>
🌐 <i>مستضاف على Render 24/7</i>

⚡ <b>المميزات:</b>
• رفع فيديوهات فردية
• رفع قوائم تشغيل تيك توك
• رفع قوائم يوتيوب
• يعمل 24/7 على السحابة
• لا يحفظ ملفات على جهازك

🚀 <b>كيفية الاستخدام:</b>
1. أرسل رابط فيديو فردي
2. أو أرسل رابط قائمة تشغيل
3. انتظر قليلاً
4. الفيديو/الفيديوهات تصل مباشرة

📌 <b>الأوامر المتاحة:</b>
/start - بدء البوت
/status - حالة البوت
/test - رابط تجريبي
/tiktok - قائمة تيك توك تجريبية

🌐 <b>المدعوم:</b>
• تيك توك (فيديوهات وقوائم)
• يوتيوب (فيديوهات وقوائم)
• إنستجرام (فيديوهات)
• تويتر (فيديوهات)

💡 <b>ملاحظة:</b>
• الحد الأقصى: 50MB للفيديو
• قوائم التشغيل: أول 5 فيديوهات فقط
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
🎬 المميزات: تيك توك + يوتيوب + قوائم
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

🎵 <b>تيك توك:</b>
https://www.tiktok.com/@khaby00
https://www.tiktok.com/@daviddobrik

📁 <b>يوتيوب بلاي ليست:</b>
https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj
https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr

🎬 <b>فيديوهات فردية:</b>
https://youtube.com/shorts/Aa7KcUfN7Fc
https://youtu.be/dQw4w9WgXcQ

🚀 <b>أرسل أي رابط وسيتم رفعه!</b>
    """
    bot.reply_to(message, test_links)

@bot.message_handler(commands=['tiktok'])
def tiktok_test_command(message):
    """رابط تيك توك تجريبي"""
    tiktok_url = "https://www.tiktok.com/@khaby00"
    
    msg = bot.reply_to(message, """
🎵 <b>جاري معالجة قائمة تيك توك...</b>

⏳ <i>سيتم رفع أول 5 فيديوهات من الحساب</i>
📦 <i>قد يستغرق 2-5 دقائق</i>
    """)
    
    # استخدام thread للتحميل
    thread = threading.Thread(
        target=handle_video_playlist,
        args=(tiktok_url, message.chat.id, msg.message_id),
        daemon=True
    )
    thread.start()

@bot.message_handler(func=lambda message: message.text and (
    'tiktok.com' in message.text or
    'youtube.com' in message.text or 
    'youtu.be' in message.text or
    'instagram.com' in message.text or
    'twitter.com' in message.text or
    'x.com' in message.text
))
def handle_video_url(message):
    """معالجة جميع روابط الفيديوهات"""
    url = message.text.strip()
    
    # التحقق إذا كان رابط قائمة تشغيل أو حساب
    is_playlist = any(keyword in url.lower() for keyword in [
        'playlist', 'list=', '/@', '/user/', '/channel/'
    ])
    
    if is_playlist:
        msg = bot.reply_to(message, """
📁 <b>تم اكتشاف رابط قائمة/حساب!</b>

🔍 <b>جاري تحليل المحتوى...</b>
⏳ <i>قد يستغرق بضع ثواني</i>
        """)
        
        # استخدام thread للتحميل
        thread = threading.Thread(
            target=handle_video_playlist,
            args=(url, message.chat.id, msg.message_id),
            daemon=True
        )
        thread.start()
    else:
        msg = bot.reply_to(message, """
🎬 <b>تم اكتشاف رابط فيديو فردي</b>

🔍 <b>جاري فحص الفيديو...</b>
⏳ <i>قد يستغرق 1-3 دقائق</i>
        """)
        
        # استخدام thread للتحميل
        thread = threading.Thread(
            target=lambda: download_and_upload_single_video(url, message.chat.id, msg.message_id),
            daemon=True
        )
        thread.start()

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """معالجة الرسائل الأخرى"""
    bot.reply_to(message, """
📌 <b>أرسل رابط فيديو أو قائمة تشغيل</b>

🎵 <b>تيك توك:</b>
• فيديو فردي: https://vm.tiktok.com/xxxxxx
• حساب: https://www.tiktok.com/@username
• موسيقى: https://www.tiktok.com/music/xxxx

📁 <b>يوتيوب:</b>
• فيديو: https://youtu.be/xxxx
• بلاي ليست: https://youtube.com/playlist?list=xxxx

💡 <b>جرب:</b> /test لروابط تجريبية
🎵 <b>تيك توك:</b> /tiktok لقائمة تجريبية
❓ <b>مساعدة:</b> /start للبدء
    """)

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء البوت نشطاً على الخطة المجانية"""
    while True:
        try:
            requests.get(f'https://telegram-video-bot-n4aj.onrender.com/ping', timeout=10)
            print(f"❤️ Keep-alive ping at {time.ctime()}")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        
        time.sleep(240)  # كل 4 دقائق

# ============== RUN FUNCTIONS ==============
def run_flask():
    """تشغيل سيرفر Flask"""
    print(f"🌐 Starting Flask on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_telegram():
    """تشغيل بوت تلجرام"""
    print("🤖 Starting Telegram Bot...")
    
    time.sleep(2)
    
    max_attempts = 3
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
                print("🔄 Conflict detected...")
                wait_time = (attempt + 1) * 5
                print(f"⏳ Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("⏳ Waiting 3 seconds...")
                time.sleep(3)
    
    if attempt == max_attempts - 1:
        print("⚠️ Bot might have connection issues, but will try to reconnect")

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting all services...")
    
    # بدء thread إبقاء البوت نشطاً
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # بدء سيرفر Flask
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # انتظار بدء سيرفر الويب
    time.sleep(3)
    print("✅ Web server started successfully!")
    
    # بدء بوت تلجرام
    run_telegram()
