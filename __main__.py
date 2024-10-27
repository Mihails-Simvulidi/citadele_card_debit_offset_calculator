import csv
import holidays
import numpy
import sys
from datetime import datetime

if __name__ == "__main__":
    lv_holidays = [
        str(holiday)
        for holiday in holidays.country_holidays("Latvia", years=range(2023, 2025))
    ]

    min_calendar_days = max_calendar_days = min_business_days = max_business_days = None

    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        for row in csv_reader:
            if len(row) == 7 and row[2] == "PIRKUMS":
                debit_date = datetime.strptime(row[1], "%d.%m.%y").date()
                transaction_date = datetime.strptime(
                    row[3].split(" ")[0], "%d/%m/%Y"
                ).date()

                calendar_days = (debit_date - transaction_date).days
                if min_calendar_days is None or min_calendar_days > calendar_days:
                    min_calendar_days = calendar_days
                if max_calendar_days is None or max_calendar_days < calendar_days:
                    max_calendar_days = calendar_days

                business_days = int(
                    numpy.busday_count(
                        str(transaction_date), str(debit_date), holidays=lv_holidays
                    )
                )
                if min_business_days is None or min_business_days > business_days:
                    min_business_days = business_days
                if max_business_days is None or max_business_days < business_days:
                    max_business_days = business_days

    print(
        f"{min_calendar_days=} {max_calendar_days=} {min_business_days=} {max_business_days=}"
    )
