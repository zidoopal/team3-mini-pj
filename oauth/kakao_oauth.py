from flask import make_response, redirect, url_for, session, Blueprint, render_template_string
from flask_oauthlib.client import OAuth
from pymongo import MongoClient
import certifi
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

kakao_bp = Blueprint('kakao_oauth', __name__)

# 환경변수 설정
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')

# 몽고DB 연결
ca = certifi.where()
client = MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.ebm0gtg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.miniproject

oauth = OAuth()

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


# 카카오 소셜로그인 기능
@kakao.tokengetter
def get_kakao_oauth_token():
    return session.get('kakao_token')

@kakao_bp.route('/login/kakao', methods=['GET', 'POST'])
def login_kakao():
    return kakao.authorize(callback=url_for('kakao_oauth.kakao_authorized', _external=True))


@kakao_bp.route('/auth/kakao_authorized', methods=['GET', 'POST'])
def kakao_authorized():
    response = kakao.authorized_response()
    if response is None or response.get('access_token') is None:
        return "요청이 거부되었습니다."
    
    session['kakao_token'] = (response['access_token'], '')
    kakao_user_info = kakao.get('https://kapi.kakao.com/v2/user/me')
    print(kakao_user_info.data)

    email = kakao_user_info.data.get('kakao_account', {}).get('email')
    nickname = kakao_user_info.data.get('properties', {}).get('nickname')
    profile_image = kakao_user_info.data.get('properties', {}).get('profile_image')

    if not email:
        return "이메일 정보를 가져올 수 없습니다."

    # 사용자 DB에서 이메일로 사용자를 찾습니다.
    user = db.kakao_users.find_one({'email': email})
    
    # 사용자가 DB에 없으면 새로운 사용자를 추가합니다.
    if not user:
        user = {
            "email": email,
            "name": nickname
        }
        db.kakao_users.insert_one(user)

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
    resp = make_response(render_template_string(js_template, email=email, name=nickname, picture=profile_image, redirect_url=url_for('get_main_page')))
    resp.set_cookie('AccessToken', 'kakao_' + response['access_token'])
    return resp
