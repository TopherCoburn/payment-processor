import logging
import datetime
from typing import Dict, List

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_payment_data(payment_data: Dict) -> bool:
    required_fields = ['amount', 'currency', 'payment_method', 'customer_id']
    for field in required_fields:
        if field not in payment_data:
            logging.error(f"Missing required field: {field}")
            return False
    return True

def calculate_payment_fee(payment_data: Dict) -> float:
    fee_percentage = 0.02
    if payment_data['payment_method'] == 'credit_card':
        fee_percentage = 0.03
    return payment_data['amount'] * fee_percentage

def process_payment(payment_data: Dict) -> Dict:
    if not validate_payment_data(payment_data):
        return {'status': 'failed', 'error': 'Invalid payment data'}
    fee = calculate_payment_fee(payment_data)
    payment_data['fee'] = fee
    payment_data['status'] = 'processed'
    payment_data['processed_at'] = datetime.datetime.now().isoformat()
    return payment_data

def get_payment_history(customer_id: str) -> List[Dict]:
    # This function would typically query a database for payment history
    # For demonstration purposes, a mock payment history is returned
    return [
        {'amount': 10.0, 'currency': 'USD', 'payment_method': 'bank_transfer', 'status': 'processed', 'processed_at': '2022-01-01T12:00:00'},
        {'amount': 20.0, 'currency': 'EUR', 'payment_method': 'credit_card', 'status': 'processed', 'processed_at': '2022-01-15T14:00:00'}
    ]