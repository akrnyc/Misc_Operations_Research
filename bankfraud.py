import pandas as pd
import random
import barnum
from datetime import datetime
from faker import Faker
fake = Faker()

#generate customers df
n_customers = 400
addresses = [barnum.create_city_state_zip() for x in range(n_customers)]

start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2022-09-01', '%Y-%m-%d')

customers = pd.DataFrame({'customer_id': random.sample(range(1000, 8000), n_customers),
                             'first_name': [fake.first_name() for x in range(n_customers)],
                             'last_name': [fake.last_name() for x in range(n_customers)],
                             'street': [fake.address().split('\n')[0] for x in range(n_customers)],
                             'city': [x[1] for x in addresses],
                             'state': [x[2] for x in addresses],
                             'zipcode': [int(x[0]) for x in addresses],
                             'country': 'US'
                             })

#generate account types df
account_types = pd.DataFrame({'id': ['A1','A2','A3'],
                              'type': ['Checking', 'Savings', 'Credit']
})

#generate accounts df
accounts = pd.DataFrame({'account_id': random.sample(range(1000, 8000), n_customers), 
                        'customer_id': customers.customer_id,
                        'account_type': [random.choice(account_types.id.to_list()) for x in range(n_customers)],
                        'account_active_at': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_customers)]
                        })

#generate transactions df
n_transactions = 2000
start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-11-21', '%Y-%m-%d')
transactions = pd.DataFrame({'id': random.sample(range(2000, 8000), n_transactions), 
                        'account_id': [random.choice(accounts.account_id.to_list()) for x in range(n_transactions)],
                        'service_date': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_transactions)],
                        'amount': [round(random.normalvariate(1000.0, 2000.0), 2) for x in range(n_transactions)]
                        })

#generate system logs df
n_sys = 5000
system_log = pd.DataFrame({'id': random.sample(range(2000, 8000), n_sys), 
                        'receive_time': [fake.date_time_between(start_date=start_date, end_date=end_date) for x in range(n_sys)],
                        'pings': [int(random.normalvariate(100.0, 20.0)) for x in range(n_sys)],
                        })

with pd.ExcelWriter('/Users/alex/Downloads/bankfraud.xlsx', engine='openpyxl') as writer:
    customers.to_excel(writer, sheet_name='customers')
    account_types.to_excel(writer, sheet_name='account_types')
    accounts.to_excel(writer, sheet_name='accounts')
    transactions.to_excel(writer, sheet_name='transactions')
    system_log.to_excel(writer, sheet_name='system_log')
