import bcrypt

def hash_passwd(plain_passwd: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_passwd.encode('utf-8'), salt).decode('utf-8')

def check_passwd(plain_passwd: str, hashed_passwd: str) -> bool:
    return bcrypt.checkpw(
        plain_passwd.encode('utf-8'),
        hashed_passwd.encode('utf-8')
    )