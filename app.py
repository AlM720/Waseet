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

# قراءة الرابط من المتصفح
query_params = st.query_params
yt_url = query_params.get("url")

if yt_url:
    # تحميل سريع (صوت فقط) لتجنب التأخير
    out_file = f"bridge_{int(time.time())}.mp3"
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': out_file, 'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        direct_link = upload_to_catbox(out_file)
        if direct_link:
            # كتابة الرابط في أول سطر بالصفحة لضمان رؤيته
            st.write(f"DOWNLOAD_READY_LINK:{direct_link}")
            os.remove(out_file)
        else:
            st.write("ERROR:UPLOAD_FAILED")
    except Exception as e:
        st.write(f"ERROR:{str(e)}")
    st.stop() # إيقاف كل شيء وإرسال النص فقط
else:
    st.title("Downloader Bridge 24/7")
    st.write("بانتظار الأوامر...")
