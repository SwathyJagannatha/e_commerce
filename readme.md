E-Commerce API with Flask and SQLAlchemy

This repository contains a RESTful API built with Flask and SQLAlchemy for managing customers, accounts, products, and orders in an e-commerce application.

Features

1> Customers: CRUD operations for managing customer data including name, email, and phone.

Customer and CustomerAccount Management: Create the CRUD (Create, Read, Update, Delete) endpoints for managing Customers and their associated CustomerAccounts

Create Customer: Implement an endpoint to add a new customer to the database. Ensure that you capture essential customer information, including name, email, and phone number.
Read Customer: Develop an endpoint to retrieve customer details based on their unique identifier (ID). Provide functionality to query and display customer information.
Update Customer: Create an endpoint for updating customer details, allowing modifications to the customer's name, email, and phone number.
Delete Customer: Implement an endpoint to delete a customer from the system based on their ID.


2> CustomerAccounts : CRUD operations for managing unique username and a secure password.
Accounts: Manage customer accounts with username and password, associated with customer profiles.

Create CustomerAccount: Develop an endpoint to create a new customer account. This should include fields for a unique username and a secure password.
Read CustomerAccount: Implement an endpoint to retrieve customer account details, including the associated customer's information.
Update CustomerAccount: Create an endpoint for updating customer account information, including the username and password.
Delete CustomerAccount: Develop an endpoint to delete a customer account.

3> Product Catalog: Create the CRUD (Create, Read, Update, Delete) endpoints for managing Products:

Products: CRUD operations for managing product data including name and price.

Create Product: Implement an endpoint to add a new product to the e-commerce database. Capture essential product details, such as the product name and price.
Read Product: Develop an endpoint to retrieve product details based on the product's unique identifier (ID). Provide functionality to query and display product information.
Update Product: Create an endpoint for updating product details, allowing modifications to the product name and price.
Delete Product: Implement an endpoint to delete a product from the system based on its unique ID.
List Products: Develop an endpoint to list all available products in the e-commerce platform. Ensure that the list provides essential product information.


View and Manage Product Stock Levels (Bonus): Create an endpoint that allows to view and manage the stock levels of each product in the catalog. Administrators should be able to see the current stock level and make adjustments as needed.
Restock Products When Low (Bonus): Develop an endpoint that monitors product stock levels and triggers restocking when they fall below a specified threshold. Ensure that stock replenishment is efficient and timely.

4> Orders: Manage customer orders with date and associated products.

Order Processing: Develop comprehensive Orders Management functionality to efficiently handle customer orders, ensuring that customers can place, track, and manage their orders seamlessly.
Place Order: Create an endpoint for customers to place new orders, specifying the products they wish to purchase and providing essential order details. Each order should capture the order date and the associated customer.
Retrieve Order: Implement an endpoint that allows customers to retrieve details of a specific order based on its unique identifier (ID). Provide a clear overview of the order, including the order date and associated products.
Manage Order History (Bonus): Create an endpoint that allows customers to access their order history, listing all previous orders placed. Each order entry should provide comprehensive information, including the order date and associated products.
Cancel Order (Bonus): Implement an order cancellation feature, allowing customers to cancel an order if it hasn't been shipped or completed. Ensure that canceled orders are appropriately reflected in the system.
Calculate Order Total Price (Bonus): Include an endpoint that calculates the total price of items in a specific order, considering the prices of the products included in the order. This calculation should be specific to each customer and each order, providing accurate pricing information.

Technologies Used:

Python: Programming language used for backend development.
Flask: Micro web framework for Python.
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python.
MySQL: Database management system used for persistent data storage.
Marshmallow: Library for object serialization/deserialization.

Setup Instructions

Clone the repository:

git clone https://github.com/yourusername/e_commerce.git
cd e_commerce
Setup Virtual Environment:

python -m venv my_venv
my_venv\Scripts\activate  # On Windows
source my_venv/bin/activate  # On macOS/Linux

Install Dependencies:

pip install -r requirements.txt

Configure Database:

Ensure MySQL server is running.
Set your database URI in app.config["SQLALCHEMY_DATABASE_URI"] in app.py.

Initialize Database:

python app.py

Run the Application:

flask run

Access API Endpoints:

