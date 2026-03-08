1. Clone the Repository
git clone https://github.com/nayanpatel-byte/BotForge.git
cd BotForge

2. Install Python Dependencies
Make sure Python 3 is installed, then install the required packages:
pip install flask flask-mysqldb mysql-connector-python

3. Setup MySQL Database
Start MySQL and create the database:
CREATE DATABASE botforge;
Import the schema:
mysql -u root -p botforge < schema.sql
Update the database credentials in the backend configuration file if required.

4. Run
Navigate to the backend directory and start the Flask server:
cd backend
python app.py
The server will start at:
http://localhost:5000
