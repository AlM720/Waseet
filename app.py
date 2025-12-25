import streamlit as st
import yt_dlp
import os
import requests
import time

def upload_to_catbox(file_path):
    """إصلاح وظيفة الرفع لضمان الحصول على رابط صحيح"""
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            # تم فصل البيانات (data) عن الملفات (files) لضمان قبولها من السيرفر
            data = {"reqtype": "fileupload"}
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
        
        # التأكد أن النتيجة تبدأ بـ https (رابط حقيقي وليس رسالة خطأ)
        if response.text.startswith("https"):
            return response.text
        else:
            return f"ERROR_FROM_SERVER: {response.text}"
    except Exception as e:
        return f"EXCEPTION: {str(e)}"

st.set_page_config(page_title="Bridge Monitor 🚀")
cookies_content = st.secrets.get("coce")
yt_url = st.query_params.get("url")

if yt_url:
    out_file = f"bridge_{int(time.time())}.mp3"
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': out_file, 'nocheckcertificate': True}

    if cookies_content:
        with open("cookies.txt", "w") as f: f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        
        # الرفع باستخدام الدالة المصلحة
        direct_link = upload_to_catbox(out_file)
        
        if direct_link and direct_link.startswith("https"):
            # إرسال الرابط الصافي لهاجينج فيس
            st.write(f"BRIDGE_LINK_START{direct_link}BRIDGE_LINK_END")
            st.success("✅ الرابط جاهز للهاجينج فيس!")
        else:
            st.error(f"❌ فشل الرفع: {direct_link}")
            st.write("BRIDGE_LINK_FAILED")
            
        if os.path.exists(out_file): os.remove(out_file)
    except Exception as e:
        st.write(f"DOWNLOAD_ERROR:{str(e)}")
    
    if os.path.exists("cookies.txt"): os.remove("cookies.txt")
    st.stop()
else:
    st.title("جسر التحميل والمراقبة 📡")
    st.info("جاهز بانتظار الطلبات...")
