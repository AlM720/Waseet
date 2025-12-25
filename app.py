import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "fileToUpload": (file_path, f)}
            response = requests.post(url, files=data)
        return response.text
    except: return None

# جلب الكوكيز من Secrets الخاصة بـ Streamlit
cookies_content = st.secrets.get("coce") 

query_params = st.query_params
yt_url = query_params.get("url")

if yt_url:
    out_file = f"bridge_{int(time.time())}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_file,
        'nocheckcertificate': True,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # استخدام الكوكيز إذا كانت متوفرة
    if cookies_content:
        with open("cookies.txt", "w") as f:
            f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        direct_link = upload_to_catbox(out_file)
        if direct_link:
            # إرسال الرابط داخل العلامات ليقرأها هاجينج فيس
            st.write(f"DOWNLOAD_READY_LINK:{direct_link}")
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
            os.remove(out_file)
        else:
            st.write("ERROR:UPLOAD_FAILED")
    except Exception as e:
        st.write(f"ERROR:{str(e)}")
    st.stop()
else:
    st.title("Downloader Bridge with Cookies 🍪")
    st.write("الجسر يعمل الآن وبانتظار الطلبات...")
