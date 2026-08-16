from flask import request, jsonify
from calculator.services.calculator_service import calculate_emi_details

def handle_emi_calculation():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
        
    try:
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        time = int(data.get('time', 0))
        start_date = data.get('start_date', None)
        prepayment_amount = float(data.get('prepayment_amount', 0))
    except ValueError:
        return jsonify({"error": "Invalid input types."}), 400

    if principal <= 0 or rate <= 0 or time <= 0:
        return jsonify({"error": "Inputs must be greater than 0"}), 400
        
    details = calculate_emi_details(principal, rate, time, start_date, prepayment_amount)
    
    if not details:
        return jsonify({"error": "Calculation failed. Ensure prepayment is not larger than principal."}), 400
    
    return jsonify({
        "loan_details": {
            "principal_amount": principal,
            "annual_interest_rate": rate,
            "original_tenure_months": time,
            "prepayment_applied": details["prepayment_applied"]
        },
        "payment_summary": {
            "monthly_emi": details["monthly_emi"],
            "actual_tenure_months": details["actual_tenure_months"],
            "total_interest_payable": details["total_interest"],
            "total_payment": details["total_payment"]
        },
        "amortization_schedule": details["schedule"],
        "message": "EMI and schedule calculated successfully"
    }), 200
