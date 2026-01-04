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
                    <span class="info-label">Storage:</span>
                    <span class="info-value">Only in Telegram</span>
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎬</div>
                    <div>Video Upload</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🌐</div>
                    <div>24/7 Online</div>
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

@app.route('/reset')
def reset_webhook():
    """Reset webhook for Telegram bot"""
    try:
        http = urllib3.PoolManager()
        url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        response = http.request('GET', url)
        return {"message": "Webhook reset", "data": response.data.decode()}, 200
    except Exception as e:
        return {"error": str(e)}, 500

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
def download_video(url, chat_id, message_id):
    """تحميل الفيديو ورفعه"""
    try:
        # تحديث الرسالة
        bot.edit_message_text(
            "🔍 <b>جاري فحص الرابط وتحضير الفيديو...</b>",
            chat_id, message_id
        )
        
        # إعدادات yt-dlp المبسطة
        ydl_opts = {
            'format': 'best[ext=mp4]/best[height<=720]',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'nooverwrites': True,
            'retries': 3,
            'fragment_retries': 3,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'skip': ['hls', 'dash']
                }
            }
        }
        
        # إنشاء مجلد مؤقت في الذاكرة
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو أولاً
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'فيديو')[:50]
                duration = info.get('duration', 0)
                
                # تحديث الرسالة بالمعلومات
                bot.edit_message_text(
                    f"📥 <b>جاري تحميل الفيديو...</b>\n\n"
                    f"🎬 <b>العنوان:</b> {video_title}\n"
                    f"⏱ <b>المدة:</b> {duration // 60}:{duration % 60:02d}\n"
                    f"📊 <b>الجودة:</b> 720p أو أقل",
                    chat_id, message_id
                )
                
                # تحميل الفيديو
                ydl.download([url])
                
                # العثور على الملف المحمل
                video_file = ydl.prepare_filename(info)
                if not video_file.endswith('.mp4'):
                    video_file = video_file.rsplit('.', 1)[0] + '.mp4'
                
                # التحقق من وجود الملف
                if not os.path.exists(video_file):
                    # البحث عن أي ملف فيديو في المجلد المؤقت
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov')):
                            video_file = os.path.join(temp_dir, file)
                            break
                
                if os.path.exists(video_file):
                    # الحصول على حجم الملف
                    file_size = os.path.getsize(video_file)
                    file_size_mb = file_size / (1024 * 1024)
                    
                    if file_size_mb > 50:  # إذا كان أكبر من 50MB
                        bot.edit_message_text(
                            f"⚠️ <b>الفيديو كبير جداً ({file_size_mb:.1f}MB)</b>\n\n"
                            f"حد تليجرام الأقصى: 50MB\n"
                            f"جاري ضغط الفيديو...",
                            chat_id, message_id
                        )
                        
                        # محاولة تحميل جودة أقل
                        ydl_opts['format'] = 'best[height<=480]/best'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl_low:
                            ydl_low.download([url])
                    
                    # تحديث الرسالة قبل الرفع
                    bot.edit_message_text(
                        f"📤 <b>جاري رفع الفيديو إلى تليجرام...</b>\n\n"
                        f"📦 <b>الحجم:</b> {file_size_mb:.1f}MB\n"
                        f"⏳ <i>قد يستغرق دقيقة...</i>",
                        chat_id, message_id
                    )
                    
                    # رفع الفيديو إلى تليجرام
                    with open(video_file, 'rb') as video:
                        bot.send_video(
                            chat_id,
                            video,
                            caption=f"🎬 {info.get('title', 'فيديو')}\n\n"
                                   f"📥 تم الرفع بواسطة @ishdmvfvzobot\n"
                                   f"🌐 استضافة Render.com 24/7\n"
                                   f"⏱ المدة: {duration // 60}:{duration % 60:02d}",
                            supports_streaming=True,
                            timeout=300,
                            parse_mode='HTML'
                        )
                    
                    # رسالة النجاح النهائية
                    bot.edit_message_text(
                        "✅ <b>تم رفع الفيديو بنجاح!</b>\n\n"
                        "🎬 الفيديو الآن في محادثتك\n"
                        "💾 مخزن على تليجرام للأبد\n"
                        "🌐 البوت يعمل 24/7 على Render\n"
                        "🚀 أرسل رابطاً آخر لرفع المزيد",
                        chat_id, message_id
                    )
                    
                    return True
                else:
                    bot.edit_message_text(
                        "❌ <b>لم يتم العثور على ملف الفيديو بعد التحميل</b>\n\n"
                        "💡 حاول رابطاً آخر أو جرب لاحقاً",
                        chat_id, message_id
                    )
                    return False
                
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "Private video" in error_msg:
            bot.edit_message_text(
                "🔒 <b>الفيديو خاص ولا يمكن الوصول إليه</b>\n\n"
                "يجب أن يكون الفيديو عاماً للتحميل",
                chat_id, message_id
            )
        elif "Unsupported URL" in error_msg:
            bot.edit_message_text(
                "❌ <b>رابط غير مدعوم</b>\n\n"
                "يدعم البوت: يوتيوب، تيك توك، إنستجرام، تويتر\n"
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
        try:
            bot.edit_message_text(
                "❌ <b>حدث خطأ غير متوقع</b>\n\n"
                "💡 حاول مرة أخرى أو جرب رابطاً مختلفاً",
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
2. انتظر قليلاً (1-3 دقائق)
3. الفيديو يصل مباشرة لمحادثتك

📌 <b>الأوامر المتاحة:</b>
/start - بدء البوت
/status - حالة البوت
/test - رابط تجريبي
/ping - اختبار الاتصال

🌐 <b>الاستضافة:</b> Render.com
🔗 <b>الرابط:</b> https://telegram-video-bot-n4aj.onrender.com

💡 <b>ملاحظة:</b>
• الحد الأقصى: 50MB للفيديو
• قد يستغرق التحميل وقتاً حسب السرعة
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
💾 التخزين: في تليجرام فقط
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

🎬 <b>يوتيوب (قصير):</b>
https://youtube.com/shorts/Aa7KcUfN7Fc
https://youtube.com/shorts/6iAQm7Rgg8Q

🎬 <b>يوتيوب (عادي):</b>
https://youtu.be/dQw4w9WgXcQ
https://youtube.com/watch?v=9bZkp7q19f0

🚀 <b>أرسل أي رابط وسيتم رفعه!</b>
    """
    bot.reply_to(message, test_links)

@bot.message_handler(func=lambda message: message.text and (
    'youtube.com' in message.text or 
    'youtu.be' in message.text or
    'tiktok.com' in message.text or
    'instagram.com' in message.text or
    'twitter.com' in message.text or
    'x.com' in message.text
))
def handle_video_url(message):
    """معالجة روابط الفيديوهات"""
    url = message.text.strip()
    
    # إرسال رسالة تأكيد
    msg = bot.reply_to(message, """
🔍 <b>جاري فحص الرابط...</b>

⏳ <i>قد تستغرق العملية 1-3 دقائق</i>
📦 <i>حسب حجم الفيديو وسرعة المصدر</i>

🔄 <i>جاري البدء...</i>
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
• تويتر/إكس (Twitter/X)

💡 <b>جرب رابط يوتيوب قصير:</b>
https://youtube.com/shorts/Aa7KcUfN7Fc
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
• تويتر/إكس

💡 <b>جرب:</b> /test لروابط تجريبية
❓ <b>مساعدة:</b> /start للبدء
📊 <b>حالة:</b> /status
    """)

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء البوت نشطاً على الخطة المجانية"""
    import urllib3
    http = urllib3.PoolManager()
    
    while True:
        try:
            # Ping our own service
            response = http.request('GET', f'https://telegram-video-bot-n4aj.onrender.com/ping', timeout=10)
            if response.status == 200:
                print(f"❤️ Keep-alive ping successful at {time.ctime()}")
            else:
                print(f"⚠️ Keep-alive ping failed: {response.status}")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        
        # انتظار 4 دقائق و 30 ثانية (أقل من 5 دقائق لتجنب إيقاف Render)
        time.sleep(270)

# ============== RUN FUNCTIONS ==============
def run_flask():
    """تشغيل سيرفر Flask"""
    print(f"🌐 Starting Flask on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_telegram():
    """تشغيل بوت تلجرام"""
    print("🤖 Starting Telegram Bot...")
    
    # انتظار قليل قبل البدء
    time.sleep(2)
    
    # محاولات متعددة للاتصال
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_attempts}...")
            
            # محاولة إزالة webhook مجدداً
            try:
                bot.remove_webhook()
                time.sleep(0.5)
            except:
                pass
            
            # بدء الاستماع للرسائل
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
                # محاولة إعادة تعيين webhook بشكل قوي
                try:
                    import urllib3
                    http = urllib3.PoolManager()
                    reset_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true"
                    response = http.request('GET', reset_url)
                    print(f"Webhook reset response: {response.status}")
                except Exception as reset_error:
                    print(f"Webhook reset error: {reset_error}")
                
                wait_time = (attempt + 1) * 10  # زيادة وقت الانتظار مع كل محاولة
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
    
    if attempt == max_attempts - 1:
        print("❌ Failed to start bot after multiple attempts")
        print("💡 The bot might still work if it's already running elsewhere")
        print("💡 Try restarting the service in Render dashboard")

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting all services...")
    
    # بدء thread إبقاء البوت نشطاً
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # بدء سيرفر Flask في thread منفصل
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # انتظار قليل لبدء سيرفر الويب
    time.sleep(3)
    print("✅ Web server started successfully!")
    
    # بدء بوت تلجرام
    run_telegram()
