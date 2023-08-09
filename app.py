from flask import Flask, render_template
from login import user_login, user_logout

# Flask 객체 인스턴스 생성
app = Flask(__name__)

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

# 로그아웃 기능
# @app.route('/logout', method = ['POST'])
# def logout():
#     return user_logout()

# 회원가입

# 글 등록 (Create)

# 조회 (Read)

# 수정 (Update)

# 삭제 (Delete)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)