from flask import Flask, render_template
from login import *
import os
from flask_oauthlib.client import OAuth



# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

oauth = OAuth()
oauth.init_app(app)

# 소셜로그인 설정
oauth = OAuth(app)

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


# tokengetter 함수
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# 구글 소셜로그인 기능
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

    return render_template('index.html')


# 회원 인증 기능
@app.route('/auth/verify', methods=['POST'])
def verify_user():
    return verify_token()

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