# Test_task_for_EmphaSoft

To run this project please follow the steps below:

1.clone this repo

2.create the virtual environment

3.install the required packages in requirements.txt

4.create the database in your PgAdmin and connect it with project

5.makemigrations and migrate

6.**_python manage.py runserver_** and open  http://127.0.0.1:8000/ in your browser and you must see a Swagger doc for the project

7.first you need to register and then verify your email before log in.

8.to get an email with verification code you need to enter your own **_smtp_** credentials in .env file, of course if you have them
if you don't just type in terminal<br> **_python manage.py verify_email your_email@gmail.com_**
and it verifies your email then you can log in and use all features.

