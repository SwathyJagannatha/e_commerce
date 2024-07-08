# Opening a virtual Environment:
# python -m venv my_venv

# Next we will need to activate it.
# my_venv\Scripts\activate

# Next we need to install Flask into the virtual environment.
# pip install flask

# Now we need to install Flask Marshmalllow
# pip install flask-marshmallow

#Now we need to go install the sql connector
#pip install mysql-connector-python


#Now we can Start Setting up our imports

from flask import Flask, jsonify, request #imports flask and allows us to instantiate an app
from flask_sqlalchemy import SQLAlchemy # this is Object Relational Mapper
from sqlalchemy import select,delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,Session # this is a class that all of our classes will inherit
# provides base functionality for converting python objects to rows of data
from flask_marshmallow import Marshmallow # creates our schema to validate incoming and outgoing data
from flask_cors import CORS # Cross Origin Resource Sharing - allows our application to be accessed by 3rd parties
import datetime
from typing import List #tie a one to many relationship back to the one
from marshmallow import ValidationError,fields,validate

app = Flask(__name__) # instantiate our app 
CORS(app) 

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Swa123sweet%40@localhost/e_commerce_dbnew"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app,model_class=Base)

ma = Marshmallow(app)

# ======================= DB Models ======================

# ==== DB MODELS =============================================================================================================================================
# The DB models are the classes that represent the tables in our database. We will create the following tables:
# Customer
# CustomerAccount
# Order
# Product

# Customer table with a one to one relationship with the CustomerAccount table and a one to many relationship with the Order table
class Customer(Base):
    __tablename__ = "Customers"
    customer_id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(db.String(255),nullable = False)
    email : Mapped[str] = mapped_column(db.String(355),nullable = False)
    phone : Mapped[str] = mapped_column(db.String(20))
    customer_account : Mapped["CustomerAccount"] = db.relationship(back_populates="customer")
    # add orders back populate
    orders: Mapped[List["Order"]] = db.relationship(back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = "Customer_Accounts"
    account_id : Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(db.String(25),nullable=False,unique=True)
    password :Mapped[int] = mapped_column(db.String(20),nullable=False)
    customer_id : Mapped[int] = mapped_column(db.ForeignKey('Customers.customer_id'))

    customer : Mapped["Customer"] = db.relationship(back_populates="customer_account")

# associate table between orders and products to manage the many to many relationship
order_product = db.Table(
    "Order_Product", #association table name
    Base.metadata,
    db.Column("order_id", db.ForeignKey("Orders.order_id"), primary_key=True),
    db.Column("product_id", db.ForeignKey("Products.product_id"), primary_key=True)      
)

# creating Orders and a one to many relationship bewtween Customer and Order
class Order(Base):
    __tablename__ = "Orders"
    order_id : Mapped[int] = mapped_column(primary_key=True)
    date : Mapped[datetime.date] = mapped_column(db.Date,nullable=False)
    customer_id : Mapped[int] = mapped_column(db.ForeignKey('Customers.customer_id'),nullable=False)
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product)
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")

class Product(Base):
    __tablename__ = "Products"
    product_id : Mapped[int] = mapped_column(primary_key=True)
    name  : Mapped[str] = mapped_column(db.String(255),nullable = False)
    price : Mapped[str] = mapped_column(db.Float,nullable = False)
    stock_level :Mapped[int] = mapped_column(db.Integer())
    #orders : Mapped[List["Order"]] = db.relationship(back_populates="product")

############## CustomerSchema ##########################

# We will need a schema for each of the tables in our database. We will create the following schemas:
# CustomerSchema
# AccountSchema
# ProductSchema
# OrderSchema

# The CustomerSchema class is used to validate the data that is sent to the API and to serialize the data that is returned from the API.
class CustomerSchema(ma.Schema):
    customer_id = fields.Integer()
    name = fields.String(required = True)
    email = fields.String(required = True)
    phone = fields.String(required=True)

    class Meta:
        # fields to show in a get request
        fields = ("customer_id","email","name","phone")

#instantiate the schemas
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


################### Customer Account Schema ###########

class AccountSchema(ma.Schema):
    account_id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True) # foreign key

    class Meta:
        fields = ("account_id","username","password","customer_id")

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

####################################################################

class OrderProductSchema(ma.Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True,validate=validate.Range(min=1))
    pass

##################### OrderSchema #######################

