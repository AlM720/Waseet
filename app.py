import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    """رفع الملف للحصول على رابط مباشر"""
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "fileToUpload": (file_path, f)}
            response = requests.post(url, files=data)
        return response.text
    except:
        return None

# إعداد الواجهة
st.set_page_config(page_title="Bridge API")
query_params = st.query_params
yt_url = query_params.get("url")

if yt_url:
    # تحميل الفيديو بصيغة صوتية لتوفير الوقت والمساحة
    out_file = f"temp_{int(time.time())}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_file,
        'nocheckcertificate': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        direct_link = upload_to_catbox(out_file)
        
        if direct_link:
            # كتابة الرابط بين علامات خاصة ليقرأها هاجينج فيس بسهولة
            st.write(f"BRIDGE_LINK_START{direct_link}BRIDGE_LINK_END")
            os.remove(out_file)
        else:
            st.write("UPLOAD_FAILED")
    except Exception as e:
        st.write(f"DOWNLOAD_ERROR: {str(e)}")
    
    st.stop() # إيقاف التنفيذ لضمان إرسال نص نظيف
else:
    st.title("جسر التحميل يعمل 24/7 🚀")
    st.write("بانتظار الطلبات من هاجينج فيس...")
