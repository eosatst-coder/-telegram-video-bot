"""
🎬 Telegram Video Bot - Render Hosting
✅ 24/7 Online | ✅ Cloud Hosted | ✅ Real Video Upload
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

print("=" * 60)
print("🎬 Telegram Video Bot - Render Hosting")
print("=" * 60)
print(f"🤖 Token: {TOKEN[:15]}...")
print(f"🌐 Port: {PORT}")

# ============== FLASK WEB SERVER ==============
app = Flask(__name__)

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Video Bot</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                margin: 0 auto;
            }
            .status {
                color: #4CAF50;
                font-size: 28px;
                margin: 20px 0;
                font-weight: bold;
            }
            .bot-link {
                display: inline-block;
                background: #0088cc;
                color: white;
                padding: 12px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 20px;
                transition: all 0.3s;
            }
            .bot-link:hover {
                background: #006699;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,136,204,0.4);
            }
            .info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: left;
            }
            .feature {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .feature-icon {
                font-size: 24px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Video Bot</h1>
            <div class="status">✅ ONLINE & WORKING</div>
            
            <div class="info">
                <p><strong>Bot:</strong> @ishdmvfvzobot</p>
                <p><strong>Host:</strong> Render.com</p>
                <p><strong>Status:</strong> Active 24/7</p>
                <p><strong>Time:</strong> """ + time.ctime() + """</p>
                <p><strong>Features:</strong> Real video upload</p>
            </div>
            
            <div class="feature">
                <span class="feature-icon">⚡</span>
                <span>Direct video upload to Telegram</span>
            </div>
            <div class="feature">
                <span class="feature-icon">🎬</span>
                <span>YouTube, TikTok, Instagram support</span>
            </div>
            <div class="feature">
                <span class="feature-icon">🌐</span>
                <span>Permanent cloud hosting</span>
            </div>
            
            <p>This bot can upload videos directly to Telegram</p>
            <a href="https://t.me/ishdmvfvzobot" class="bot-link" target="_blank">
                🚀 Open in Telegram
            </a>
            
            <div style="margin-top: 30px; color: #666; font-size: 14px;">
                <p>Service ID: srv-d5d4541r0fns73ac1d8g</p>
                <p>Hosted on Render Free Tier</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/health')
def health():
    return "OK", 200

@app.route('/ping')
def ping():
    return "Pong", 200

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Clear any existing webhook to avoid conflicts
try:
    bot.remove_webhook()
    print("✅ Webhook cleared")
    time.sleep(1)
except Exception as e:
    print(f"⚠️ Could not clear webhook: {e}")

# ============== VIDEO DOWNLOAD FUNCTIONS ==============
def download_video(url, chat_id, message_id):
    """تحميل الفيديو ورفعه"""
    try:
        # إرسال رسالة تبدأ التحميل
        bot.edit_message_text(
            "📥 <b>جاري تحميل الفيديو...</b>",
            chat_id, message_id
        )
        
        # إعدادات yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'nooverwrites': True,
            'retries': 10,
            'fragment_retries': 10,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        # إنشاء مجلد مؤقت
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو
                info = ydl.extract_info(url, download=True)
                
                # تحديث الرسالة
                bot.edit_message_text(
                    f"📤 <b>جاري رفع الفيديو...</b>\n\n"
                    f"🎬 <b>العنوان:</b> {info.get('title', 'فيديو')[:50]}...\n"
                    f"⏱ <b>المدة:</b> {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}",
                    chat_id, message_id
                )
                
                # العثور على الملف المحمل
                video_file = ydl.prepare_filename(info)
                if not video_file.endswith('.mp4'):
                    video_file = video_file.rsplit('.', 1)[0] + '.mp4'
                
                # رفع الفيديو إلى تليجرام
                with open(video_file, 'rb') as video:
                    bot.send_video(
                        chat_id,
                        video,
                        caption=f"🎬 {info.get('title', 'فيديو')}\n\n"
                               f"📥 تم الرفع بواسطة @ishdmvfvzobot\n"
                               f"🌐 استضافة Render.com",
                        supports_streaming=True,
                        timeout=300  # 5 دقائق للفيديوهات الكبيرة
                    )
                
                # تحديث رسالة النجاح
                bot.edit_message_text(
                    "✅ <b>تم رفع الفيديو بنجاح!</b>\n\n"
                    "🎬 الفيديو الآن في محادثتك\n"
                    "💾 مخزن على تليجرام للأبد\n"
                    "🌐 البوت يعمل 24/7 على Render",
                    chat_id, message_id
                )
                
                return True
                
    except Exception as e:
        print(f"❌ Download error: {e}")
        try:
            bot.edit_message_text(
                f"❌ <b>حدث خطأ أثناء التحميل:</b>\n\n"
                f"{str(e)[:200]}",
                chat_id, message_id
            )
        except:
            pass
        return False

def download_video_thread(url, chat_id, message_id):
    """تشغيل التحميل في thread منفصل"""
    thread = threading.Thread(
        target=download_video,
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
• رفع مباشر إلى تليجرام
• يعمل 24/7 على السحابة
• لا يحفظ ملفات على جهازك
• دعم يوتيوب، تيك توك، إنستجرام

🚀 <b>كيفية الاستخدام:</b>
1. أرسل رابط فيديو
2. انتظر قليلاً
3. الفيديو يصل مباشرة لمحادثتك

📌 <b>الأوامر المتاحة:</b>
/start - بدء البوت
/status - حالة البوت
/test - رابط تجريبي

🌐 <b>الاستضافة:</b> Render.com
🔗 <b>الرابط:</b> https://telegram-video-bot-n4aj.onrender.com
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
📡 الخدمة: srv-d5d4541r0fns73ac1d8g
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

• يوتيوب:
https://youtu.be/dQw4w9WgXcQ
https://youtube.com/shorts/Aa7KcUfN7Fc

• تيك توك:
https://www.tiktok.com/@example/video/123456789

• إنستجرام:
https://www.instagram.com/reel/Cxample/

🚀 <b>أرسل أي رابط وسيتم رفعه!</b>
    """
    bot.reply_to(message, test_links)