class OrderSchema(ma.Schema):
    order_id = fields.Integer()
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    product_id = fields.List(fields.Integer(),required=False)
    products = fields.List(fields.Nested(OrderProductSchema))
    class Meta:
        fields = ("order_id","date","customer_id","product_id","products")

order_schema = OrderSchema()
orders_schema = OrderSchema(many = True) 

###################### Productschema #############################

class ProductSchema(ma.Schema):
    product_id = fields.Integer()
    name = fields.String(required=True)
    price = fields.Float(required=True)
    stock_level = fields.Integer(required=True)

    class Meta:
        fields = ("product_id","name","price","stock_level")

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)

######################################################################
    
with app.app_context():
    # db.drop_all()
    db.create_all()

# tables we have

#customer
#customeraccount
#order
#orderProduct -- many to many
#product

############################### Customer Crud ###################

# ==== CUSTOMERS API ROUTES =========================================================================================
# The API routes are used to interact with the database through the API. We will create the following routes:
# GET /customers - get all customers
# POST /customers - add a customer
# PUT /customers/<id> - update a customer by id
# DELETE /customers/<id> - delete a customer by id

# Get customers

@app.route("/customers", methods=["GET"])

def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars()
    customers = result.all()
    return customers_schema.jsonify(customers)

# Add a customer

@app.route("/customers",methods=["POST"])
def add_customers():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    
    with Session(db.engine) as session:
        with session.begin():
            name = customer_data['name']
            email = customer_data['email']
            phone = customer_data['phone']

            new_customer = Customer(name = name,email=email,phone=phone)
            session.add(new_customer)
            session.commit()
    return jsonify({"Message":"New Customer Added successfully!!"})

# update customer based on the id

@app.route("/customers/<int:id>",methods=["PUT"])
def update_customers(id):
    with Session(db.engine) as session:
        with session.begin():
            query = select(Customer).filter(Customer.customer_id == id)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"Customer not found"}),404
            customer = result

            try:
                cust_data = customer_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages),400

            for field,value in cust_data.items():
                setattr(customer,field,value)
            
            session.commit()

    return jsonify({"Message": "Customer Info Updated Successfully!!"})

#update the customer based on the name

@app.route("/customers/by_name/<string:name_val>",methods=["PUT"])
def update_customers_by_name(name_val):
    with Session(db.engine) as session:
        with session.begin():
            query = select(Customer).filter(Customer.name == name_val)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"Customer not found"}),404
            customer = result

            try:
                cust_data = customer_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages),400

            for field,value in cust_data.items():
                setattr(customer,field,value)
            
            session.commit()

    return jsonify({"Message": "Customer Info Updated Successfully!!"})

@app.delete("/customers/<int:cust_id>")
def delete_customers(cust_id):
    with Session(db.engine) as session:
        with session.begin():
            query = select(Customer).filter(Customer.customer_id == cust_id)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"Customer not found"}),404
            
            session.delete(result)
        return jsonify({"message":"Customer removed successfully!!"})
    
################## CustomerAccount Crud ############

# The AccountSchema class is used to validate the data that is sent to the API and to serialize the data that is returned from the API.

# ==== CustomerAccount API ROUTE ========================================================================
# The API routes are used to interact with the database through the API. We will create the following routes:
# GET /customeraccount - get all customer accounts
# POST /customeraccount - add a customer account
# PUT /customeraccount/<id> - update a customer account by id
# DELETE /customeraccount/<id> - delete a customer account by id

# get customeraccount

@app.route("/customeraccount",methods = ["GET"])
def get_customer_account():
    query=select(CustomerAccount)
    result = db.session.execute(query).scalars()
    cust_account = result.all()
    return accounts_schema.jsonify(cust_account)    

# add customeraccount

@app.post("/customeraccount")
def add_customer_account():
    try:
        customer_acc_data =account_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    
    with Session(db.engine) as session:
        with session.begin():
            new_account = CustomerAccount(username=customer_acc_data['username'],password=customer_acc_data['password'],customer_id = customer_acc_data['customer_id'])
            session.add(new_account)
            session.commit()
    return jsonify({"message": "New Customer Account added"})
    
# update customer account

@app.put("/customeraccount/<int:accid>")
def update_customer_account(accid):
    with Session(db.engine) as session:
        with session.begin():
            query = select(CustomerAccount).filter(CustomerAccount.account_id == accid)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"CustomerAccount not found"}),404 # Resource not found

            cust_accnt = result

            try:
                cust_accnt_data = account_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages),400 # Bad Request

            for field,value in cust_accnt_data.items():
                setattr(cust_accnt,field,value)

            session.commit()

    return jsonify({"message":"Customer Account details updated successfully"}),200

