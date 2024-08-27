from app import db 

class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)

class Order(db.model):
    _tablename_ = 'order_details'
    type_of_services = db.Column(db.String(50), unique=True, nullable=False)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    menu_name = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

class Facilities(db.Model):
    _tablename_ = 'rooms'
    facility_type = db.Column(db.String(50), unique=True, nullable=False)
    pax_number = db.Column(db.String(50), unique=True, nullable=False) 
    checkout_date =  db.Column(db.DateTime, nullable=False)
    checkin_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    _tablename_ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    user = db.relationship('User')
    room = db.relationship('Room')

class Payment(db.Model):
    _tablename_ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount_to_pay = db.Column(db.Float, nullable=False)
    payment_Method = db.Column(db.DateTime, nullable=False)
    Knockoff = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    Remaining_balance = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)


    booking = db.relationship('Booking')

class Invoice(db.Model):
    _tablename_ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    booking = db.relationship('Booking')