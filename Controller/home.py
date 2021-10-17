from flask import Blueprint
from flask import Flask, render_template, url_for, request
from flask_login import login_required, logout_user
from werkzeug.utils import redirect
home_route = Blueprint('home_route', __name__)


data = {
    "wishlist": ["Microsoft", "Google", "Uber"],
    "inprogress": ["Twitter", "Pearson"],
    "applied": ["Amazon", "NetApp"],
    "offers": ["Perfios"]
}

upcoming_events = [
    {"duedate": "28th Sept, 2021",
     "company": "Apple"
     },
    {"duedate": "19th Dec, 2021",
     "company": "Microsoft"
     },
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     },
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     },
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     }
]

profile = {
    "name": "Jessica Holds",
    "Location": "Raleigh, NC",
    "phone_number": "",
    "social": {
            "linkedin": "www.linkedin.com/in/surajdm",

    }
}


@home_route.route('', methods=['GET'])
@login_required
def home():
    return render_template('home.html', data=data, upcoming_events=upcoming_events)


@home_route.route('/view', methods=['GET'])
@login_required
def view():
    card_selected = request.args.get('user')
    return render_template('view_list.html', data=data, upcoming_events=upcoming_events)

@home_route.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("/login")

@home_route.route('/add_New',methods=['GET'])
@login_required
def add_New():
    print("Adding New...")
    return render_template('home.html', data=data, upcoming_events=upcoming_events)