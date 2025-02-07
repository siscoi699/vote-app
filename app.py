from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(__name__)

# ملف لحفظ بيانات المصوتين
VOTERS_FILE = "voters.json"

# تحميل بيانات المصوتين
def load_voters():
    try:
        with open(VOTERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# حفظ بيانات المصوتين
def save_voters(data):
    with open(VOTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    if request.cookies.get('voted'):  # منع التصويت أكثر من مرة
        return jsonify({'message': '❌ لقد قمت بالتصويت مسبقًا!'}), 403

    data = request.json
    choice = data.get('choice')
    user_ip = request.remote_addr  # الحصول على عنوان IP للمستخدم

    voters = load_voters()
    voters[user_ip] = choice  # حفظ تصويت المستخدم بناءً على IP

    save_voters(voters)  # حفظ البيانات إلى الملف

    response = make_response(jsonify({'message': '✅ تم تسجيل تصويتك بنجاح!'}))
    response.set_cookie('voted', 'true', max_age=86400)  # منع التصويت لمدة 24 ساعة

    return response

@app.route('/voters')
def show_voters():
    voters = load_voters()
    return render_template('voters.html', voters=voters)

if __name__ == '__main__':
    app.run(debug=True)
