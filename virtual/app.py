from flask import Flask, render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hostelpayment:abc123@localhost:3306/hostel-payment'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address_line1 = db.Column(db.String(120), unique=True, nullable=False)
    address_line2 = db.Column(db.String(120), unique=True, nullable=False)
    address_line3 = db.Column(db.String(120), unique=True, nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    knockoff = db.Column (db.Float, nullable=False)
    user = db.relationship('User', backref='bookings')  # Relationship to User

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='invoices')  # Relationship to User
    booking = db.relationship('Booking', backref='invoices')  # Relationship to Booking

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    amount_to_pay = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return render_template('login.html')

@app.route('/invoice/<int:id>')
def invoice(id):
    user = User.query.get(id)  # Retrieve user by ID
    return render_template('invoice.html',user=user)

@app.route('/success')
def success():
    return render_template('success.html')
'''
@app.route("/payment")
def payment():
    return render_template('payment.html')
'''
@app.route('/payment', methods=['GET','POST']) 
def payment():
   
    if request.method == 'POST':
        # Retrieve the input from the form
        amount_to_pay = request.form.get('payment_amount')  # Get the input

        # Check if the input is None or empty
        if amount_to_pay is None or amount_to_pay.strip() == '':
            print("No input received")  # Handle case where no input was provided
            return redirect('/payment')  # Redirect back to payment form

        try:
            user_input = int(amount_to_pay)  # Convert to int
            new_payment = Payment(amount_to_pay=user_input)  # Create a new payment record
            db.session.add(new_payment)  # Add to session
            db.session.commit()  # Commit to save
            return redirect(url_for('success'))  # Redirect to success page
        except ValueError:
            print("Not a valid input")  # Handle invalid input
            return redirect('/payment')  # Redirect back to payment form

    return render_template('payment.html')  # Render the form for GET requests

if __name__ == '__main__':
    app.run(debug=True)