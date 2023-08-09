from flask import Flask, render_template
from login import *
import os
from flask_oauthlib.client import OAuth
import jwt

# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
oauth = OAuth(app)

# 소셜로그인 설정

# 구글 소셜로그인
google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# 카카오 소셜로그인
kakao = oauth.remote_app('kakao',
    consumer_key=os.environ.get('KAKAO_CLIENT_ID'),
    consumer_secret='team3', 
    request_token_params={'scope': 'profile_image, profile_nickname, account_email'},
    base_url='https://kapi.kakao.com/v2/user/me',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://kauth.kakao.com/oauth/token',
    authorize_url='https://kauth.kakao.com/oauth/authorize',
)



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




# 구글 소셜로그인 기능

# tokengetter 함수
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# 구글 소셜 로그인
@app.route('/login/google', methods=['GET', 'POST'])
def login_google():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/auth/authorized', methods=['GET', 'POST'])
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return "요청이 거부되었습니다."
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo').data
    print(user_info)

    # 사용자 DB에서 이메일로 사용자를 찾습니다.
    user = db.users.find_one({'email': user_info['email']})
    
    # 사용자가 DB에 없으면 새로운 사용자를 추가합니다.
    if not user:
        user = {
            "email": user_info["email"],
        }
        db.users.insert_one(user)

    # 메인 페이지로 리다이렉트하기 전에 쿠키에 액세스 토큰을 저장합니다.
    resp = make_response(redirect(url_for('get_main_page')))
    resp.set_cookie('AccessToken', 'google_' + response['access_token'])
    return resp

# 카카오 소셜로그인 기능
@kakao.tokengetter
def get_kakao_oauth_token():
    return session.get('kakao_token')

@app.route('/login/kakao', methods=['GET', 'POST'])
def login_kakao():
    return kakao.authorize(callback=url_for('kakao_authorized', _external=True))

@app.route('/auth/kakao_authorized', methods=['GET', 'POST'])
def kakao_authorized():
    response = kakao.authorized_response()
    if response is None or response.get('access_token') is None:
        return "요청이 거부되었습니다."
    session['kakao_token'] = (response['access_token'], '')
    kakao_user_info = kakao.get('https://kapi.kakao.com/v2/user/me')
    print(kakao_user_info.data)

    email = kakao_user_info.data.get('kakao_account', {}).get('email')
    if not email:
        return "이메일 정보를 가져올 수 없습니다."

    user = db.users.find_one({'email': email})
    
    # 사용자가 DB에 없으면 새로운 사용자를 추가합니다.
    if not user:
        user = {
            "email": email,
        }
        db.users.insert_one(user)

    # 메인 페이지로 리다이렉트하기 전에 쿠키에 액세스 토큰을 저장합니다.
    resp = make_response(redirect(url_for('get_main_page')))
    resp.set_cookie('AccessToken', 'kakao_' + response['access_token'])
    return resp



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

# 글 등록 (Create)

# 조회 (Read)

# 수정 (Update)

# 삭제 (Delete)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)