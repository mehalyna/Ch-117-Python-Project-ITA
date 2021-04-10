# Ch-117-Python-Project-ITA
Python Project of Ch-117 mixed group ITA

### Installation for Windows

1. Install python 3.8 at the [link](https://www.python.org/downloads/windows/)
2. Install MongoDB at the [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
3. Clone the repository
   ```sh
   git clone https://github.com/mehalyna/Ch-117-Python-Project-ITA.git
   ```
4. Install python packages from requirements.txt
   ```sh
   pip install -r requirements.txt
   ```
5. Initialize database
   - Install MongoDB Compass
   - Connect to local db
   ```python
   from mongoengine import connect
   connect(
       db=DB_NAME,
       host=MONGO_URL,
       port=PORT
    )
   ```
   - In mongoDB compass connect to localhost mongodb://127.0.0.1:27017
   - Create database "name DB" and create collection 'user'
   - In collection push "ADD DATA" and select 'Insert Document'
   - Input {"_id":{"$oid":"60636f34bb19534f686cfe0f"},"firstname":"admin","lastname":"admin","email":"thusday13081@gmail.com","login":"user123","password_hash":"pbkdf2:sha256:150000$De6yt2gS$8cea55706d35565cd9d9617c6718627892b9457dbe514ffe305d86b4629104a5","role":"admin","status":"active","last_login":{"$date":"2021-03-30T21:06:27.163Z"},"reviews":[],"recommended_books":[],"wishlist":[],"preference":{"genres":[],"authors":[],"rating":2.5,"years":[]}}
   - Save
6. Run the server
   ```sh
   app.py
   ```
   - your login admin123
   - your password 12345678

## For contributors
### Project setup
Start with our wiki
### Git Flow
We are using simpliest github flow to organize our work:
![Git Flow Ilustration](https://github.com/mehalyna/Share-images/blob/main/68747470733a2f2f7363696c6966656c61622e6769746875622e696f2f736f6674776172652d646576656c6f706d656e742f696d672f6769746875622d666c6f772e706e67.png)

### Note! Contribution rules:
1. All Pull Requests should start from prefix #xxx-yyy where xxx - task number and and yyy - short description e.g. #020-CreateAdminPanel
2. Pull request should not contain any files that is not required by task.

In case of any violations, pull request will be rejected.