Customers: GET /customers, POST /customers, PUT /customers/<id>, DELETE /customers/<id>
Accounts: GET /customeraccount, POST /customeraccount, PUT /customeraccount/<id>, DELETE /customeraccount/<id>
Products: GET /products, POST /products, PUT /products/<id>, DELETE /products/<id>
Orders: GET /orders, POST /orders, PUT /orders/<id>, DELETE /orders/<id>

API Documentation

Detailed API documentation can be found in the application.py file with descriptions of each endpoint, request formats, and response formats.

Post request Examples:
.........................

http://127.0.0.1:5000/customers
body:

	{
	"name":"Anwar Kumar",
	"email":"kuhyewed@gmail.com",
	"phone" :"2321321"
	}

customeraccount
................

    {
	"customer_id":"3",
	"username": "Amar kunwar",
	"password":"merrychris345@#@#!@!"
	}

products:

{
	"name":"Countertop organizers",
	"price": 28,
	"stock_level": 1
}

orders:

{
    "date": "2023-07-07",
    "customer_id": 3,
    "products": [
        {
            "product_id": 4,
            "quantity": 1
        },
        {
            "product_id": 2,
            "quantity": 1
        }
    ]
}

delete examples:

http://127.0.0.1:5000/customers/2

http://127.0.0.1:5000/customeraccount/3

http://127.0.0.1:5000/orders/4

http://127.0.0.1:5000/orders/1


http://127.0.0.1:5000/products/1


Get request:
............

http://127.0.0.1:5000/customers

http://127.0.0.1:5000/orders

Sample output:
...............

[
	{
		"customer_id": 1,
		"date": "Sun, 07 Jul 2024 00:00:00 GMT",
		"order_id": 1,
		"products": [
			"western wear"
		]
	},
	{
		"customer_id": 2,
		"date": "Tue, 07 May 2024 00:00:00 GMT",
		"order_id": 2,
		"products": [
			"western wear",
			"Kitchen organizers"
		]
	},
	{
		"customer_id": 1,
		"date": "Thu, 06 Jul 2023 00:00:00 GMT",
		"order_id": 3,
		"products": [
			"formal wear",
			"western wear"
		]
	},
	{
		"customer_id": 3,
		"date": "Fri, 07 Jul 2023 00:00:00 GMT",
		"order_id": 5,
		"products": [
			"western wear",
			"Bathroom organizers"
		]
	}
]

get orders history:
...................
http://127.0.0.1:5000/orders/history?customer_id=2

[
	{
		"customer_id": 2,
		"date": "Tue, 07 May 2024 00:00:00 GMT",
		"order_id": 2,
		"products": [
			{
				"product name": "western wear",
				"product_id": 2
			},
			{
				"product name": "Kitchen organizers",
				"product_id": 3
			}
		]
	}
]

http://127.0.0.1:5000/products

Sample output:
...............

[
	{
		"name": "formal wear",
		"price": 30.0,
		"product_id": 1,
		"stock_level": 13
	},
	{
		"name": "western wear",
		"price": 323.44,
		"product_id": 2,
		"stock_level": 5
	},
	{
		"name": "Kitchen organizers",
		"price": 28.8,
		"product_id": 3,
		"stock_level": 12
	},
	{
		"name": "Bathroom organizers",
		"price": 20.0,
		"product_id": 4,
		"stock_level": 0
	},
	{
		"name": "Countertop organizers",
		"price": 28.0,
		"product_id": 5,
		"stock_level": 0
	}
]


http://127.0.0.1:5000/customeraccount

[
	{
		"account_id": 2,
		"customer_id": 3,
		"password": "merrychris345@#@#!@!",
		"username": "Amar kunwar"
	}
]

Update requests:

customers:
..........

http://127.0.0.1:5000/customers/2


{
		"customer_id": 2,
		"email": "updatedsecondmail",
		"name": "sinha",
		"phone": "777238729"
}

http://127.0.0.1:5000/customers/by_name/sinha

{
		"customer_id": 2,
		"email": "latestmail34@gmail.com",
		"name": "sinha",
		"phone": "777238729"
}


customeraccount:
...............

http://127.0.0.1:5000/customeraccount/3

{	
	"customer_id":2,
	"username": "Shriya",
	"password":"HotChocolate@!"
}

orders:
........

http://127.0.0.1:5000/orders/2

{
    "date": "2024-05-07",
    "customer_id": 2,
    "products": [
        {
            "product_id": 2,
            "quantity": 5
        },
        {
            "product_id": 3,
            "quantity": 1
        }
    ]
}
