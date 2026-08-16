from flask import Blueprint
from calculator.controllers.calculator_controller import handle_emi_calculation

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/emi', methods=['POST'])
def emi_calculator():
    """
    Calculate EMI with Schedule and Prepayment
    ---
    tags:
      - Calculator
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            principal:
              type: number
              example: 100000
              description: The total loan amount
            rate:
              type: number
              example: 10.5
              description: Annual interest rate in percentage
            time:
              type: integer
              example: 12
              description: Original loan tenure in months
            start_date:
              type: string
              example: "2026-08-16"
              description: Optional. Date the loan starts (YYYY-MM-DD)
            prepayment_amount:
              type: number
              example: 15000
              description: Optional. Amount paid in advance to reduce principal
    responses:
      200:
        description: EMI calculation result
      400:
        description: Invalid inputs
    """
    return handle_emi_calculation()
