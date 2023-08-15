import argparse
import sys

from actions import *
from fio import test_connection as fio_test
from sms import test as sms_test

main_parser = argparse.ArgumentParser("FIO Notify", "Notifies about incoming payments on FIO Bank account via SMS.")
sub_parser = main_parser.add_subparsers()

fio_parser = sub_parser.add_parser("fio", help="Fio API related commands.")
fio_sub_parser = fio_parser.add_subparsers()

fio_test_parser = fio_sub_parser.add_parser("test", help="Test connection to API and token.")
fio_test_parser.set_defaults(func=lambda _: print("Fio API connection OK." if fio_test() else "Fio API connection NOT OK."))

fio_set_last_parser = fio_sub_parser.add_parser("set-last", help="Set last pull date")
fio_set_last_parser.add_argument("date_start", metavar="<YYYY-MM-DD>", type=str, help="Start date in YYYY-MM-DD format")
fio_set_last_parser.add_argument("date_end", metavar="<YYYY-MM-DD>", type=str, help="End date in YYYY-MM-DD format")
fio_set_last_parser.set_defaults(func= lambda args: fio_set_last(args))

sms_parser = sub_parser.add_parser("sms", help="SMS API related commands.")
sms_sub_parser = sms_parser.add_subparsers()

sms_test_parser = sms_sub_parser.add_parser("test", help="Test connection to API and token.")
sms_test_parser.set_defaults(func=lambda _: print("SMS API connection OK." if sms_test() else "SMS API connection NOT OK."))

notify_parser = sub_parser.add_parser("notify", help="Notification related commands.")
notify_parser.set_defaults(func= lambda args: notify(args))

if len(sys.argv) <= 1:
    main_parser.print_help()

args = main_parser.parse_args()
if "func" in args:
    args.func(args)
