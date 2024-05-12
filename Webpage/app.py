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
        user = auth.get_user_by_email(email)
        user_ref = db.collection('users').document(user.uid)
        user_data = user_ref.get().to_dict()
        
        if user_data and user_data.get('password') == password:
            
            role = user_data.get('role')
            if role == 'investor':
                
                return jsonify({'success': True, 'redirect_url': '/investor/{}'.format(user.uid)})
            elif role == 'startup':
               
                return jsonify({'success': True, 'redirect_url': '/project/{}'.format(user.uid)})
            else:
                return jsonify({'success': False, 'error': 'Invalid role'})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    except auth.AuthError as e:
        print("Firebase Authentication Error:", e)
        return jsonify({'success': False, 'error': 'Authentication failed'})
    
    except Exception as e:
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
            user = auth.create_user(
                email=email,
                password=password
            )

            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'email': email,
                'password': password
            })
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
            user_ref = db.collection('users').document(user_id)
            user_ref.update({
                'role': role
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
            'validupto':validUpto,
            'startup_address':startup_address,
            'total_amount_invested':0
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False})
# Investor page
@app.route("/investor/<string:user_id>")
def investor(user_id):
    return render_template('investor_home.html',user_id=user_id)

# Investment details page
@app.route("/investor/project_showcase/<string:user_id>")
def project_showcase(user_id):
    return render_template('project_showcase.html',user_id=user_id)

@app.route('/retrieve_project_data_for_investor/<string:user_id>')
def retrieve_project_data_for_investor(user_id):
    projects = []

    try:
        startup_users_ref = db.collection('users').where('role', '==', 'startup')
        startup_users = startup_users_ref.stream()
        for startup_user in startup_users:
            user_data = startup_user.to_dict()
            project_name = user_data.get('projectName')
            expected_fund = user_data.get('expectedFund')
            total_amount_invested =  user_data.get('total_amount_invested')
            projects.append({
                "name": project_name,
                "total_amount_invested": total_amount_invested,  
                "ratings": 4.5,  
                "targeted_fund": expected_fund,
                "invest_link": f"/portfolio_call/{startup_user.id}/{user_id}"
            })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    return jsonify(projects)

# Watchlist page
@app.route("/investor/watchlist/<string:user_id>")
def watchlist(user_id):
    return render_template('watchlist.html',user_id=user_id)

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
@app.route("/project/<string:user_id>")
def project(user_id):
    return render_template('project_home.html',project_id = user_id,user_id = "null")
    
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


@app.route('/retrive_profile_data/<string:user_id>',methods=['GET','POST'])
def retrive_profile_data(user_id):
    try:
        user_ref = db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()
        if user_data.get("role", "") == "investor":
            profile_data = {
                "name": user_data.get("investor_name", ""),
                "email": user_data.get("email", ""),
                "account_type": user_data.get("role", "")
            }
        elif user_data.get("role", "") == "startup":
            profile_data = {
                "name": user_data.get("name", ""),
                "email": user_data.get("email", ""),
                "account_type": user_data.get("role", "")
            }

        return jsonify(profile_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Profile page
@app.route("/profile_call/<string:user_id>")
def profile_call(user_id):
    return render_template('profile.html',user_id = user_id)

# portfolio call
@app.route('/portfolio_call/<string:user_id>/<string:project_id>')
def portfolio_call(user_id,project_id):
    return render_template("portfolio.html",user_id = user_id,project_id = project_id)

@app.route('/retrieve_project_data/<string:user_id>/<string:project_id>')
def retrieve_project_data(user_id,project_id):
    try:
        if project_id == "null":
            role = "startup"
        else:
            role = "investor"
        user_ref = db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()
        project_data = {
            "name": user_data.get('projectName'),
            "total_fund": user_data.get('expectedFund'),
            "total_amount_invested": user_data.get('total_amount_invested'),
            "expiring_date": user_data.get('validupto'),
            "category": user_data.get('category'),
            "youtube_link": user_data.get('demolink'),
            "abstract": user_data.get('abstract'),
            "impact": user_data.get('impact'),
            "state": user_data.get('state'),
            "city": user_data.get('city'),
            "email": user_data.get('email'),
            "user_id": role,
            "project_id":project_id,
            "startup_address":user_data.get('startup_address')
        }

        return jsonify(project_data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/investor_name_get/<string:project_id>')
def investor_name_get(project_id):
    user_ref = db.collection('users').document(project_id)
    user_data = user_ref.get().to_dict()
    investor_name = {
        "name": user_data.get('investor_name'),
    }

    return jsonify(investor_name)

@app.route('/update_fund_records/<string:user_id>',methods=["GET","POST"])
def update_fund_records(user_id):
    try:
        data = request.get_json()
        amount_invested = data.get("total_amount_invested")
        user_ref = db.collection('users').document(user_id)
        user_data = user_ref.get().to_dict()
        current_amount = user_data.get("total_amount_invested", 0)
        amount_invested = int(amount_invested) + current_amount
        user_ref.update({
            'total_amount_invested': amount_invested
        })
        print("passed...")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

