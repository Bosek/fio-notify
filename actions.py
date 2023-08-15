from datetime import datetime
from os import getenv

from fio import get as fio_get
from fio import get_transactions as fio_get_transactions
from sms import send as sms_send


def fio_set_last(args):
    date_format = "%Y-%m-%d"
    date_start = datetime.strptime(args.date_start, date_format)
    date_start_formatted = date_start.strftime(date_format)
    date_end = datetime.strptime(args.date_end, date_format)
    date_end_formatted = date_end.strftime(date_format)

    transactions, _ = fio_get_transactions(f"periods/<token>/{date_start_formatted}/{date_end_formatted}/transactions.json")
    if transactions is None or len(transactions) == 0:
        print("Could not set last date(first step).")
        return
    
    transaction = transactions[-1]
    req = fio_get(f"set-last-id/<token>/{transaction.ID}/")
    if req.status_code < 400:
        print(f"Last date set to transaction ID {transaction.ID} from {transaction.get_date().strftime(date_format)}")
    else:
        print("Could not set last date(second step).")
    
    return

def notify(args):
    if (NUMBERS := getenv("NUMBERS")) is None:
        raise EnvironmentError("No NUMBERS")
    else:
        NUMBERS = [int(number) for number in NUMBERS.split(",")]

    print("Checking FIO payments...")
    transactions, _ = fio_get_transactions()
    if transactions is None or len(transactions) == 0:
        print("No payment found.")
        return
    
    for transaction in transactions:
        string = ""
        if (title := getenv("TITLE")) is not None:
            string = f"{title}\n"
        else:
            print("No TITLE env variable set, skipping")
        string = string + f"{transaction.AccountName}\n"
        string = string + f"{transaction.Amount}{transaction.Currency}\n"

        foreign_amount = transaction.get_foreign_amount()
        if foreign_amount is not None:
            string = string + f"{foreign_amount.amount_text}{foreign_amount.currency}\n"

        if transaction.VS and int(transaction.VS) != 0:
            string = string + f"{transaction.VS}\n"

        if transaction.Message:
            string = string + f"{transaction.Message}"

        sms_send(NUMBERS, string)
        
