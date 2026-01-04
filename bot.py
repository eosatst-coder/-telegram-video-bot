"""
🎬 Telegram Video Bot - Render Hosting (Webhook Version)
✅ 24/7 Online | ✅ Real Upload | ✅ No Conflict
"""

import os
import time
import telebot
import requests
import tempfile
import threading
import traceback
from flask import Flask, request
from threading import Thread
import yt_dlp

# ============== CONFIG ==============
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8288842404:AAEp6wAU8EC3uepgsuwuzYkBO_Mv3nMecp4')
PORT = int(os.environ.get('PORT', 10000))
WEBHOOK_URL = "https://telegram-video-bot-n4aj.onrender.com"  # رابط Render الخاص بك
MAX_VIDEOS = 5

print("=" * 60)
print("🎬 Telegram Video Bot - Webhook Version")
print("=" * 60)

# ============== FLASK APP ==============
app = Flask(__name__)

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============== VIDEO FUNCTIONS ==============
def extract_playlist_info(url):
    """استخراج معلومات القائمة"""
    try:
        print(f"🔍 استخراج القائمة: {url}")
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'playlistend': MAX_VIDEOS,
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_urls = []
            if 'entries' in info:
                for entry in info['entries'][:MAX_VIDEOS]:
                    if entry:
                        video_url = f"https://www.youtube.com/watch?v={entry.get('id')}"
                        video_urls.append(video_url)
            
            return {
                'success': True,
                'title': info.get('title', 'Playlist'),
                'video_urls': video_urls
            }
    except Exception as e:
        print(f"❌ خطأ في استخراج القائمة: {e}")
        return {'success': False}

def download_video(video_url):
    """تحميل فيديو واحد"""
    try:
        print(f"📥 تحميل: {video_url}")
        
        ydl_opts = {
            'format': 'best[height<=480]',  # جودة منخفضة لسرعة التحميل
            'quiet': False,
            'no_warnings': False,
            'outtmpl': '%(title).50s.%(ext)s',
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, 'video.mp4')
            ydl_opts['outtmpl'] = temp_file
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # تحميل الفيديو
                info = ydl.extract_info(video_url, download=True)
                
                # البحث عن الملف المحمل
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mkv', '.webm')):
                        actual_file = os.path.join(temp_dir, file)
                        
                        with open(actual_file, 'rb') as f:
                            video_data = f.read()
                        
                        return {
                            'success': True,
                            'data': video_data,
                            'title': info.get('title', 'video')[:50],
                            'size': len(video_data)
                        }
        
        return {'success': False}
        
    except Exception as e:
        print(f"❌ خطأ في التحميل: {e}")
        return {'success': False}

def process_playlist_async(url, chat_id, message_id):
    """معالجة القائمة في خلفية"""
    try:
        # تحليل القائمة
        bot.edit_message_text(
            "🔍 جاري تحليل قائمة التشغيل...",
            chat_id, message_id
        )
        
        playlist_info = extract_playlist_info(url)
        
        if not playlist_info['success'] or len(playlist_info['video_urls']) == 0:
            bot.edit_message_text(
                "❌ لا يمكن قراءة القائمة أو لا تحتوي على فيديوهات",
                chat_id, message_id
            )
            return
        
        video_urls = playlist_info['video_urls']
        
        bot.edit_message_text(
            f"✅ تم اكتشاف {len(video_urls)} فيديو\n"
            f"📤 جاري رفع {min(3, len(video_urls))} فيديوهات...",
            chat_id, message_id
        )
        
        # رفع أول 3 فيديوهات فقط للتجربة
        uploaded = 0
        for i, video_url in enumerate(video_urls[:3]):
            try:
                bot.edit_message_text(
                    f"⏬ جاري تحميل الفيديو {i+1}...",
                    chat_id, message_id
                )
                
                # تحميل الفيديو
                video_result = download_video(video_url)
                
                if video_result['success']:
                    bot.edit_message_text(
                        f"⏫ جاري رفع الفيديو {i+1}...",
                        chat_id, message_id
                    )
                    
                    # رفع الفيديو
                    bot.send_video(
                        chat_id,
                        video_result['data'],
                        caption=f"🎬 الفيديو {i+1} - {video_result['title']}\n⬆️ @ishdmvfvzobot",
                        supports_streaming=True,
                        timeout=120
                    )
                    
                    uploaded += 1
                    print(f"✅ تم رفع الفيديو {i+1}")
                else:
                    print(f"❌ فشل تحميل الفيديو {i+1}")
                
                time.sleep(1)  # انتظار بين الفيديوهات
                
            except Exception as e:
                print(f"❌ خطأ في الفيديو {i+1}: {e}")
                continue
        
        # النتيجة النهائية
        bot.edit_message_text(
            f"✅ اكتمل الرفع!\n"
            f"📤 تم رفع {uploaded} من {len(video_urls[:3])} فيديو",
            chat_id, message_id
        )
        
    except Exception as e:
        print(f"❌ خطأ في معالجة القائمة: {e}")
        traceback.print_exc()

