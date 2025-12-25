import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    """رفع الملف للحصول على رابط مباشر يتجاوز حظر هاجينج فيس"""
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "fileToUpload": (file_path, f)}
            response = requests.post(url, files=data)
        return response.text # يعيد رابط مباشر مثل https://files.catbox.moe/xxxx.mp4
    except:
        return None

st.title("جسر التحميل الذكي 🚀")
st.write("هذا التطبيق يعمل كخادم خلفي لمشروع هاجينج فيس")

# قراءة الرابط من Query Params (للسماح للهاجينج فيس بالاتصال به تلقائياً)
query_params = st.query_params
yt_url = query_params.get("url")

if yt_url:
    st.info(f"جاري معالجة الرابط: {yt_url}")
    out_file = f"video_{int(time.time())}.mp4"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_file,
        'nocheckcertificate': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    
    direct_link = upload_to_catbox(out_file)
    if direct_link:
        st.success("تم التحميل والرفع!")
        st.code(direct_link) # سيظهر الرابط هنا ليقرأه هاجينج فيس
        os.remove(out_file)
    else:
        st.error("فشل الرفع لمستودع catbox")