# ============================ Delete CustomerAccount ===================================== #

@app.delete("/customeraccount/<int:acc_id>")
def delete_customer_Account(acc_id):
    with Session(db.engine) as session:
        with session.begin():
            query=select(CustomerAccount).filter(CustomerAccount.account_id == acc_id)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"Customer Account not found"}),404
            session.delete(result)
        return jsonify({"message":"Customer Account deleted successfully"})
    

#----------------------------- API Routes for orders --------------------------#

# ==== Orders API ROUTE ========================================================================
# The API routes are used to interact with the database through the API. We will create the following routes:
# GET /orders - get all orders
# POST /orders - add an order
# PUT /orders/<id> - update an order by id
# DELETE /orders/<id> - delete an order by id
# For this one we use @app.method instead of @app.route showing we can use different methods

# Get orders

@app.route("/orders",methods=["GET"])
def get_orders():
    query = select(Order) #select * from order
    result = db.session.execute(query).scalars().all()
    orders_with_products = []
    orders = result
    for order in orders:
        order_dict = {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "date": order.date,
            "products": [product.name for product in order.products]
            # can also just display product.product_id
        }
        orders_with_products.append(order_dict)

    return jsonify(orders_with_products)

# ----------------create orders ------------------

@app.route("/orders",methods=["POST"])
def add_orders():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400
    product_ids = order_data.get('product_id',[])
    products = order_data.get('products',[])

    new_order = Order(
        customer_id = order_data['customer_id'], 
        date = order_data['date'],
    )

    with Session(db.engine) as session:
        with session.begin():
            
            for product_info in order_data['products']:
                product_id = product_info['product_id']
                quantity = product_info['quantity']

                product = session.query(Product).get(product_id)

                if product is None:
                    return jsonify({"Message":f"Product with id {product_id} deosnt exist"}),404
                
                if product.stock_level < quantity:
                    return jsonify({"Message":f"Sorry, Not enough Product Stock for product {product.name}, available stock is {product.stock_level}"}),404
                
                product.stock_level -= quantity 
                new_order.products.append(product)

            session.add(new_order)
            session.commit()

    return jsonify({"Message":"New Order added successfully"}),201

######################### manage order history #################

# http://127.0.0.1:5000/orders/history?customer_id=2 -> request format

@app.route("/orders/history",methods=["GET"])
def get_orders_custid():
    id = request.args.get("customer_id")
    query = select(Order).where(Order.customer_id == id).order_by(Order.order_id.asc()) #select * from order
    result = db.session.execute(query).scalars().all()
    orders_with_products = []
    orders = result
    for order in orders:
        order_dict = {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "date": order.date,
            "products": [{"product_id":product.product_id ,"product name" :product.name} for product in order.products]
        }
        orders_with_products.append(order_dict)

    return jsonify(orders_with_products),200

# @app.route("/orders/history", methods=["GET"])
# def get_orders_custid():
#     customer_id = request.args.get("customer_id")
#     if not customer_id:
#         return jsonify({"Error": "customer_id query parameter is required"}), 400

#     with Session(db.engine) as session:
#         query = select(Order).where(Order.customer_id == customer_id).order_by(Order.order_id.asc())
#         orders = session.execute(query).scalars().all()
#         if not orders:
#             return jsonify({"Error": f"No orders found for customer_id {customer_id}"}), 404

#         orders_with_products = []
#         for order in orders:
#             order_dict = {
#                 "order_id": order.order_id,
#                 "customer_id": order.customer_id,
#                 "date": order.date,
#                 "products": [{"product_id": p.product_id, "name": p.name} for p in order.products]
#             }
#             orders_with_products.append(order_dict)

#     return jsonify(orders_with_products), 200

############################# update orders #########################

