from database.dummy_db import loan_requests_data, customers_data

def process_loan_approval(request_id):
    """
    Business logic to approve a loan.
    Finds the request, updates its status, and updates the customer's balance.
    """
    for req in loan_requests_data:
        if req['id'] == request_id:
            if req['status'] != 'pending':
                return False, "Request is already processed."
            
            # Find customer
            customer = next((c for c in customers_data if c['id'] == req['customer_id']), None)
            if not customer:
                return False, "Customer not found."
            
            # Update data
            req['status'] = 'approved'
            customer['balance'] += req['amount']
            return True, f"Loan approved and {req['amount']} added to customer {customer['name']}."
            
    return False, "Request not found."

def process_loan_rejection(request_id):
    """
    Business logic to reject a loan.
    """
    for req in loan_requests_data:
        if req['id'] == request_id:
            if req['status'] != 'pending':
                return False, "Request is already processed."
            
            req['status'] = 'rejected'
            return True, "Loan request rejected successfully."
            
    return False, "Request not found."
