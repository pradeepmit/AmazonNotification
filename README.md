# AmazonNotification
Fetch Product from amazon and show the current price and set mail notification if required
To run the project we need to install flask and python 2.7 & required credentials from amazon associate account.
like AccessKey, SecretKey, AssociateTag

after installing the flask go to the folde and run the file app.py as "python app.py" server will run on http://127.0.0.1:5000/

Installation:

Ubuntu/linux
1. pip install flask
2. pip install flask-mysql
3. Install the My SQL Server also


Database setup:

#this Step can be automate
Login to mysql;
Choose database;
create tables:
CREATE TABLE EmailAddress (id INT NOT NULL AUTO_INCREMENT, email VARCHAR(45) NULL,  UNIQUE INDEX email_UNIQUE (email ASC), PRIMARY KEY (id));
CREATE TABLE subscription (id INT NOT NULL AUTO_INCREMENT,email_d INT NULL,product VARCHAR(45) NULL, PRIMARY KEY (id), INDEX fk_email_addres_email_idx (email_d ASC),  CONSTRAINT fk_email_addres_email FOREIGN KEY (email_d) REFERENCES EmailAddress (id) ON DELETE CASCADE  ON UPDATE CASCADE);


Thanks!