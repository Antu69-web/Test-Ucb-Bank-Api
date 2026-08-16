from datetime import datetime
import calendar

def add_months(sourcedate, months):
    """Add months to a date, keeping the day of the month as close as possible."""
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day)

def calculate_emi_details(principal, annual_rate, tenure_months, start_date_str=None, prepayment_amount=0):
    if principal <= 0 or annual_rate <= 0 or tenure_months <= 0:
        return None

    r = annual_rate / 12 / 100
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            start_date = datetime.now()
    else:
        start_date = datetime.now()

    # Apply prepayment on day 1 if any
    actual_principal = principal - prepayment_amount if prepayment_amount > 0 else principal
    if actual_principal <= 0:
        return None  # Prepayment paid off the whole loan

    # Standard EMI based on original terms (some banks do this) 
    # OR recalculate EMI based on new principal.
    # Usually, EMI remains same, tenure reduces. Let's recalculate based on new principal for simplicity if tenure remains same,
    # But real prepayment keeps EMI same and reduces tenure. Let's do that!
    
    # Original EMI calculation
    original_emi = principal * r * ((1 + r) ** tenure_months) / (((1 + r) ** tenure_months) - 1)
    emi = original_emi

    schedule = []
    remaining_balance = actual_principal
    total_interest = 0
    actual_tenure = 0
    total_payment_made = prepayment_amount

    # Generate schedule until balance is 0 or tenure is reached
    for i in range(1, tenure_months + 1):
        if remaining_balance <= 0.01:
            break
            
        interest_for_month = remaining_balance * r
        
        # If remaining balance + interest is less than EMI, adjust the last EMI
        if remaining_balance + interest_for_month < emi:
            emi_for_month = remaining_balance + interest_for_month
            principal_for_month = remaining_balance
        else:
            emi_for_month = emi
            principal_for_month = emi - interest_for_month
            
        remaining_balance -= principal_for_month
        if remaining_balance < 0.01:
            remaining_balance = 0
            
        total_interest += interest_for_month
        total_payment_made += emi_for_month
        actual_tenure += 1

        next_date = add_months(start_date, i)
        
        schedule.append({
            "installment_no": i,
            "payment_date": next_date.strftime("%Y-%m-%d"),
            "emi_amount": round(emi_for_month, 2),
            "principal_paid": round(principal_for_month, 2),
            "interest_paid": round(interest_for_month, 2),
            "remaining_balance": round(remaining_balance, 2)
        })

    return {
        "monthly_emi": round(original_emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment_made, 2),
        "actual_tenure_months": actual_tenure,
        "prepayment_applied": round(prepayment_amount, 2),
        "schedule": schedule
    }
