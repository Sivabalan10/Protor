from flask import Flask,redirect,render_template,request,url_for,jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore

app = Flask(__name__)

cred = credentials.Certificate('C:/Users/SIVA/Social-impact-project/Webpage/social-impact-84cf7-firebase-adminsdk-xrgob-1f4ce47849.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# WEB PAGE ROUTES

# Login page
@app.route("/")
def homepage():
    return render_template('login.html')
    
# Login call
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    try:
        # Authenticate user with Firebase Authentication
        user = auth.get_user_by_email(email)
        
        # Verify user's credentials in Firestore
        user_ref = db.collection('users').document(user.uid)
        user_data = user_ref.get().to_dict()
        
        if user_data and user_data.get('password') == password:
            # Password matches, proceed
            return jsonify({'success': True})
        else:
            # Password does not match or user data not found
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    except auth.AuthError as e:
        # Handle Firebase Authentication errors
        print("Firebase Authentication Error:", e)
        return jsonify({'success': False, 'error': 'Authentication failed'})
    
    except Exception as e:
        # Handle other exceptions
        print("Error:", e)
        return jsonify({'success': False, 'error': 'An error occurred'})

# Logout call
@app.route("/logout")
def logout():
    return redirect('/')

# Sign_up page
@app.route("/sign_up")
def sign_up():
    return render_template('sign_up.html')

@app.route("/sign_up/account_added", methods=["GET", "POST"])
def account_added():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password
            )

            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'email': email,
                'password': password
                # Add more user data as needed
            })

            # Return user ID as JSON response
            return jsonify({"success": True, "user_id": user.uid})
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    return render_template('sign_up.html')
# Choosing role
@app.route("/role_choosing/<string:user_id>", methods=["GET", "POST"])
def role_choosing(user_id):
    if request.method == "POST":
        data = request.get_json()
        role = data.get("role")
        try:
            # Update user document in Firestore with role information
            user_ref = db.collection('users').document(user_id)
            user_ref.update({
                'role': role
                # Add more user data as needed
            })
            return jsonify({"success": True, "user_id": user_id, "role": role})
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    return render_template('role_choosing.html',user_id =  user_id)

# Enter Investor details
@app.route("/role_choosing/enter_investor_details/<string:user_id>")
def enter_investor_details(user_id):
    return render_template("enter_investor.html",user_id = user_id)

# storing investor detail
@app.route("/store_investor",methods=["GET", "POST"])
def store_investor():
    data = request.json  # Get JSON data from request
    user_id = data.get('user_id')
    username = data.get('username')
    project_interest = data.get('projectInterest')
    description = data.get('description')
    investor_industry = data.get('investorIndustry')
    sector = data.get('sector')
    state = data.get('state')
    country = data.get('country')
    mobile_number = data.get('mobileNumber')
    linked_url = data.get('linkedUrl')
    email = data.get('email')
    print(username)
    try:
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'investor_name': username,
            'project_interest': project_interest,
            'description': description,
            'investor_industry': investor_industry,
            'sector': sector,
            'state': state,
            'country':country,
            'mobile_number':mobile_number,
            'linked_url':linked_url,
            'email' : email
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False})

# Enter Project page
@app.route("/role_choosing/enter_project_details/<string:user_id>")
def enter_project_details(user_id):
    return render_template('enter_startup.html',user_id = user_id)

# storing project details
@app.route('/store_project', methods=['GET','POST'])
def store_startup():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    projectName = data.get('projectName')
    email = data.get('email')
    whichtype = data.get('type')
    state = data.get('state')
    city = data.get('city')
    abstract = data.get('abstract')
    category = data.get('category')
    demoLink = data.get('demoLink')
    linkedinUrl = data.get('linkedinUrl')
    impact = data.get('impact')
    service = data.get('service')
    expectedFund = data.get('expectedFund')
    expectedShareValue = data.get('expectedShareValue')
    validUpto = data.get('validUpto')
    startup_address = data.get('startup_address')
    print(startup_address)
    try:
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'name': name,
            'projectName': projectName,
            'email': email,
            'type': whichtype,
            'state': state,
            'city': city,
            'abstract':abstract,
            'category':category,
            'demolink':demoLink,
            'linkedin' : linkedinUrl,
            'impact':impact,
            'service':service,
            'expectedFund':expectedFund,
            'expectedsharevalue':expectedShareValue,
            'validupto':validUpto,
            'startup_address':startup_address,
            'shares_sold':0
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True)

