from flask import request, jsonify
from hash import hash_password
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.message import EmailMessage
import random
import time
import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
# 환경변수
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')
MAIL_SERVER = os. environ.get('MAIL_SERVER')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


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

    # 이메일 인증 여부 검사
    auth = db.emailAuth.find_one({'email':email}) 
    if(auth['authComplete'] == False):
        return jsonify({'msg':'이메일 인증이 필요합니다!'}), 401
        
    db.emailAuth.delete_many({'email':email})
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


def verify_email():
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
    
    return jsonify({'msg':'이메일 검증 완료.','email':email}), 200
    

def send_email():
    email = request.form['email_give']
    test_email = gmail_sender(MAIL_USERNAME,email,MAIL_PASSWORD)
    
    # 인증번호 난수 생성 
    accessCode = random.randint(111111, 999999)
    content = "플리플리를 방문해주셔서 감사합니다!\n\n" + "인증 번호는 [" + str(accessCode) + "]입니다.\n" + "해당 인증번호를 인증번호 확인란에 기입하여 주세요."
    test_email.msg_set("[플리플리] 이메일 인증번호", content)

    # 인증 메일 전송 
    test_email.smtp_connect_send()

    # 인증 정보가 이미 존재하면 삭제
    db.emailAuth.delete_many({"email": email})
    timestamp = time.time()
    doc = {
        "email" : email,
        "accessCode" : accessCode,
        "authComplete" : False,
        "timestamp": timestamp
    }
    db.emailAuth.insert_one(doc)
    
    return jsonify({'msg':'이메일 인증번호 전송'}), 200


def email_auth():
    email = request.form['email_give']
    access_code = request.form['accessCode_give']

    auth = db.emailAuth.find_one({'email':email})
    if(access_code == str(auth['accessCode'])):
        # 인증번호 만료 시
        if(time.time() - auth['timestamp'] > 180):
            db.emailAuth.delete_one({'email':email})
            return jsonify({'msg':'인증번호가 만료되었습니다.'}), 401
        db.emailAuth.update_one({'email':email},{'$set':{'authComplete':True}})
        return jsonify({'msg':'이메일 인증 성공'}), 200
    else:
        return jsonify({'msg':'인증번호가 일치하지 않습니다.'}), 401
    
        
    

class gmail_sender:
    def __init__(self, sender_email, receiver_email, sender_pasword, cc_email ="", bcc_email=""):
        self.s_email = sender_email
        self.r_email = receiver_email
        self.pw = sender_pasword
        self.server_name = MAIL_SERVER
        self.server_port = 587

        self.msg = EmailMessage()
        self.msg['From'] = self.s_email
        self.msg['To'] = self.r_email
        if cc_email != "":
            self.cc_email = cc_email
            self.msg['Cc'] = self.cc_email
        if bcc_email != '':
            self.bcc_email = bcc_email
            self.msg['Bcc'] = self.bcc_email
        self.smtp = smtplib.SMTP(self.server_name, self.server_port)

    def msg_set(self, msg_title, msg_body):
        self.msg['Subject'] = msg_title
        self.msg.set_content(msg_body)

    def smtp_connect_send(self):
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.s_email, self.pw)
        self.smtp.send_message(self.msg)
        self.smtp.close()
    
        

    