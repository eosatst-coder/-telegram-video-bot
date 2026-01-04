"""
🎬 Telegram Video Bot - Render Hosting
✅ 24/7 Online | ✅ Cloud Hosted
"""

import os
import time
import telebot
import requests
import urllib3
from flask import Flask
from threading import Thread

# ============== CONFIG ==============
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4')
PORT = int(os.environ.get('PORT', 10000))

print("=" * 50)
print("🎬 Telegram Video Bot - Render Hosting")
print("=" * 50)
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
            </div>
            
            <div class="feature">
                <span class="feature-icon">⚡</span>
                <span>Direct video upload to Telegram</span>
            </div>
            <div class="feature">
                <span class="feature-icon">🌐</span>
                <span>Permanent cloud hosting</span>
            </div>
            <div class="feature">
                <span class="feature-icon">💾</span>
                <span>No files stored on your device</span>
            </div>
            
            <p>This bot is permanently hosted on Render cloud</p>
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

@app.route('/reset')
def reset_webhook():
    """Reset webhook for Telegram bot"""
    try:
        # Forcefully delete webhook
        http = urllib3.PoolManager()
        url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        response = http.request('GET', url)
        return f"Webhook reset: {response.data.decode()}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Clear any existing webhook to avoid conflicts
try:
    bot.remove_webhook()
    print("✅ Webhook cleared")
    time.sleep(1)
except Exception as e:
    print(f"⚠️ Could not clear webhook: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 <b>مرحباً! أنا بوت رفع الفيديوهات</b>
🌐 <i>مستضاف على Render 24/7</i>

⚡ <b>المميزات:</b>
• رفع مباشر إلى تليجرام
• يعمل 24/7 على السحابة
• لا يحفظ ملفات على جهازك
• تخزين دائم في محادثتك

🚀 <b>كيفية الاستخدام:</b>
أرسل رابط فيديو (يوتيوب، تيك توك، إلخ)

📌 <b>الأوامر المتاحة:</b>
/start - بدء البوت
/status - حالة البوت
/ping - اختبار الاتصال
/reset - إعادة تعيين البوت

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

@bot.message_handler(commands=['reset'])
def reset_command(message):
    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.reply_to(message, "🔄 تم إعادة تعيين البوت بنجاح")
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في الإعادة: {str(e)[:100]}")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text
    if text.startswith('http'):
        bot.reply_to(message, f"""
🔗 <b>تم استلام الرابط:</b>
{text}

⏳ <i>جاري المعالجة...</i>
📤 <i>سيتم رفع الفيديو مباشرة إلى هذه المحادثة</i>

💡 <i>ملاحظة:</i> خاصية التحميل قيد التطوير
سيتم إضافة yt-dlp قريباً لتحميل الفيديوهات
        """)
    else:
        bot.reply_to(message, "📌 أرسل رابط فيديو (يوتيوب، تيك توك، إلخ) أو استخدم /start")

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
