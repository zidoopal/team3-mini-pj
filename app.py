from flask import Flask, render_template
from login import *
from signup import *
from detail import *
import boto3, os, jwt
from oauth import google_oauth, kakao_oauth
from flask_oauthlib.client import OAuth

# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
oauth = OAuth(app)

# 환경변수 설정
load_dotenv()
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')


# 몽고DB 연결
ca = certifi.where()
client = MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.ebm0gtg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.miniproject



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

# 상세 페이지 렌더링
@app.route('/detail/<id>', methods=['GET'])
def get_detail_page(id):
    return render_template('detail.html')

@app.route('/create-post', methods = ['GET'])
def get_createPost_page():
    return render_template('createPost.html')

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

# 이메일 유효성 검증
@app.route('/signup/email-verification', methods=['POST'])
def email_verification():
    return verify_email()

# 이메일 인증 요청
@app.route('/signup/send-email', methods=['POST'])
def send_verification_email():
    return send_email()

# 인증번호 검증
@app.route('/signup/verify-auth-code', methods=['POST'])
def verify_auth_code():
    return email_auth()

# 상세페이지 게시글 조회
@app.route('/api/detail/<post_id>', methods=['GET'])
def detail(post_id):
    post = get_post_detail(post_id)
    if post:
        return jsonify(post)
    else:
        return jsonify({"message": "존재하지 않는 게시글입니다."}), 404

# 댓글 추가
@app.route('/detail/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    comment = request.json.get('comment')
    user_name = request.json.get('name')
    user_picture = request.json.get('picture')

    if not comment or not user_name or not user_picture:
        return jsonify({"message": "올바르지 않은 형식입니다."}), 400

    if add_comment_to_db(post_id, comment, user_name, user_picture):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400

# 댓글 조회
@app.route('/detail/<post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = fetch_comments_from_db(post_id)
    return jsonify({"comments": comments})



# S3객체 생성
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id = os.environ.get("AWS_S3IMAGE_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_S3IMAGE_SECERT_ACCESS_KEY"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3
        
s3 = s3_connection()

# 이미지파일 S3에 저장 / 노래 제목, 가수, 이미지 url, 작성자는 db에 저장
@app.route("/upload", methods=["POST"])
def api_write():
    # html에서 가져온 정보
    file = request.files['image_give']
    title_receive = request.form['song_title_give']
    artist_receive = request.form['artist_give']
    d = datetime.now()
    date = str(d.year)+'년 '+str(d.month)+'월 '+str(d.day)+' 일'

    # 현재 로그인 사용자 정보
    # writer =get_user()

    # S3에 저장할 파일 이름 지정
    filename = file.filename.split('.')[0]
    ext = file.filename.split('.'[-1])
    img_name = datetime.now().strftime(f"{filename}-%Y-%m-%d-%H-%S.{ext}")

    # S3 버킷에 업로드
    image_url = s3_put_object(s3,'group3artistimage',file,img_name)
    

    # 게시글 숫자 세기
    post_list = list(db.posts.find({}, {'_id': False}))
    postId = len(post_list) + 1
    
    # mongodb에 저장
    doc = {
        'postId': postId,
        'user': '',
        'song_title': title_receive,
        'artist': artist_receive,
        'img_url': image_url,
        'createdAt': date
    }
    db.posts.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


# S3에 이미지 업로드
def s3_put_object(s3, bucket, file, filename):
    try:
        s3.put_object(
            Body=file, #업로드할 파일 객체
            Bucket=bucket,
            Key=f'images/{filename}', #S3에 업로드할 파일 경로
            ContentType=file.content_type, #image/jpeg ?
            ACL='public-read'
        )
        url = f'https://group3artistimage.s3.ap-northeast-2.amazonaws.com/images/{filename}'
        print(url)
        return url
    
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)