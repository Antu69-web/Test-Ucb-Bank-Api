from customers.models.customer import Customer
from database.db import db

def get_all_customers():
    customers = Customer.query.all()
    return [{"id": c.id, "name": c.name, "balance": c.balance} for c in customers]

def add_customer(data):
    if not data or 'name' not in data or 'balance' not in data:
        return {"error": "Invalid customer data"}, 400
        
    new_customer = Customer(name=data['name'], balance=data['balance'])
    db.session.add(new_customer)
    db.session.commit()
    
    return {"message": "Customer added successfully", "customer": {"id": new_customer.id, "name": new_customer.name, "balance": new_customer.balance}}, 201

def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {"message": "Customer deleted successfully"}, 200
        
    return {"error": "Customer not found"}, 404

def add_multiple_customers(data_list):
    if not isinstance(data_list, list):
        return {"error": "Invalid format. Expected a list of customers."}, 400
        
    added_customers = []
    for data in data_list:
        if 'name' in data and 'balance' in data:
            new_customer = Customer(name=data['name'], balance=data['balance'])
            db.session.add(new_customer)
            added_customers.append({"name": data['name'], "balance": data['balance']})
            
    if not added_customers:
        return {"error": "No valid customers found in the list."}, 400
        
    db.session.commit()
    return {"message": f"{len(added_customers)} customers added successfully", "customers": added_customers}, 201
