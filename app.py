import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return "ERROR:FILE_EMPTY"
            
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload"}
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
        return response.text if response.text.startswith("https") else f"ERROR:{response.text}"
    except Exception as e:
        return f"EXCEPTION:{str(e)}"

st.set_page_config(page_title="Bridge Pro 2025")
cookies_content = st.secrets.get("coce")
yt_url = st.query_params.get("url")

if yt_url:
    out_file = f"valid_audio_{int(time.time())}.mp3"
    # إعدادات تحميل تضمن الحصول على ملف صوتي حقيقي
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    if cookies_content:
        with open("cookies.txt", "w") as f: f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        # التأكد من حجم الملف قبل الرفع
        file_size = os.path.getsize(out_file) if os.path.exists(out_file) else 0
        
        if file_size > 1000: # أكثر من 1 كيلوبايت لضمان المحتوى
            direct_link = upload_to_catbox(out_file)
            st.write(f"BRIDGE_LINK_START{direct_link}BRIDGE_LINK_END")
            st.write(f"DEBUG_SIZE:{file_size}")
        else:
            st.write("BRIDGE_LINK_START_ERROR:FILE_WAS_EMPTY_ON_SERVER_BRIDGE_LINK_END")
            
        if os.path.exists(out_file): os.remove(out_file)
    except Exception as e:
        st.write(f"BRIDGE_LINK_START_ERROR:{str(e)}_BRIDGE_LINK_END")
    
    if os.path.exists("cookies.txt"): os.remove("cookies.txt")
    st.stop()
else:
    st.title("Downloader Bridge Pro 📡")
    st.info("جاهز وبانتظار طلبات هاجينج فيس...")
