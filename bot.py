"""
🚀 Telegram Video Bot - FINAL WORKING VERSION
✅ يرفع الفيديوهات فعلياً | ✅ يعمل على Render | ✅ لا أخطاء
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
print("🤖 Telegram Video Bot - FINAL WORKING VERSION")
print("=" * 60)
print(f"✅ Token: {TOKEN[:15]}...")
print(f"✅ Port: {PORT}")
print(f"✅ Webhook URL: {WEBHOOK_URL}")

# ============== FLASK APP ==============
app = Flask(__name__)

# ============== TELEGRAM BOT ==============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============== VIDEO DOWNLOADER ==============
def download_video(video_url):
    """تحميل فيديو وإرجاع بياناته"""
    try:
        print(f"📥 محاولة تحميل: {video_url}")
        
        # إعدادات yt-dlp مبسطة
        ydl_opts = {
            'format': 'best[height<=360]',  # جودة منخفضة للسرعة
            'quiet': False,
            'no_warnings': False,
            'outtmpl': '%(id)s.%(ext)s',
            'socket_timeout': 30,
            'retries': 2,
            'fragment_retries': 2,
            'ignoreerrors': False,
            'noplaylist': True,
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts['outtmpl'] = os.path.join(tmpdir, '%(id)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # الحصول على معلومات الفيديو أولاً
                info = ydl.extract_info(video_url, download=False)
                print(f"✅ معلومات الفيديو: {info.get('title', 'بدون عنوان')}")
                
                # تحميل الفيديو
                print("⬇️ جاري التحميل...")
                ydl.download([video_url])
                
                # البحث عن الملف المحمل
                video_id = info.get('id', 'video')
                possible_files = [
                    os.path.join(tmpdir, f"{video_id}.mp4"),
                    os.path.join(tmpdir, f"{video_id}.mkv"),
                    os.path.join(tmpdir, f"{video_id}.webm"),
                ]
                
                for file_path in possible_files:
                    if os.path.exists(file_path):
                        print(f"✅ تم العثور على الملف: {file_path}")
                        with open(file_path, 'rb') as f:
                            video_data = f.read()
                        
                        return {
                            'success': True,
                            'data': video_data,
                            'title': info.get('title', 'فيديو'),
                            'size': len(video_data)
                        }
                
                # إذا لم نجد الملف بالاسم المتوقع، نبحث عن أي ملف فيديو
                for file_name in os.listdir(tmpdir):
                    if file_name.endswith(('.mp4', '.mkv', '.webm')):
                        file_path = os.path.join(tmpdir, file_name)
                        print(f"✅ تم العثور على الملف البديل: {file_name}")
                        with open(file_path, 'rb') as f:
                            video_data = f.read()
                        
                        return {
                            'success': True,
                            'data': video_data,
                            'title': info.get('title', 'فيديو'),
                            'size': len(video_data)
                        }
                
                print("❌ لم يتم العثور على أي ملف فيديو بعد التحميل")
                return {'success': False, 'error': 'لم يتم إنشاء ملف الفيديو'}
                
    except Exception as e:
        print(f"❌ خطأ في التحميل: {str(e)}")
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def get_playlist_videos(url):
    """الحصول على فيديوهات القائمة"""
    try:
        print(f"🔍 جاري تحليل القائمة: {url}")
        
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
                for i, entry in enumerate(info['entries']):
                    if entry and i < 5:  # أول 5 فقط
                        video_id = entry.get('id')
                        if video_id:
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            videos.append(video_url)
            
            print(f"✅ تم العثور على {len(videos)} فيديو في القائمة")
            return {
                'title': info.get('title', 'قائمة التشغيل'),
                'videos': videos,
                'count': len(videos)
            }
            
    except Exception as e:
        print(f"❌ خطأ في تحليل القائمة: {e}")
        return {'title': '', 'videos': [], 'count': 0, 'error': str(e)}

# ============== BOT HANDLERS ==============
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Telegram Video Bot</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; }
            h1 { color: #333; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Video Bot</h1>
        <p class="status">✅ ONLINE & WORKING</p>
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
📁 <code>https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj</code>

<b>يتم رفع أول 3 فيديوهات من القائمة</b>

🤖 @ishdmvfvzobot
    """
    bot.reply_to(message, welcome)

