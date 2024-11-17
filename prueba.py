import bcrypt

hashed_password = bcrypt.hashpw("beton2".encode(), bcrypt.gensalt()).decode('utf-8')
print(hashed_password)
