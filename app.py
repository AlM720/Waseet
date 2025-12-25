import streamlit as st
import yt_dlp
import os
import requests
import time

# إعداد الصفحة لتكون مريحة على الجوال
st.set_page_config(page_title="Bridge Monitor 🚀", layout="centered")

def upload_to_catbox(file_path):
    try:
        url = "https://catbox.moe/user/api.php"
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "fileToUpload": (file_path, f)}
            response = requests.post(url, files=data)
        return response.text
    except: return None

# جلب الكوكيز من السكرت
cookies_content = st.secrets.get("coce")

st.title("جسر التحميل والمراقبة 📡")

# استقبال الرابط
yt_url = st.query_params.get("url")

if yt_url:
    st.info(f"جاري معالجة الرابط: {yt_url}")
    out_file = f"bridge_{int(time.time())}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_file,
        'nocheckcertificate': True,
        'quiet': False, # تفعيل السجلات للتأكد من العمل
    }

    if cookies_content:
        with open("cookies.txt", "w") as f:
            f.write(cookies_content)
        ydl_opts['cookiefile'] = "cookies.txt"

    with st.spinner("جاري التحميل من يوتيوب..."):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])
            
            st.success("تم تحميل الملف بنجاح من يوتيوب!")
            
            with st.spinner("جاري الرفع إلى Catbox..."):
                direct_link = upload_to_catbox(out_file)
            
            if direct_link:
                st.balloons()
                st.markdown("### ✅ الرابط المباشر جاهز:")
                st.code(direct_link) # يظهر لك الرابط لتنسخه وتتأكد منه
                
                # العلامة البرمجية لهاجينج فيس (لا تحذفها)
                st.write(f"BRIDGE_LINK_START{direct_link}BRIDGE_LINK_END")
                
                # خيار للتحميل اليدوي للتجربة
                st.link_button("افتح الرابط المباشر للتجربة", direct_link)
                
                os.remove(out_file)
            else:
                st.error("فشل الرفع إلى مستودع Catbox")
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
else:
    st.warning("بانتظار طلبات من هاجينج فيس... يمكنك وضع رابط يوتيوب في المتصفح يدوياً للتجربة هكذا:")
    st.code(f"https://your-app.streamlit.app/?url=رابط_اليوتيوب")

if os.path.exists("cookies.txt"): os.remove("cookies.txt")
