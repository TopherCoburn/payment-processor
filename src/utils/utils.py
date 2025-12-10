# utils.py for payment-processor project
import logging
import datetime

def calculate_fee(amount):
    fee_percentage = 0.02  # 2% fee
    return amount * fee_percentage

def log_transaction(transaction_id, amount, status):
    logging.info(f'Transaction {transaction_id}: {amount} - {status}')

def validate_card_number(card_number):
    # Luhn algorithm for card number validation
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class PaymentError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def process_payment(card_number, amount):
    if not validate_card_number(card_number):
        raise PaymentError('Invalid card number', 400)
    try:
        fee = calculate_fee(amount)
        log_transaction('temp', amount, 'processing')
        # simulate payment processing
        log_transaction('temp', amount, 'success')
        return fee
    except Exception as e:
        log_transaction('temp', amount, 'failed')
        raise PaymentError('Payment processing failed', 500) from e
    finally:
        log_transaction('temp', amount, 'completed')