@app.route("/orders/<int:orderid>",methods=["PUT"])
def update_orders(orderid):
    with Session(db.engine) as session:
        with session.begin():
            query = select(Order).filter(Order.order_id == orderid)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message": "Order not found"}), 404  # Resource not found

            order_info = result

            try:
                order_data = order_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400  # Bad Request

            # Store the original product quantities
            original_product_quantities = {product.product_id: 0 for product in order_info.products}
            for product in order_info.products:
                original_product_quantities[product.product_id] += 1

            # Update order info
            order_info.customer_id = order_data.get('customer_id', order_info.customer_id)
            order_info.date = order_data.get('date', order_info.date)

            # Clear existing products to add updated ones
            order_info.products.clear()

            # Track product quantities in the new order
            new_product_quantities = {}
            for product_info in order_data['products']:
                product_id = product_info['product_id']
                new_quantity = product_info['quantity']
                new_product_quantities[product_id] = new_quantity

            for product_id, new_quantity in new_product_quantities.items():
                product = session.query(Product).get(product_id)

                if product is None:
                    return jsonify({"Message": f"Product with id {product_id} doesn't exist"}), 404

                old_quantity = original_product_quantities.get(product_id, 0)
                quantity_difference = new_quantity - old_quantity

                if product.stock_level < quantity_difference:
                    return jsonify({"Message": f"Sorry, not enough product stock for product {product.name}, available stock is {product.stock_level}"}), 404

                # Update the stock level
                product.stock_level -= quantity_difference

                # Add the product to the order's products list
                order_info.products.extend([product] * new_quantity)

            session.commit()

        return jsonify({"message": "Order details updated successfully"}), 200

#########################  delete/cancel orders ##################

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def cancel_order(order_id):
    with Session(db.engine) as session:
        with session.begin():
            # Check if the order exists
            order = session.get(Order, order_id)
            if order is None:
                return jsonify({"Error": f"Order with id {order_id} doesn't exist"}), 404
            
            # Delete related entries in order_product table
            delete_statement = delete(order_product).where(order_product.c.order_id == order_id)
            session.execute(delete_statement)
            
            # Delete the order
            session.delete(order)
            session.commit()

        return jsonify({"message": "Order deleted successfully"}), 200

###################### product api routes ################################

# ==== Products API ROUTEs ========================================================================
# The API routes are used to interact with the database through the API. We will create the following routes:
# GET /products - get all products
# POST /products - add a product
# PUT /products/<id> - update a product by id
# DELETE /products/<id> - delete a product by id

# get products

@app.route("/products",methods=["GET"])
def get_products():
    query = select(Product)
    result = db.session.execute(query).scalars()
    products = result.all()
    return products_schema.jsonify(products)

@app.route("/products",methods=["POST"])
def add_products():
    try:
        product_data = product_schema.load(request.json)
        print("Validated Data:",product_data)
    except ValidationError as err:
        print("Validation error:", err.messages)
        return jsonify(err.messages),400
    
    with Session(db.engine) as session:
        with session.begin():
            name = product_data['name']
            price = product_data['price']
            stock_level = product_data['stock_level']

            new_product = Product(name = name ,price=price,stock_level=stock_level)
            session.add(new_product)
            session.commit()
    return jsonify({"Message":"New Product added successfully"})

########## update products ##################

@app.route("/products/<int:product_id>",methods =["PUT"])
def update_product(product_id):
    with Session(db.engine) as session:
        with session.begin():
            #then we have to find the product in the db
            query = select(Product).filter(Product.product_id == product_id)
            result = session.execute(query).scalar() # this is the same as scalars().first() - first result
            print(result)
            if result is None:
                #no product found
                return jsonify({"error": "Product not found"}), 404
            product = result
            try:
                product_data = product_schema.load(request.json)
            except ValidationError as err:
                # always let them know when they mess up
                return jsonify(err.messages),400 # bad request

            #once we have the product and valid data, we can update!!
            for field,value in product_data.items():
                setattr(product,field,value)
            #save to db
            session.commit()
            return jsonify({"Message":f"Product with id {product_id} updated successfully"}),200 # update successful

####################### delete products ########################

@app.delete("/products/<int:product_id>")
def delete_products(product_id):
    with Session(db.engine) as session:
        with session.begin():
            query=select(Product).filter(Product.product_id == product_id)
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"message":"Product not found"}),404
            product_name = result.name
            stock_level = result.stock_level
            session.delete(result)
        return jsonify({"message":f"Product with id {product_id} and name {product_name} and stock-level {stock_level} deleted successfully"})

#--------------------------- default route -----------------------------#

@app.route("/")
def home():
    return "<h1>This a tasty api (ヘ･_･)ヘ┳━┳  (╯°□°）╯︵ ┻━┻</h1>"

if __name__ == "__main__": #check that the file we're in is the file thats being run
    app.run(debug=True) #if so we run our application and turn on the debugger



