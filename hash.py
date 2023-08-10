import hashlib

# 비밀번호 해시 함수
def hash_password(password):
    # SHA-256 해시 함수를 사용하여 비밀번호를 암호화
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password