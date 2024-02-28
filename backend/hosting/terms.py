from backend.config import *

terms = Blueprint('terms', __name__)

@terms.route('/terms and policies')
def terms_and_policies():
    return render_template('terms and policies.html', title="Terms and Policies", user=current_user)

@terms.route('/terms and policies/terms and conditions')
def terms_and_conditions():
    return render_template('terms and policies/terms_and_conditions.html', title="Terms and Conditions", user=current_user)

@terms.route('/terms and policies/privacy policy')
def privacy_policy():
    return render_template('terms and policies/privacy_policy.html', title="Privacy Policy", user=current_user)

@terms.route('/terms and policies/terms of use')
def terms_of_use():
    return render_template('terms and policies/terms_of_use.html', title="Terms of Use", user=current_user)

@terms.route('/terms and policies/copyright policy')
def copyright_policy():
    return render_template('terms and policies/copyright_policy.html', title="Copyright Policy", user=current_user)

@terms.route('/terms and policies/safety policy')
def safety_policy():
    return render_template('terms and policies/safety_policy.html', title="Safety Policy", user=current_user)

@terms.route('/terms and policies/cookie policy')
def cookie_policy():
    return render_template('terms and policies/cookie_policy.html', title="Cookie Policy", user=current_user)