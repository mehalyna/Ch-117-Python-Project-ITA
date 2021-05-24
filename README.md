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
   - Set up MongoDB Compass
      - Meke connection mongodb://<your_url>:<your_port>
      - Create database <your_db_name>
   - Create file `.env` in root folder of the project with fields:
   ```text
      FLASK_SECRET_KEY=<your_secret_key>
      DJANGO_SECRET_KEY=<your_secret_key>
      DB_NAME=<your_db_name>
      MONGO_URL=<your_url>
      PORT=<your_port>
   ```

### Our project include two servers:
   - admin
   - user
  

#### To run admin server:
 1. Create the first administrator user to login in admin.
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
      ```
      
Following commands should be run in the 'admin' directory of the projectad

2. Run the server <br/>
    ```sh
    theproject\admin>app.py
    ```
3. Run the tests <br/>
   ```sh
   theproject\admin>pytest -v
   ```
4. To see test coverage <br/>
   ```sh
   theproject\admin>coverage run -m --omit='*/venv/*' pytest -v
   theproject\admin>coverage report
   ```
   

#### To run user server:
Following commands should be run in the 'library' directory of the project
1. Run the server <br/>
   
   ```sh
    theproject\library>python manage.py runserver
   ```
2. Run the tests <br/>
   ```sh
    theproject\library>python manage.py test -v 2
   ```
3. To see test coverage <br/>
   ```sh
   theproject\library>coverage run --omit='*/venv/*' manage.py test -v 2
   theproject\library>coverage report
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

