from pymongo import MongoClient
import certifi
import os

# 환경변수 설정
from dotenv import load_dotenv
load_dotenv('.env')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

# 몽고DB 연결
ca = certifi.where()
client = MongoClient(f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.ebm0gtg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.miniproject

def get_post_detail(post_id):
    post = db.posts.find_one({"postId": post_id}, {"_id": 0})
    if post:
        return post
    else:
        return None

def add_comment_to_db(post_id, comment):
    if not comment:
        return None
    
    comment_data = {
        "postId": post_id,
        "content": comment,
        # "userName": "홍종훈",
        # "userProfileImage": ""
    }

    # 댓글 저장
    result = db.comments.insert_one(comment_data)
    if result.inserted_id:
        return True
    else:
        return False

def fetch_comments_from_db(post_id):
    comments = db.comments.find({"postId": post_id})
    comment_list = []
    for comment in comments:
        comment_list.append({
            "userName": comment.get("userName", "Anonymous"),
            "userProfileImage": comment.get("userProfileImage", "default.png"),
            "content": comment["content"]
        })
    return comment_list
