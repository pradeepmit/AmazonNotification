from flask import Flask, render_template, json, request
import signature
from flask.ext.mysql import MySQL
app = Flask(__name__)
# mysql = MySQL()
 
# # MySQL configurations


AmazonApi = signature.AmazonApi(AccessKey, SecretKey, AssociateTag, "webservices.amazon.in")
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
 
	url = AmazonApi.itemLookup(_name,'All')
	#url is the required signed url which will used to get the searched product from amazon
	print'azlookup=',url
	#return json.dumps({'html':url})
    # validate the received values
	if _name:
		return json.dumps({'signedurl':url})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
    
if __name__ == "__main__":
    app.run(debug=True)