@bot.message_handler(func=lambda message: message.text and (
    'youtube.com' in message.text or 
    'youtu.be' in message.text or
    'tiktok.com' in message.text or
    'instagram.com' in message.text or
    'twitter.com' in message.text
))
def handle_video_url(message):
    """معالجة روابط الفيديوهات"""
    url = message.text.strip()
    
    # إرسال رسالة تأكيد
    msg = bot.reply_to(message, """
🔍 <b>جاري فحص الرابط...</b>

⏳ <i>قد تستغرق العملية 1-3 دقائق</i>
📦 <i>حسب حجم الفيديو وسرعة المصدر</i>
    """)
    
    # بدء التحميل في thread منفصل
    download_video_thread(url, message.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def handle_other_url(message):
    """معالجة الروابط الأخرى"""
    url = message.text.strip()
    bot.reply_to(message, f"""
🔗 <b>تم استلام الرابط:</b>
{url}

❌ <b>هذا النوع من الروابط غير مدعوم حالياً</b>

✅ <b>الأنواع المدعومة:</b>
• يوتيوب (YouTube)
• تيك توك (TikTok)
• إنستجرام (Instagram)
• تويتر (Twitter)

💡 <b>جرب رابط يوتيوب:</b>
https://youtu.be/dQw4w9WgXcQ
    """)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """معالجة الرسائل الأخرى"""
    bot.reply_to(message, """
📌 <b>أرسل رابط فيديو لرفعه</b>

🚀 <b>الأنواع المدعومة:</b>
• يوتيوب
• تيك توك
• إنستجرام
• تويتر

💡 <b>جرب:</b> /test لروابط تجريبية
❓ <b>مساعدة:</b> /start للبدء
    """)

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء البوت نشطاً على الخطة المجانية"""
    while True:
        try:
            requests.get(f"https://telegram-video-bot-n4aj.onrender.com/ping", timeout=10)
            print(f"❤️ Keep-alive ping at {time.ctime()}")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        time.sleep(300)  # كل 5 دقائق

# ============== RUN FUNCTIONS ==============
def run_flask():
    """تشغيل سيرفر Flask"""
    print(f"🌐 Starting Flask on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_telegram():
    """تشغيل بوت تلجرام"""
    print("🤖 Starting Telegram Bot...")
    
    # Wait a bit before starting
    time.sleep(3)
    
    retry_count = 0
    max_retries = 10
    
    while retry_count < max_retries:
        try:
            print(f"🔄 Attempt {retry_count + 1}/{max_retries} to start bot...")
            
            # Clear webhook before polling
            try:
                bot.remove_webhook()
                time.sleep(1)
            except:
                pass
            
            # Start polling with specific parameters
            bot.polling(
                none_stop=True,
                timeout=30,
                long_polling_timeout=30,
                allowed_updates=None
            )
            
            print("✅ Bot polling started successfully")
            break
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Bot error: {error_msg[:150]}")
            
            # Handle specific errors
            if "409" in error_msg:
                print("🔄 Conflict detected - another instance might be running")
                print("Waiting 10 seconds before retry...")
                time.sleep(10)
            elif "timed out" in error_msg.lower():
                print("⏰ Timeout - retrying immediately")
                time.sleep(2)
            else:
                print("🔄 General error - waiting 5 seconds")
                time.sleep(5)
            
            retry_count += 1
    
    if retry_count >= max_retries:
        print("❌ Failed to start bot after multiple attempts")
        print("💡 Try stopping any local bot instances")
        print("💡 Or wait a few minutes and restart the service")

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting all services...")
    
    # Start keep-alive thread
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Start Flask in background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    time.sleep(3)
    print("✅ Web server started successfully!")
    
    # Give webhook reset time
    time.sleep(2)
    
    # Start Telegram bot
    run_telegram()
