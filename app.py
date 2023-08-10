from flask import Flask, render_template
from login import *
from signup import *
from oauth import google_oauth, kakao_oauth
import os
from flask_oauthlib.client import OAuth
import jwt

# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
oauth = OAuth(app)

app.register_blueprint(google_oauth.google_bp)
app.register_blueprint(kakao_oauth.kakao_bp)


# 메인페이지 렌더링
@app.route('/', methods = ['GET'])
def get_main_page():
    return render_template('index.html')

# 로그인페이지 렌더링
@app.route('/login', methods = ['GET'])
def get_login_page():
    return render_template('login.html')

# 로그인 기능
@app.route('/login', methods=['POST'])
def login():
    return user_login()


# 회원 인증 기능
@app.route('/auth/verify', methods=['POST'])
def verify_token():
    # 쿠키에서 AccessToken을 가져옵니다.
    token = request.cookies.get('AccessToken')
    
    if not token:
        return jsonify({"message": "토큰이 존재하지 않습니다.", "authenticated": False}), 401

    # 토큰이 구글 토큰인지 확인
    if token.startswith('google_'):
        print('구글 토큰')
        return jsonify({"message": "OK", "authenticated": True}), 200
    
    # 토큰이 카카오 토큰인지 확인
    if token.startswith('kakao_'):
        print('카카오 토큰')
        return jsonify({"message": "OK", "authenticated": True}), 200

    
    try:
        # 일반 토큰 검증
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "OK", "authenticated": True}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "만료된 토큰입니다.", "authenticated": False}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "올바르지 않은 토큰입니다.", "authenticated": False}), 401



# 로그아웃 기능
@app.route('/logout', methods = ['POST'])
def logout():
    return user_logout()

# 회원가입
@app.route('/signup', methods = ['GET'])
def get_signup_page():
    return render_template('signup.html')

# 회원가입 기능
@app.route('/signup', methods=['POST'])
def signup():
    return user_signup()

# 글 등록 (Create)

# 조회 (Read)

# 수정 (Update)

# 삭제 (Delete)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)