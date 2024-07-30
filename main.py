from datetime import datetime

from bson import ObjectId
from flask import Flask, request, redirect, url_for, session, render_template, render_template_string, flash, jsonify
from functools import wraps
from pymongo.mongo_client import MongoClient
from bson.binary import Binary
import base64

uri = "mongodb+srv://Sanjay:98tbzGvuKfNUgEVc@cluster0.byqcgoi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client["Auction"]

app = Flask(__name__)
app.secret_key = "2ec59840e6ec02253bc9de4b91aec47741c4a2e57ed02e32eb2eb671123be40a"

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    #upcomingauction_collection = db["UpcomingAuction"]
    liveauction_collection = db["LiveAuction"]
    pastauction_collection = db["PastAuction"]

    # Retrieve data for upcoming auctions
    # products_upcoming = upcomingauction_collection.find()
    # products_upcoming_with_images = []
    # # Convert binary image data to Base64 for each product and append to the list
    # for product in products_upcoming:
    #     image_binary_data = product.get("image")
    #     if image_binary_data:
    #         image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
    #     else:
    #         image_base64 = None
    #     product_with_image = {**product, "image_base64": image_base64}
    #     products_upcoming_with_images.append(product_with_image)

    # Retrieve data for live auctions
    products_live = liveauction_collection.find()
    products_live_with_images = []
    for product in products_live:
        image_binary_data = product.get("image")
        if image_binary_data:
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
        product_with_image = {**product, "image_base64": image_base64}
        products_live_with_images.append(product_with_image)

    # Retrieve data for past auctions
    products_past = pastauction_collection.find()
    products_past_with_images = []
    for product in products_past:
        image_binary_data = product.get("image")
        if image_binary_data:
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
        product_with_image = {**product, "image_base64": image_base64}
        products_past_with_images.append(product_with_image)
    return render_template("index.html",
                           products_live=products_live_with_images,
                           products_past=products_past_with_images)


@app.route("/bid", methods=["POST","GET"])
def bid():
    # Get the product ID and type from the query parameters
    product_id = request.args.get('product_id')
    product_type = request.args.get('product_type')
    user_name = request.args.get('user_name')
    # Fetch the product information based on the product ID and type
    product = None
    if product_type == 'live':
        product = db['LiveAuction'].find_one({'_id': ObjectId(product_id)})
    elif product_type == 'past':
        product = db['PastAuction'].find_one({'_id': ObjectId(product_id)})
    # Check if product exists
    if product:
        image_binary_data = product.get("image")
        if image_binary_data:
            # Convert image to Base64
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
    else:
        # Handle the case where no product is found
        image_base64 = None

    bid_info = db['Bid'].find_one({'product_name': product['name']})
    # If no bid is found, set bid_info to None
    if not bid_info:
        bid_info = {'message': 'No bid placed for this product by this user'}

    # Add the Base64 image and bid information to the context dictionary
    product_with_image = {"product": product, "image_base64": image_base64, "bid_info": bid_info}
    # Render the bidding page with the product information
    return render_template('biddingplace.html', product=product_with_image, uname=user_name)
@app.route("/login", methods=["GET", "POST"])
def login():
    users_collection = db["Customer"]
    if request.method == "POST":
        # Get username and password from the login form
        email = request.form['email']
        password = request.form['password']

        # Query the MongoDB database for the user
        user = users_collection.find_one({"email": email, "password": password})

        if user:
            # Valid credentials, set the session username
            session['username'] = user['username']
            # Redirect to home page
            return redirect(url_for('home', name=user['username']))
        else:
            # Invalid credentials, render login page with error message
            return render_template("login.html", error="Invalid username or password")

    # If the request method is GET (i.e., user is accessing the login page)
    return render_template("login.html")

@app.route("/home/<name>")
def home(name):
    upcomingauction_collection = db["UpcomingAuction"]
    liveauction_collection = db["LiveAuction"]
    pastauction_collection = db["PastAuction"]

    # Retrieve data for upcoming auctions
    products_upcoming = upcomingauction_collection.find()
    products_upcoming_with_images = []

    # Convert binary image data to Base64 for each product and append to the list
    for product in products_upcoming:
        image_binary_data = product.get("image")
        if image_binary_data:
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
        product_with_image = {**product, "image_base64": image_base64}
        products_upcoming_with_images.append(product_with_image)

    # Retrieve data for live auctions
    products_live = liveauction_collection.find()
    products_live_with_images = []
    for product in products_live:
        image_binary_data = product.get("image")
        if image_binary_data:
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
        product_with_image = {**product, "image_base64": image_base64}
        products_live_with_images.append(product_with_image)

    # Retrieve data for past auctions
    products_past = pastauction_collection.find()
    products_past_with_images = []
    for product in products_past:
        image_binary_data = product.get("image")
        if image_binary_data:
            image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        else:
            image_base64 = None
        product_with_image = {**product, "image_base64": image_base64}
        products_past_with_images.append(product_with_image)
    return render_template("home.html",
                           products_upcoming=products_upcoming_with_images,
                           products_live=products_live_with_images,
                           products_past=products_past_with_images,user_name=name)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    users_collection = db["Customer"]
    if request.method == "POST":
        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        address = request.form.get("address")

        # Check if email already exists in the database
        existing_email_user = users_collection.find_one({"email": email})
        if existing_email_user:
            # Email already exists, render signup page with error message
            return render_template("signup.html", error="Email already exists")

        # Check if username already exists in the database
        existing_username_user = users_collection.find_one({"username": name})
        if existing_username_user:
            # Username already exists, render signup page with error message
            return render_template("signup.html", error="Username already exists")

        # Read the default image file
        with open("Images/default.jpeg", "rb") as file:
            default_image_data = file.read()

        # Insert new user data into the database with default profile picture
        new_user = {
            "username": name,
            "email": email,
            "password": password,
            "address": address,
            "profile_picture": default_image_data
        }
        users_collection.insert_one(new_user)

        # Redirect to home page after successful signup
        return redirect(url_for("home", name=name))

    # If it's a GET request, render the signup page
    return render_template("signup.html")

