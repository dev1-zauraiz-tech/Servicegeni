# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration (SQLite file db.sqlite3 in project root)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()

# Sample articles data
articles = [
    {
        'id': 1,
        'slug': 'employee-user-management',
        'title': 'Employee & User Management',
        'category': 'Administration',
        'content': '''
        <h2>Managing Users in Your System</h2>
        <p>This guide covers all aspects of user management in your ServiceGeni system.</p>
        
        <h3>Adding New Users</h3>
        <ol>
            <li>Navigate to the Admin panel</li>
            <li>Click on "User Management"</li>
            <li>Click "Add New User"</li>
            <li>Fill in the required information</li>
            <li>Assign appropriate roles and permissions</li>
        </ol>
        
        <h3>User Roles and Permissions</h3>
        <ul>
            <li><strong>Admin:</strong> Full system access</li>
            <li><strong>Manager:</strong> Can view reports and manage staff</li>
            <li><strong>Technician:</strong> Can access work orders and customer data</li>
            <li><strong>Receptionist:</strong> Can manage appointments and basic customer info</li>
        </ul>
        
        <h3>Removing Users</h3>
        <p>To remove a user, go to their profile and click "Deactivate Account". This will prevent them from logging in but preserve their data.</p>
        ''',
        'summary': 'Complete guide to managing users, roles, and permissions in your ServiceGeni system.',
        'author': 'ServiceGeni Support',
        'lastUpdated': 'January 2025'
    },
    {
        'id': 2,
        'slug': 'training-sessions',
        'title': 'Training Sessions',
        'category': 'Training',
        'content': '''
        <h2>Training Sessions and Materials</h2>
        <p>Get your team up to speed with comprehensive training resources.</p>
        
        <h3>Available Training Sessions</h3>
        <ul>
            <li><strong>System Overview:</strong> 2-hour introduction to ServiceGeni</li>
            <li><strong>Advanced Analytics:</strong> 3-hour deep dive into reporting</li>
            <li><strong>Customer Management:</strong> 2-hour CRM training</li>
            <li><strong>Phone System:</strong> 1.5-hour VoIP setup and management</li>
        </ul>
        
        <h3>Scheduling Training</h3>
        <p>Contact your account manager to schedule training sessions for your team.</p>
        
        <h3>Training Materials</h3>
        <p>Access training videos, documentation, and quick reference guides in the Help Center.</p>
        ''',
        'summary': 'Schedule training sessions and access learning materials for your team.',
        'author': 'ServiceGeni Support',
        'lastUpdated': 'January 2025'
    },
    {
        'id': 3,
        'slug': 'phone-redirect-outages',
        'title': 'Phone Call Redirection During Outages',
        'category': 'Phone System',
        'content': '''
        <h2>Maintaining Phone Service During Outages</h2>
        <p>Learn how to redirect calls when your main system is experiencing issues.</p>
        
        <h3>Automatic Failover</h3>
        <p>ServiceGeni includes automatic failover to ensure your phone system remains operational.</p>
        
        <h3>Manual Call Forwarding</h3>
        <ol>
            <li>Log into your ServiceGeni dashboard</li>
            <li>Go to Phone System settings</li>
            <li>Click "Call Forwarding"</li>
            <li>Enter the forwarding number</li>
            <li>Save your settings</li>
        </ol>
        
        <h3>Emergency Contacts</h3>
        <p>Set up emergency contact numbers that will receive calls during system outages.</p>
        ''',
        'summary': 'Step-by-step guide to maintain business continuity during outages.',
        'author': 'ServiceGeni Support',
        'lastUpdated': 'January 2025'
    },
    {
        'id': 4,
        'slug': 'dc-connect-plus',
        'title': 'DC Connect+ Integration',
        'category': 'Integration',
        'content': '''
        <h2>DC Connect+ Features and Setup</h2>
        <p>Everything you need to know about DC Connect+ integration.</p>
        
        <h3>Key Features</h3>
        <ul>
            <li>Advanced call routing</li>
            <li>Automated workflows</li>
            <li>Enhanced analytics</li>
            <li>Custom integrations</li>
        </ul>
        
        <h3>Setup Process</h3>
        <ol>
            <li>Contact your account manager</li>
            <li>Review your current setup</li>
            <li>Configure new features</li>
            <li>Test the integration</li>
            <li>Go live with enhanced features</li>
        </ol>
        ''',
        'summary': 'Everything you need to know about DC Connect+ features and setup.',
        'author': 'ServiceGeni Support',
        'lastUpdated': 'January 2025'
    },
    {
        'id': 5,
        'slug': 'new-customer-onboarding',
        'title': 'New Customer Onboarding',
        'category': 'Getting Started',
        'content': '''
        <h2>Welcome to ServiceGeni!</h2>
        <p>Your complete onboarding timeline and checklist.</p>
        
        <h3>Week 1: Initial Setup</h3>
        <ul>
            <li>Account creation and configuration</li>
            <li>User setup and training</li>
            <li>Phone system integration</li>
            <li>Basic workflow setup</li>
        </ul>
        
        <h3>Week 2: Training and Testing</h3>
        <ul>
            <li>Comprehensive team training</li>
            <li>System testing and validation</li>
            <li>Workflow optimization</li>
            <li>Go-live preparation</li>
        </ul>
        
        <h3>Week 3: Go Live</h3>
        <ul>
            <li>Full system activation</li>
            <li>Live support during transition</li>
            <li>Performance monitoring</li>
            <li>Feedback and adjustments</li>
        </ul>
        ''',
        'summary': 'Complete onboarding process and timeline for new customers.',
        'author': 'ServiceGeni Support',
        'lastUpdated': 'January 2025'
    }
]

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/get-started')
def get_started():
    return render_template('get_started.html')