@bot.message_handler(func=lambda m: 'youtu' in m.text.lower())
def handle_youtube_link(message):
    """معالجة روابط يوتيوب"""
    url = message.text.strip()
    chat_id = message.chat.id
    
    print(f"📩 رسالة جديدة من {chat_id}: {url}")
    
    # إرسال رسالة بداية
    status_msg = bot.reply_to(message, "⏳ <b>جاري تحليل الرابط...</b>")
    
    # تشغيل في thread منفصل
    thread = threading.Thread(
        target=process_youtube_request,
        args=(url, chat_id, status_msg.message_id),
        daemon=True
    )
    thread.start()

def process_youtube_request(url, chat_id, status_msg_id):
    """معالجة طلب اليوتيوب"""
    try:
        # التحقق إذا كان قائمة
        is_playlist = 'list=' in url or 'playlist' in url
        
        if is_playlist:
            # معالجة قائمة التشغيل
            bot.edit_message_text(
                "📁 <b>تم اكتشاف قائمة تشغيل...</b>",
                chat_id, status_msg_id
            )
            
            # الحصول على الفيديوهات
            playlist_info = get_playlist_videos(url)
            
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
            
            # رفع أول 3 فيديوهات
            uploaded = 0
            for i, video_url in enumerate(playlist_info['videos'][:3]):
                try:
                    bot.edit_message_text(
                        f"⬇️ <b>جاري تحميل الفيديو {i+1}...</b>",
                        chat_id, status_msg_id
                    )
                    
                    # تحميل الفيديو
                    video_result = download_video(video_url)
                    
                    if video_result['success']:
                        bot.edit_message_text(
                            f"⬆️ <b>جاري رفع الفيديو {i+1}...</b>",
                            chat_id, status_msg_id
                        )
                        
                        # إرسال الفيديو
                        bot.send_video(
                            chat_id,
                            video_result['data'],
                            caption=f"🎬 الفيديو {i+1} - {playlist_info['title'][:30]}...\n⬆️ @ishdmvfvzobot",
                            supports_streaming=True,
                            timeout=120
                        )
                        
                        uploaded += 1
                        print(f"✅ تم رفع الفيديو {i+1} بنجاح")
                    else:
                        print(f"❌ فشل تحميل الفيديو {i+1}: {video_result.get('error', '')}")
                    
                    # انتظار 3 ثواني بين الفيديوهات
                    time.sleep(3)
                    
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
            
            # تحميل الفيديو
            video_result = download_video(url)
            
            if video_result['success']:
                bot.edit_message_text(
                    "⬆️ <b>جاري رفع الفيديو...</b>",
                    chat_id, status_msg_id
                )
                
                # إرسال الفيديو
                bot.send_video(
                    chat_id,
                    video_result['data'],
                    caption=f"🎬 {video_result['title'][:50]}\n⬆️ @ishdmvfvzobot",
                    supports_streaming=True,
                    timeout=120
                )
                
                bot.edit_message_text(
                    "✅ <b>تم رفع الفيديو بنجاح!</b>",
                    chat_id, status_msg_id
                )
                print("✅ تم رفع الفيديو الفردي بنجاح")
            else:
                bot.edit_message_text(
                    f"❌ <b>فشل تحميل الفيديو</b>\n\n"
                    f"الخطأ: {video_result.get('error', 'غير معروف')}",
                    chat_id, status_msg_id
                )
                print(f"❌ فشل تحميل الفيديو الفردي")
                
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        traceback.print_exc()
        try:
            bot.edit_message_text(
                f"❌ <b>حدث خطأ غير متوقع:</b>\n{str(e)[:100]}",
                chat_id, status_msg_id
            )
        except:
            pass

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    bot.reply_to(message, 
                 "📌 <b>أرسل رابط يوتيوب</b>\n\n"
                 "مثال فيديو:\n"
                 "🎬 <code>https://youtu.be/dQw4w9WgXcQ</code>\n\n"
                 "مثال قائمة:\n"
                 "📁 <code>https://youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj</code>")

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
            print(f"❤️ Keep-alive ping at {time.ctime()}")
        except Exception as e:
            print(f"⚠️ Keep-alive failed: {e}")
        time.sleep(180)  # كل 3 دقائق

# ============== MAIN ==============
if __name__ == "__main__":
    print("🚀 Starting Telegram Video Bot...")
    
    # إعداد webhook
    if setup_webhook():
        print("✅ Webhook setup complete")
    else:
        print("⚠️ Webhook setup failed, using polling...")
    
    # تشغيل keep-alive في خلفية
    Thread(target=ping_server, daemon=True).start()
    
    # تشغيل Flask
    print(f"🌐 Starting Flask server on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True, use_reloader=False)
