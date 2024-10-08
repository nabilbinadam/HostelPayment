from flask import Flask, render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    project_name=db.Column(db.String(30), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    room=db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rate=db.Column(db.Float, nullable=False)
    units=db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
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
    total_amount = db.Column(db.Float, nullable=False)
    amount_to_pay = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return render_template('login.html')

@app.route('/invoice/<int:booking_id>')
def invoice(booking_id): 
    booking_id = request.args.get('booking_id', type=int)  # Get booking_id from query parameters
    project_name = request.args.get('project_name', type=str)  # Get booking_id from query parameters
    date = request.args.get('date', type=int)  # Get booking_id from query parameters
    room = request.args.get('room', type=str) 
    units = request.args.get('units', type=int) 
    rate = request.args.get('rate', type=float) 
    total_cost = request.args.get('total_cost', type=float)
    user_id = request.args.get('user_id', type=int)
    user = User.query.get(user_id)  # Retrieve user by ID
    booking = Booking.query.get(booking_id)  # Retrieve booking by ID
    project_name = Booking.query.get(project_name)
    date = Booking.query.get(date)
    room = Booking.query.get(room) 
    units = Booking.query.get(units) 
    rate = Booking.query.get(rate) 
    total_cost = Booking.query.get(total_cost) 


    return render_template('invoice.html', user=user, booking=booking,)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/payment/<int:invoice_id>', methods=['GET', 'POST'])
def payment(invoice_id):
    # Retrieve the invoice using the provided invoice_id
    invoice = Invoice.query.get(invoice_id)
    booking = Booking.query.get(invoice_id)

    if not invoice:
        return "Invoice not found", 404

    if request.method == 'POST':
        amount_to_pay = request.form.get('payment_amount')

        if not amount_to_pay:
            print("No input received")
            return redirect(url_for('payment', invoice_id=invoice_id))

        try:
            user_input = float(amount_to_pay)
            new_payment = Payment(
                amount_to_pay=user_input,
                id=invoice.id,
                total_amount=invoice.total_amount,  
                date =invoice.invoice_date
            )
            db.session.add(new_payment)
            db.session.commit()
            
            return redirect(url_for('success'))
        
        except ValueError:
            print("Not a valid input")
            return redirect(url_for('payment', invoice_id=invoice_id))

    return render_template('payment.html', invoice=invoice, booking=booking ) # Pass the invoice to the template



"""
@app.route('/payment/<int:invoice_id>', methods=['POST']) 
def payment(invoice_id):
   invoice_id = request.args.get('invoice_id', type=int)
   project_name = request.args.get('project_name', type=str)
   invoice_date = request.args.get('invoice_date', type=int)
   total_amount = request.args.get('total_amount', type=int)
   invoice = Invoice.query.get(invoice_id)
   project_name = Invoice.query.get(project_name)
   invoice_date = Invoice.query.get(invoice_date)
   total_amount = Invoice.query.get(total_amount)    
   if request.method == 'POST':
    



        # Retrieve the input from the form
        amount_to_pay = request.form.get('payment_amount')  # Get the input

        # Check if the input is None or empty
        #if amount_to_pay is None or amount_to_pay.strip() == '':
           # print("No input received")  # Handle case where no input was provided
           # return redirect('/payment')  # Redirect back to payment form

        try:
            user_input = int(amount_to_pay)  # Convert to int
            new_payment = Payment(amount_to_pay=user_input)  # Create a new payment record
            db.session.add(new_payment)  # Add to session
            db.session.commit()  # Commit to save
            return redirect(url_for('success'))  # Redirect to success page
        except ValueError:
            print("Not a valid input")  # Handle invalid input
            return redirect('/payment')  # Redirect back to payment form
            
   return render_template('payment.html', invoice=invoice, payment=payment )  # Render the form for GET requests
"""


@app.route('/create_invoice/<int:booking_id>', methods=['POST'])
def create_invoice(booking_id):
    # Retrieve the booking using the provided booking_id
    booking = Booking.query.get(booking_id)


  # Check if an invoice already exists for this booking
    existing_invoice = Invoice.query.filter_by(booking_id=booking_id).first()
    if existing_invoice:
        # Return the already saved template
        return render_template("already_saved.html")
    
    # Create a new Invoice record based on the Booking
    invoice = Invoice(
         
        id=booking.id,
        user_id =booking.id,
        booking_id= booking.id,
        invoice_date = booking.date, # Set current date as invoice date
        total_amount=booking.total_cost,  # Use total_cost from Booking
        payment_status=True  # Default to unpaid
    )

 
    # Add the invoice to the session and commit
    db.session.add(invoice)
    db.session.commit()

    return redirect(url_for('success'))  # Redirect to a success page

@app.route('/delete_invoice/<int:booking_id>', methods=['POST'])
def delete_invoice(booking_id):
    invoice = Invoice.query.get(booking_id)
    
    if not invoice:
        return "Invoice not found", 404

    db.session.delete(invoice)
    db.session.commit()

    return redirect(url_for('success'))  # Redirect to a success page

  