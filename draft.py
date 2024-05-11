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


if __name__ == "__main__":
    app.run(debug=True)