# Auth routes
@app.route('/sign-up', methods=['POST'])
def sign_up():
    # Accept either combined name or first/last from the Get Started form
    name = request.form.get('name', '').strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    if not name:
        name = (first_name + ' ' + last_name).strip()

    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm_password', '')

    if not name or not email or not password:
        flash('Please fill all required fields', 'error')
        return redirect(url_for('get_started'))
    if password != confirm:
        flash('Passwords do not match', 'error')
        return redirect(url_for('get_started'))
    if User.query.filter_by(email=email).first():
        flash('Email already registered. Please login.', 'error')
        return redirect(url_for('sign_in'))

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    session['user_name'] = user.name
    flash('Welcome to ServiceGeni!', 'success')
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Logged in successfully', 'success')
            return redirect(url_for('homepage'))
        flash('Invalid email or password', 'error')
        return redirect(url_for('sign_in'))
    return render_template('sign_in.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('homepage'))

@app.route('/knowledge-base')
def knowledge_base():
    # Convert list to dictionary for template compatibility
    kb_articles = {article['slug']: article for article in articles}
    return render_template('knowledge_base.html', articles=kb_articles)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = next((a for a in articles if a['slug'] == article_id), None)
    if not article:
        flash('Article not found', 'error')
        return redirect(url_for('knowledge_base'))
    return render_template('article_detail.html', article=article, article_id=article_id)

@app.route('/api/article-feedback/<int:article_id>', methods=['POST'])
def article_feedback(article_id):
    data = request.get_json()
    feedback = data.get('feedback', '')
    # Here you would typically save the feedback to a database
    return jsonify({'success': True, 'message': 'Feedback received'})

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search_results.html', query='', results=[])

    results = []
    for a in articles:
        if query.lower() in a['title'].lower() or query.lower() in a['content'].lower():
            results.append({
                'id': a['slug'],
                'title': a['title'],
                'category': a['category'],
                'snippet': a['content'][:160] + '...'
            })
    return render_template('search_results.html', query=query, results=results)

@app.route('/submit-ticket', methods=['GET', 'POST'])
def submit_ticket():
    if request.method == 'POST':
        subject = request.form.get('subject', '')
        description = request.form.get('description', '')
        email = request.form.get('email', '')
        ticket_id = int(datetime.now().timestamp())
        return render_template('ticket_success.html', ticket_id=ticket_id, subject=subject, email=email)
    return render_template('submit_ticket.html')

# Marketing pages based on screenshots
@app.route('/product')
def product():
    return render_template('marketing_product.html')

@app.route('/pricing')
def pricing():
    return render_template('marketing_pricing.html')

@app.route('/contact')
def contact():
    return render_template('marketing_contact.html')

@app.route('/support')
def support():
    return render_template('marketing_support.html')

@app.route('/blog')
def blog():
    posts = [
        {
            'date': '1/6/25',
            'title': 'ServiceGeni and Digital Concierge are joining forces!',
            'slug': 'servicegeni-dc-joining-forces'
        },
        {
            'date': '7/2/24',
            'title': '4.1 Voyager\'s Venture Release Notes',
            'slug': 'voyagers-venture-4-1-release-notes'
        }
    ]
    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
