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
client = MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.ebm0gtg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.miniproject

def user_signup():
    email = request.form['email_give'].strip()
    password = request.form['password_give'].strip()
    confirmPassword = request.form['confirmPassword_give'].strip()
    nickname = request.form['nickname_give'].strip()

    ## 로그인 검증
    # 이메일 입력 검사
    if(email == ''):
        return jsonify({'msg':'이메일을 입력해주세요!'}), 401

    # 이메일 유효성 검사
    try :
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'msg':'유효하지 않은 이메일 입니다!'}), 401
    
    # 중복 이메일 검사
    findUser = db.users.find_one({'email': email} ,{'_id':False})
    if(findUser):
        return jsonify({'msg':'이미 등록된 이메일 입니다!'}), 401
    
    # 비밀번호 입력 검사
    if(password == ''):
        return jsonify({'msg':'비밀번호를 입력해주세요!'}), 401

    # 비밀번호 길이 검사
    if len(password) < 5 or len(password) > 20:
        return jsonify({'msg':'비밀번호는 5자리 이상 20자리 이하로 해주세요!'}), 401

    # 비밀번호 확인 일치 검사
    if(password != confirmPassword):
        return jsonify({'msg':'비밀번호가 일치하지 않습니다!'}), 401
    
    # 닉네임 입력 검사
    if(nickname == ''):
        return jsonify({'msg':'닉네임을 입력해주세요!'}), 401
    
    # 닉네임 길이 검사
    if len(password) > 20:
        return jsonify({'msg':'닉네임은 20자리 이하로 해주세요!'}), 401
    
    # 중복 닉네임 검사
    findUser = db.users.find_one({'nickname': nickname} ,{'_id':False})
    if(findUser):
        return jsonify({'msg':'이미 등록된 닉네임 입니다!'}), 401
        
        
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


def verification_email():
    email = request.form['email_give'].strip()

    # 이메일 입력 검사
    if(email == ''):
        return jsonify({'msg':'이메일을 입력해주세요!'}), 401

    # 이메일 유효성 검사
    try :
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'msg':'유효하지 않은 이메일 입니다!'}), 401
    
    # 중복 이메일 검사
    findUser = db.users.find_one({'email': email} ,{'_id':False})
    if(findUser):
        return jsonify({'msg':'이미 등록된 이메일 입니다!'}), 401
    
    # TODO 이메일 인증번호 전송 로직
    emailCertificationNumber = ''

    return jsonify({'msg':'이메일 인증번호 전송'}), 200

    
