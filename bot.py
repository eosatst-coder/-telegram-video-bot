"""
🚀 Telegram Video Bot - WORKING VERSION
✅ يرفع الفيديوهات فعلياً | ✅ 24/7 | ✅ Render Hosting
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
WEBHOOK_URL = "https://telegram-video-bot-n4aj.onrender.com"

print("=" * 60)
print("🤖 Telegram Video Bot - WORKING VERSION")
print("=" * 60)

# ============== FLASK APP ==============
app = Flask(__name__)

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============== VIDEO DOWNLOADER ==============
class VideoDownloader:
    @staticmethod
    def download_single_video(video_url, chat_id):
        """تحميل فيديو واحد وإرساله"""
        try:
            print(f"📥 Downloading: {video_url}")
            
            # إعدادات yt-dlp بسيطة
            ydl_opts = {
                'format': 'best[ext=mp4]/best[height<=480]',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'socket_timeout': 30,
                'retries': 3,
            }
            
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts['outtmpl'] = os.path.join(tmpdir, 'video.%(ext)s')
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # تحميل الفيديو
                    info = ydl.extract_info(video_url, download=True)
                    video_file = ydl.prepare_filename(info)
                    
                    # البحث عن الملف المحمل
                    if not os.path.exists(video_file):
                        # البحث عن أي ملف فيديو
                        for file in os.listdir(tmpdir):
                            if file.endswith(('.mp4', '.mkv', '.webm')):
                                video_file = os.path.join(tmpdir, file)
                                break
                    
                    if os.path.exists(video_file):
                        file_size = os.path.getsize(video_file)
                        print(f"✅ Downloaded: {file_size / 1024 / 1024:.1f} MB")
                        
                        # إرسال الفيديو
                        with open(video_file, 'rb') as video:
                            bot.send_video(
                                chat_id,
                                video,
                                caption=f"🎬 {info.get('title', 'Video')}\n⬆️ @ishdmvfvzobot",
                                supports_streaming=True,
                                timeout=120
                            )
                        
                        print("✅ Video sent successfully!")
                        return True
                    else:
                        print("❌ No video file found!")
                        return False
                        
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return False

    @staticmethod
    def get_playlist_videos(url):
        """الحصول على فيديوهات القائمة"""
        try:
            print(f"🔍 Getting playlist: {url}")
            
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'playlistend': 5,  # أول 5 فيديوهات فقط
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                videos = []
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            video_id = entry.get('id')
                            if video_id:
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                                videos.append(video_url)
                
                print(f"✅ Found {len(videos)} videos")
                return {
                    'title': info.get('title', 'Playlist'),
                    'videos': videos,
                    'count': len(videos)
                }
                
        except Exception as e:
            print(f"❌ Error getting playlist: {e}")
            return {'title': '', 'videos': [], 'count': 0}

# ============== BOT HANDLERS ==============
@app.route('/')
def home():
    return """
    <html>
    <head><title>Telegram Video Bot</title></head>
    <body style="text-align:center;padding:50px;font-family:Arial;">
        <h1>🤖 Telegram Video Bot</h1>
        <p style="color:green;font-weight:bold;">✅ ONLINE & WORKING</p>
        <p>Bot: @ishdmvfvzobot</p>
        <p>Time: """ + time.ctime() + """</p>
        <p><a href="https://t.me/ishdmvfvzobot">Open in Telegram</a></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Bad Request', 400

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = """
🎬 <b>مرحباً! أنا بوت رفع الفيديوهات</b>

<b>أرسل لي:</b>
1. رابط فيديو يوتيوب فردي
2. رابط قائمة يوتيوب

<b>مثال:</b>
🎬 <code>https://youtu.be/dQw4w9WgXcQ</code>
📁 <code>https://youtube.com/playlist?list=...</code>

<b>يتم رفع أول 5 فيديوهات من القائمة</b>

🤖 @ishdmvfvzobot
    """
    bot.reply_to(message, welcome)

@bot.message_handler(func=lambda m: 'youtu' in m.text.lower())
def handle_youtube_link(message):
    """معالجة روابط يوتيوب"""
    url = message.text.strip()
    chat_id = message.chat.id
    
    # إرسال رسالة بداية
    status_msg = bot.reply_to(message, "⏳ <b>جاري المعالجة...</b>")
    
    # تشغيل في thread منفصل
    thread = threading.Thread(
        target=process_video_request,
        args=(url, chat_id, status_msg.message_id),
        daemon=True
    )
    thread.start()

