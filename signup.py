from flask import request, jsonify
from hash import hash_password
from email_validator import validate_email, EmailNotValidError
import certifi
from pymongo import MongoClient
# 환경변수 설정
import os
from dotenv import load_dotenv
load_dotenv()
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')


# 몽고DB 연결
ca = certifi.where()
# TODO 테스트를 위해 나의 db 에 연결 되어서 추후에 전체 공용 DB 로 변경해야함
client = MongoClient('mongodb+srv://sparta:test@cluster0.voucrah.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.miniproject

def user_signup():
    email = request.form['email_give']
    password = request.form['password_give']
    confirmPassword = request.form['confirmPassword_give']
    nickname = request.form['nickname_give']

    ## 로그인 검증
    # 이메일 유효성 검사
    try :
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'msg':'유효하지 않은 이메일 입니다!'}), 401
    
    # 중복 이메일 검사
    findUser = db.users.find_one({'email': email} ,{'_id':False})
    if(findUser):
        return jsonify({'msg':'이미 등록된 이메일 입니다!'}), 401

     # 중복 닉네임 검사
    findUser = db.users.find_one({'nickname': nickname} ,{'_id':False})
    if(findUser):
        return jsonify({'msg':'이미 등록된 닉네임 입니다!'}), 401
    
    # 비밀번호 길이 검사
    if len(password) < 5 or len(password) > 20:
        return jsonify({'msg':'비밀번호는 5자리 이상 20자리 이하로 해주세요!'}), 401

    # 비밀번호 확인 일치 검사
    if(password != confirmPassword):
        return jsonify({'msg':'비밀번호가 일치하지 않습니다!'}), 401
        
        
    # 비밀번호를 해시 함수로 암호화하고 저장
    hashed_password = hash_password(password)
    user = {
        'email': email,
        'password': hashed_password,
        'nickname': nickname,
    }
    
    # 유저를 DB에 저장
    db.users.insert_one(user)

    return jsonify({'msg':'회원가입이 완료되었습니다!'}), 200



        

