from workflow.models.loan_request import LoanRequest
from customers.models.customer import Customer
from database.db import db

def request_loan(data):
    customer_id = data.get('customer_id')
    amount = data.get('amount')
    
    if not customer_id or not amount:
        return {"error": "Missing customer_id or amount"}, 400
        
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404
        
    new_request = LoanRequest(customer_id=customer_id, amount=amount)
    db.session.add(new_request)
    db.session.commit()
    
    return {"message": "Loan request submitted successfully", "request_id": new_request.id}, 201

def get_pending_loans():
    requests = LoanRequest.query.filter_by(status='pending').all()
    return [{"id": r.id, "customer_id": r.customer_id, "amount": r.amount, "status": r.status} for r in requests]

def approve_loan(request_id):
    loan_request = LoanRequest.query.get(request_id)
    
    if not loan_request:
        return {"error": "Loan request not found"}, 404
        
    if loan_request.status != 'pending':
        return {"error": f"Loan is already {loan_request.status}"}, 400
        
    # Update status and balance
    loan_request.status = 'approved'
    
    customer = Customer.query.get(loan_request.customer_id)
    if customer:
        customer.balance += loan_request.amount
        
    db.session.commit()
    
    return {"message": "Loan approved and balance updated successfully"}, 200

def reject_loan(request_id):
    loan_request = LoanRequest.query.get(request_id)
    
    if not loan_request:
        return {"error": "Loan request not found"}, 404
        
    if loan_request.status != 'pending':
        return {"error": f"Loan is already {loan_request.status}"}, 400
        
    loan_request.status = 'rejected'
    db.session.commit()
    
    return {"message": "Loan request rejected"}, 200
