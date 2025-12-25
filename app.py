import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload"} # تم إصلاح طلب الرفع
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
        return response.text if response.text.startswith("https") else None
    except: return None

st.set_page_config(page_title="Final Bridge 2025")
cookies_content = st.secrets.get("coce")
yt_url = st.query_params.get("url")

if yt_url:
    out_file = f"audio_{int(time.time())}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio', # اسم مؤقت
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True,
    }

    if cookies_content:
        with open("cookies.txt", "w") as f: f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        # الملف الناتج سيكون temp_audio.mp3
        actual_file = "temp_audio.mp3"
        
        if os.path.exists(actual_file):
            direct_link = upload_to_catbox(actual_file)
            if direct_link:
                st.write(f"BRIDGE_LINK_START{direct_link}BRIDGE_LINK_END")
            else: st.write("BRIDGE_LINK_START_ERROR:UPLOAD_FAILED_BRIDGE_LINK_END")
            os.remove(actual_file)
        else: st.write("BRIDGE_LINK_START_ERROR:CONVERSION_FAILED_BRIDGE_LINK_END")
            
    except Exception as e:
        st.write(f"BRIDGE_LINK_START_ERROR:{str(e)}_BRIDGE_LINK_END")
    
    if os.path.exists("cookies.txt"): os.remove("cookies.txt")
    st.stop()