@app.route("/biddingplace")
@login_required
def biddingplace():
    # Render the "biddingplace" template
    return render_template("biddingplace.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route('/profile')
def profile():
    # Get the username query parameter from the URL
    username = request.args.get('username')

    # Retrieve person information from the customer table using the username
    profile = db["Customer"].find_one({"username": username})

    image_binary_data = profile.get("profile_picture")
    if image_binary_data:
        image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
    else:
        image_base64 = None

    # Add the Base64 image to the profile dictionary
    profile_with_image = {**profile, "image_base64": image_base64}
    # Render the profile.html template and pass the user information
    return render_template("profile.html", user=profile_with_image)

@app.route('/profile/editprofile')
def editprofile():
    username = request.args.get('username')

    # Retrieve person information from the customer table using the username
    profile = db["Customer"].find_one({"username": username})

    image_binary_data = profile.get("profile_picture")
    if image_binary_data:
        image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
    else:
        image_base64 = None

    # Add the Base64 image to the profile dictionary
    profile_with_image = {**profile, "image_base64": image_base64}
    # Render the profile.html template and pass the user information
    return render_template("editprofile.html", user=profile_with_image)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Get the form data
    username = request.form.get('username')
    email = request.form.get('email')
    location = request.form.get('location')

    # Get the uploaded image file
    profile_image = request.files['profile-image']
    image_data = profile_image.read()

    # Update the user's document in the database with the new profile information
    db["Customer"].update_one({"username": username}, {"$set": {"email": email, "address": location}})

    # Update the profile picture if an image was uploaded
    if image_data:
        db["Customer"].update_one({"username": username}, {"$set": {"profile_picture": Binary(image_data)}})

    # Redirect the user to their updated profile page
    return redirect(url_for('profile', username=username))

@app.route('/submit_bid', methods=['POST'])
def submit_bid():
    bids_collection = db['Bid']

    username = request.args.get('user_name')
    product_name = request.args.get('product_name')
    bid_amount = request.form['bidAmount']
    bid_limit = request.form['bidLimit']

    # Check if the username and product name already exist in the database
    existing_bid = bids_collection.find_one({'username': username, 'product_name': product_name})

    if existing_bid:
        # If the username and product name exist, update the existing bid
        bids_collection.update_one({'username': username, 'product_name': product_name},
                                   {'$set': {'amount': bid_amount, 'limit': bid_limit}})
        message = f'Bid for {username} on {product_name} updated successfully.'
    else:
        # If the username and product name don't exist, insert a new bid
        new_bid = {'username': username, 'product_name': product_name, 'amount': bid_amount, 'limit': bid_limit}
        bids_collection.insert_one(new_bid)
        message = f'New bid for {username} on {product_name} added successfully.'

    return redirect(url_for('home', name=username))

@app.route('/postproduct')
def post_product():
    return render_template('postproduct.html',username=request.args.get('name'))

@app.route('/post_product',methods=['POST'])
def postproduct():
    live_auction_collection = db['LiveAuction']
    if request.method == 'POST':
        # Get the form data
        product_name = request.form['name']
        base_price = float(request.form['base_price'])  # Convert to float if needed
        shipment_from = request.form['shipment_from']
        end_date = request.form['end_date']
        image = request.files['image']
        image_data = image.read()

        # Parse and format the end date
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

        # Get the current date (without time)
        start_time = datetime.now().strftime('%d-%m-%Y')

        # Create the document to be inserted into the LiveAuction collection
        product_data = {
            'name': product_name,
            'base_price': base_price,
            'shipment_from': shipment_from,
            'start_date': start_time,
            'end_date': end_date,
            'image': Binary(image_data)
        }

        # Insert the product information into the LiveAuction collection
        inserted_product = live_auction_collection.insert_one(product_data)

        # Check if insertion was successful
        if inserted_product.inserted_id:
            # Redirect to the product upload page
            return redirect(url_for('home', name=request.args.get('name')))
        else:
            return jsonify({'status': 'error', 'message': 'Failed to upload product'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'})

@app.route('/handle_end_date', methods=['POST'])
def handle_end_date():
    # Get the product ID from the request data
    product_id = request.form.get('product_id')

    # Fetch the product information based on the product ID
    product = db['LiveAuction'].find_one({'_id': ObjectId(product_id)})

    if product:
        # Fetch all bids for the product
        bids = db['Bid'].find({'product_name': product['name']})

        # Find the highest bid
        highest_bid = None
        winning_user = None
        for bid in bids:
            if highest_bid is None or bid['amount'] > highest_bid:
                highest_bid = bid['amount']
                winning_user = bid['username']

        # Update the product information with the winning user and bid amount
        product['winner'] = winning_user
        product['winning_bid'] = highest_bid

        # Remove the product from the LiveAuction table
        db['LiveAuction'].delete_one({'_id': ObjectId(product_id)})

        # Insert the product into the PastAuction table
        db['PastAuction'].insert_one(product)

        # Return a response indicating success
        return redirect(url_for('home', username=winning_user))

    else:
    # Return a response indicating failure
        return jsonify({'error': 'Product not found'})