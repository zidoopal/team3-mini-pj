from flask import make_response, redirect, url_for, session, Blueprint
from flask_oauthlib.client import OAuth
from pymongo import MongoClient
import certifi
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

google_bp = Blueprint('google_oauth', __name__)

# 환경변수 설정
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')

# 몽고DB 연결
ca = certifi.where()
client = MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.ebm0gtg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.miniproject

oauth = OAuth()

# 구글 소셜로그인
google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# tokengetter 함수
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@google_bp.route('/login/google', methods=['GET', 'POST'])
def login_google():
    return google.authorize(callback=url_for('google_oauth.authorized', _external=True))

from flask import render_template_string

@google_bp.route('/auth/authorized', methods=['GET', 'POST'])
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return "요청이 거부되었습니다."
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo').data

    # 사용자 DB에서 이메일로 사용자를 찾습니다.
    user = db.google_users.find_one({'email': user_info['email']})
    
    # 사용자가 DB에 없으면 새로운 사용자를 추가합니다.
    if not user:
        user = {
            "email": user_info["email"],
            "name": user_info['name']
        }
        db.google_users.insert_one(user)

    # 클라이언트 로컬 스토리지에 정보를 저장하는 JavaScript 코드를 작성합니다.
    js_template = """
    <script>
        localStorage.setItem('email', '{{ email }}');
        localStorage.setItem('name', '{{ name }}');
        localStorage.setItem('picture', '{{ picture }}');
        setTimeout(function(){
            window.location.href = "{{ redirect_url }}"; // 이동할 페이지 URL
        }, 0);
    </script>
    """

    # JavaScript 코드에 필요한 정보를 채워서 응답으로 전송합니다.
    resp = make_response(render_template_string(js_template, email=user_info['email'], name=user_info['name'], picture=user_info['picture'], redirect_url=url_for('get_main_page')))
    resp.set_cookie('AccessToken', 'google_' + response['access_token'])
    return resp
