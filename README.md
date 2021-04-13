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
   
   - You must create the first administrator user yourself.
   - Start flask shell from terminal:
   - ```sh
     from models import User
     ```
   - ```sh
      u = User(firstname='<UserFirstname>', lastname='<UserLastname>', login='<UserLogin>', role='admin', email='<UserEmail@example.com>')
      ```
   - Minimum number of characters for login = 6  
   - ```sh
      u.set_password('<UserPassword>')
      ```
   - Minimum number of characters for password = 8
   - ```sh   
      u.save()
   
6. Run the server
      ```sh
    app.py
      ```

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

