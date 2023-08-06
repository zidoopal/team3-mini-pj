# 🚢 항해 16기 3조 미니 프로젝트

## 01. 파이썬 버전 확인

- 터미널에서 python --version
  - 유진 (Python 3.8.6)

## 02. 터미널에서 파일 경로 마지막 부분 team3-mini-pj(미정) 확인 후 가상환경 설정

- 윈도우 : python -m venv venv
- 맥 : python3 -m venv venv

## 03. 가상환경 venv 활성화하기

- 터미널 환경에서 경로의 마지막 부분이 team3-mini-pj(미정) 확인 후,<br>
  우측 하단 파이썬 버전 클릭 > venv로 골라주기 > 새 터미널 열어서 (venv) 뜨는지 확인하기

## 04. 패키지 설치하기

- 필수설치

  - pip install flask (파이썬 프레임워크)
  - pip install dnspython (도메인을 받아 뭔가를 송수신할 때 사용, pymongo 패키지가 동작하려면 필요한 패키지)
  - pip install pymongo (MongoDB를 python으로 사용하기 위해 쓰이는 라이브러리)
  - pip install requests (Python에서 HTTP 요청을 보내는 모듈, js에서 fetch 역할)

## 05. pymongo로 DB 조작하기

- 저장 - 예시

  - doc = {'name':'bobby','age':21}<br>
    db.users.insert_one(doc)

- 한 개 찾기 - 예시

  - user = db.users.find_one({'name':'bobby'})

- 여러개 찾기 - 예시 ( \_id 값은 제외하고 출력)

  - all_users = list(db.users.find({},{'\_id':False}))

- 바꾸기 - 예시

  - db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

- 지우기 - 예시
  - db.users.delete_one({'name':'bobby'})
