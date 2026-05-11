import bcrypt
pw = b'admin'
s = bcrypt.gensalt()
h = bcrypt.hashpw(pw, s) # Hash password
print(h)
# entered_pw = b'GeekPassword'

# if bcrypt.checkpw(entered_pw, h):
#     print("Password match!")
# else:
#     print("Incorrect password.")