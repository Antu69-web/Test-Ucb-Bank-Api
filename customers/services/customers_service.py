import pandas as pd
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

def upload_customers_from_file(file):
    filename = file.filename
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file)
        else:
            return {"error": "Invalid file format. Please upload a .csv or .xlsx file."}, 400
            
        # Smart column mapping
        df.columns = df.columns.str.lower().str.strip()
        
        name_variations = ['name', 'customer name', 'full name', 'client name', 'customer', 'id name']
        balance_variations = ['balance', 'account balance', 'amount', 'current balance', 'taka']
        
        actual_name_col = next((col for col in df.columns if col in name_variations), None)
        actual_balance_col = next((col for col in df.columns if col in balance_variations), None)
        
        if not actual_name_col or not actual_balance_col:
            return {"error": f"Could not find valid 'name' or 'balance' columns. Found: {list(df.columns)}"}, 400
            
        df = df.rename(columns={actual_name_col: 'name', actual_balance_col: 'balance'})
            
        df = df.dropna(subset=['name'])
        df['balance'] = df['balance'].fillna(0).astype(int)
        
        data_list = df[['name', 'balance']].to_dict('records')
        
        # Reuse the bulk insertion logic
        return add_multiple_customers(data_list)
        
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}, 500
