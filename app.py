from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient

# Flask 객체 인스턴스 생성
app = Flask(__name__)

# 메인 페이지


@app.route('/')
def index():
    return render_template('login.html')


# 회원가입

# 글 등록 (Create)

# 조회 (Read)

# 수정 (Update)

# 삭제 (Delete)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    # app.run()