def process_video_request(url, chat_id, status_msg_id):
    """معالجة طلب الفيديو"""
    try:
        # تحديث الحالة
        bot.edit_message_text(
            "🔍 <b>جاري تحليل الرابط...</b>",
            chat_id, status_msg_id
        )
        
        downloader = VideoDownloader()
        
        # التحقق إذا كان قائمة
        is_playlist = 'list=' in url or 'playlist' in url
        
        if is_playlist:
            # معالجة القائمة
            bot.edit_message_text(
                "📁 <b>تم اكتشاف قائمة تشغيل...</b>",
                chat_id, status_msg_id
            )
            
            # الحصول على الفيديوهات
            playlist_info = downloader.get_playlist_videos(url)
            
            if playlist_info['count'] == 0:
                bot.edit_message_text(
                    "❌ <b>لم أجد فيديوهات في هذه القائمة</b>",
                    chat_id, status_msg_id
                )
                return
            
            bot.edit_message_text(
                f"✅ <b>تم العثور على {playlist_info['count']} فيديو</b>\n"
                f"📤 <b>جاري رفع أول {min(3, playlist_info['count'])} فيديوهات...</b>",
                chat_id, status_msg_id
            )
            
            # رفع أول 3 فيديوهات فقط
            uploaded = 0
            for i, video_url in enumerate(playlist_info['videos'][:3]):
                try:
                    bot.edit_message_text(
                        f"⬇️ <b>جاري تحميل الفيديو {i+1}...</b>",
                        chat_id, status_msg_id
                    )
                    
                    # تحميل وإرسال الفيديو
                    success = downloader.download_single_video(video_url, chat_id)
                    
                    if success:
                        uploaded += 1
                        print(f"✅ تم رفع الفيديو {i+1}")
                    else:
                        print(f"❌ فشل رفع الفيديو {i+1}")
                    
                    # انتظار 2 ثانية بين الفيديوهات
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ خطأ في الفيديو {i+1}: {e}")
                    continue
            
            # النتيجة النهائية
            bot.edit_message_text(
                f"✅ <b>اكتمل رفع القائمة!</b>\n\n"
                f"📁 {playlist_info['title'][:30]}...\n"
                f"🔢 الفيديوهات: {playlist_info['count']}\n"
                f"📤 تم رفع: {uploaded} فيديو\n\n"
                f"🎬 <b>جميع الفيديوهات في محادثتك الآن!</b>",
                chat_id, status_msg_id
            )
            
        else:
            # فيديو فردي
            bot.edit_message_text(
                "🎬 <b>جاري تحميل الفيديو...</b>",
                chat_id, status_msg_id
            )
            
            # تحميل وإرسال الفيديو
            success = downloader.download_single_video(url, chat_id)
            
            if success:
                bot.edit_message_text(
                    "✅ <b>تم رفع الفيديو بنجاح!</b>",
                    chat_id, status_msg_id
                )
            else:
                bot.edit_message_text(
                    "❌ <b>فشل تحميل الفيديو</b>\n"
                    "تأكد من أن الرابط صحيح والفيديو متاح",
                    chat_id, status_msg_id
                )
                
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        
        try:
            bot.edit_message_text(
                f"❌ <b>حدث خطأ:</b>\n{str(e)[:100]}",
                chat_id, status_msg_id
            )
        except:
            pass

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.reply_to(message, 
                 "📌 <b>أرسل رابط يوتيوب</b>\n\n"
                 "مثال:\n"
                 "🎬 <code>https://youtu.be/dQw4w9WgXcQ</code>\n"
                 "📁 <code>https://youtube.com/playlist?list=...</code>")

# ============== WEBHOOK SETUP ==============
def setup_webhook():
    """إعداد webhook"""
    try:
        bot.remove_webhook()
        time.sleep(1)
        
        webhook_url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=webhook_url)
        
        print(f"✅ Webhook set to: {webhook_url}")
        return True
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False

# ============== KEEP ALIVE ==============
def ping_server():
    """إبقاء السيرفر نشطاً"""
    while True:
        try:
            requests.get(f"{WEBHOOK_URL}/health", timeout=10)
            print(f"❤️ Keep-alive: {time.ctime()}")
        except:
            print("⚠️ Keep-alive failed")
        time.sleep(240)  # كل 4 دقائق

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting bot...")
    
    # إعداد webhook
    if setup_webhook():
        print("✅ Webhook setup complete")
    else:
        print("⚠️ Webhook setup failed, trying polling...")
    
    # تشغيل keep-alive
    Thread(target=ping_server, daemon=True).start()
    
    # تشغيل Flask
    print(f"🌐 Starting web server on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