# ============== BOT HANDLERS ==============
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Telegram Video Bot</title></head>
    <body style="text-align:center;padding:50px;">
        <h1>🤖 Telegram Video Bot</h1>
        <p>✅ Online & Working</p>
        <p>Bot: @ishdmvfvzobot</p>
        <p><a href="https://t.me/ishdmvfvzobot">Open in Telegram</a></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Invalid content type', 403

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 *مرحباً! أنا بوت رفع الفيديوهات*

*المميزات:*
• رفع فيديوهات فردية من يوتيوب
• رفع قوائم تشغيل يوتيوب (أول 3 فيديوهات)
• يعمل 24/7

*كيفية الاستخدام:*
1. أرسل رابط فيديو يوتيوب فردي
2. أو أرسل رابط قائمة يوتيوب
3. انتظر قليلاً

*مثال:*
🎬 فيديو: https://youtu.be/dQw4w9WgXcQ
📁 قائمة: https://youtube.com/playlist?list=...
    """
    bot.reply_to(message, welcome, parse_mode='Markdown')

@bot.message_handler(func=lambda m: 'youtube.com' in m.text or 'youtu.be' in m.text)
def handle_youtube(message):
    url = message.text.strip()
    
    # إرسال رسالة تأكيد
    msg = bot.reply_to(message, "🎬 *جاري معالجة الطلب...*\n\n⏳ الرجاء الانتظار...", parse_mode='Markdown')
    
    # تشغيل في thread منفصل
    thread = threading.Thread(
        target=process_playlist_async,
        args=(url, message.chat.id, msg.message_id),
        daemon=True
    )
    thread.start()

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.reply_to(message, 
                 "📌 أرسل رابط يوتيوب (فيديو أو قائمة)\n\n"
                 "مثال:\n"
                 "🎬 https://youtu.be/dQw4w9WgXcQ\n"
                 "📁 https://youtube.com/playlist?list=...")

# ============== SETUP WEBHOOK ==============
def setup_webhook():
    """إعداد Webhook"""
    try:
        # إزالة أي webhook سابق
        bot.remove_webhook()
        time.sleep(1)
        
        # تعيين webhook جديد
        webhook_path = f"{WEBHOOK_URL}/webhook"
        print(f"🌐 Setting webhook to: {webhook_path}")
        
        bot.set_webhook(url=webhook_path)
        
        # التحقق من Webhook
        time.sleep(2)
        info = bot.get_webhook_info()
        print(f"✅ Webhook Info: {info.url}")
        print(f"✅ Webhook Status: {'Active' if info.pending_update_count != -1 else 'Inactive'}")
        
        return True
    except Exception as e:
        print(f"❌ Error setting webhook: {e}")
        return False

# ============== KEEP ALIVE ==============
def keep_alive():
    """إبقاء الخادم نشطاً"""
    while True:
        try:
            requests.get(f'{WEBHOOK_URL}/health', timeout=10)
            print(f"❤️ Keep-alive at {time.ctime()}")
        except:
            print("⚠️ Keep-alive failed")
        time.sleep(300)  # كل 5 دقائق

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting Telegram Video Bot...")
    
    # إعداد Webhook
    if setup_webhook():
        print("✅ Webhook setup complete")
    else:
        print("❌ Webhook setup failed")
    
    # تشغيل keep-alive في خلفية
    Thread(target=keep_alive, daemon=True).start()
    
    # تشغيل Flask
    print(f"🌐 Starting Flask on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
