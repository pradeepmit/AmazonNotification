from flask import Flask, render_template, json, request
import signature
from werkzeug.datastructures import ImmutableMultiDict
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ProductNotification'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


AmazonApi = signature.AmazonApi(AccessKey, SecretKey, AssociateTag, Endpoint, "webservices.amazon.in")
#TODO: will pick the credentials from file
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 	print'request==',request.form
 	_name = request.form['inputName']
 	#_category = request.form['catagory']
 
	
    # validate the received values
	if _name:
		productList = AmazonApi.itemSearch(_name,'All')
		return render_template("productList.html",result = productList)
		return json.dumps({'signedurl':url})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/saveEmailNProduct',methods=['POST'])
def saveEmailNProduct():
	print'request==',request.form
	_email = request.form['inputEmail']
	_products = []
	data = dict(request.form)
	if('checkBox' in data.keys()):
		_products = data.get('checkBox');

	cursor.execute("SELECT id FROM EmailAddress where email='%s'"%(_email))
	resp = cursor.fetchall()
	print'resp===',resp
	if(len(resp) == 0):
		insertEmail = cursor.execute("INSERT INTO EmailAddress (email) VALUES ('%s')"%(_email))
		conn.commit();
		cursor.execute("SELECT id FROM EmailAddress where email='%s'"%(_email))
		resp1 = cursor.fetchall()
		setProducts(resp1[0][0],_products)

		
	else:
		setProducts(resp[0][0],_products)
	return 'true'
def setProducts(email,products = []):
	for pr in products:
		query = "INSERT INTO subscription (product,email_d) VALUES ('%s', %d)"%(pr,email)
		recCreated = cursor.execute(query)
		conn.commit()
		print'recCreated==',recCreated
	

	#TO DO Email Scheduler on subscribed products price drop
	
	

    
if __name__ == "__main__":
    app.run(debug=True)