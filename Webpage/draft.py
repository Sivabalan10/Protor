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
    return render_template("enter_investor.html")

# storing investor detail
@app.route("/store_investor",methods=["GET", "POST"])
def store_investor():
    data = request.json  # Get JSON data from request
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
    investor_data = True
    if investor_data:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# Enter Project page
@app.route("/role_choosing/enter_project_details/<string:user_id>")
def enter_project_details(user_id):
    return render_template('enter_startup.html')

# storing project details
@app.route('/store_project', methods=['POST'])
def store_startup():
    data = request.json
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
    project_detail_stored = True
    if project_detail_stored:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
# Investor page
@app.route("/investor")
def investor():
    return render_template('investor_home.html')

# Investment details page
@app.route("/investor/project_showcase")
def project_showcase():
    return render_template('project_showcase.html')

@app.route('/retrieve_project_data_for_investor')
def retrieve_project_data_for_investor():
    projects = [
    {
        "name": "Animal_detection",
        "holders": 100,
        "ratings": 4.5,
        "targeted_fund": "$50,000",
        "invest_link": "/portfolio_call"
    },
    {
        "name": "PCB_Board_Detection",
        "holders": 75,
        "ratings": 4.2,
        "targeted_fund": "$30,000",
        "invest_link": "/portfolio_call"
    },
    {
        "name": "Social impact",
        "holders": 120,
        "ratings": 4.8,
        "targeted_fund": "$80,000",
        "invest_link": "/portfolio_call"
    }
    ]
    return jsonify(projects)

# Watchlist page
@app.route("/investor/watchlist")
def watchlist():
    return render_template('watchlist.html')

@app.route('/retrieve_watchlist')
def retrieve_watchlist():
    projects = [
    {
        "name": "Animal_detection",
        "holders": 100,
        "ratings": 4.5,
        "targeted_fund": "$50,000",
        "invest_link": "/portfolio_call"
    },
    {
        "name": "PCB_Board_Detection",
        "holders": 75,
        "ratings": 4.2,
        "targeted_fund": "$30,000",
        "invest_link": "/portfolio_call"
    },
    {
        "name": "Social impact",
        "holders": 120,
        "ratings": 4.8,
        "targeted_fund": "$80,000",
        "invest_link": "/portfolio_call"
    }
    ]
    return jsonify(projects)

#investment details
@app.route("/investor/investment_details")
def investment_details():
    return render_template('investment_details.html')

@app.route('/investor/investment_records')
def get_investment_records():
    investment_records = [
    {"name": "Stock A", "value": 100, "quantity": 10, "total_amount": 1000},
    {"name": "Stock B", "value": 150, "quantity": 8, "total_amount": 1200},
    {"name": "Stock C", "value": 80, "quantity": 15, "total_amount": 1200}
    ]
    return jsonify(investment_records)

@app.route('/investor/transaction_details')
def get_transaction_details():
    transaction_details = [
        {"date": "2024-05-01", "amount": 200, "stock_name": "Stock A"},
        {"date": "2024-05-02", "amount": 300, "stock_name": "Stock B"},
        {"date": "2024-05-03", "amount": 150, "stock_name": "Stock C"}
    ]
    return jsonify(transaction_details)

#terms and conditions
@app.route('/termsandconditionsforstartup')
def termsandconditionsforstartup():
    return render_template('startup_tandc.html')

@app.route('/termsandconditionsforinvestor')
def termsandconditionsforinvestor():
    return render_template('investor_tandc.html')

# Project page
@app.route("/project")
def project():
    return render_template('project_home.html')
    
# Project analysis page
@app.route("/project/allotment_status")
def allotment_status():
    return render_template('allotment_status.html')

@app.route('/retrieve_ipo_allotment_data')
def retrieve_ipo_allotment_data():
    ipo_allotment_data = {
    "company_name": "Azure Company",
    "pan": "ABCDE1234F",
    "application_number": "APP123456789",
    "name_applied": "John Doe",
    "shares_applied": 100,
    "shares_alloted": 50,
    "status": "Allotment Completed"
    }   
    return jsonify(ipo_allotment_data)
# Sebi application page
@ app.route("/project/sebi_apply")
def sebi_apply():
    return render_template('sebi_apply.html')

# profile call
@app.route('/profile_call')
def profile_call():
    role = "project"
    name = "Sivabalan"
    return redirect(url_for('view_profile',roles = role,names = name))

@app.route('/retrive_profile_data')
def retrieve_profile_data():
    profile_data = {
    "name": "Sivabalan",
    "email": "sparkysiva10@gmail.com",
    "account_type": "Investor"
    }
    return jsonify(profile_data)

# Profile page
@app.route("/<roles>/view_profile/<names>")
def view_profile(roles,names):
    print(roles,names)
    return render_template('profile.html')

# portfolio call
@app.route('/portfolio_call')
def portfolio_call():
    role2 = "investor"
    return redirect(url_for('view_project_portfolio',roles2 = role2))

# Portfolio page
@app.route("/<roles2>/view_project_portfolio")
def view_project_portfolio(roles2):
    return render_template('portfolio.html')

@app.route('/retrieve_project_data')
def retrieve_project_data():
    project_data = {
    "name": "Animal Detection Project",
    "total_fund": 50000,
    "share_price": 400,
    "shareholders": 100,
    "expiring_date": "2024-12-31",
    "category": "Technology",
    "youtube_link": "https://www.youtube.com/embed/kxUfXvpMSMs?si=YhIYaowBeRD9uxq0",
    "abstract": "This is a animal detection project abstract.",
    "impact": "This project will have a significant impact.",
    "state": "Tamilnadu",
    "city": "Chennai",
    "email": "sparkysiva10@gmail.com"
    }
    return jsonify(project_data)

if __name__ == "__main__":
    app.run(debug=True)

