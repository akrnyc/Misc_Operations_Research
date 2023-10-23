import pandas as pd
import random
import barnum
from datetime import datetime
from faker import Faker
fake = Faker()

#generate customers df
n_customers = 5000
addresses = [barnum.create_city_state_zip() for x in range(n_customers)]

start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-09-01', '%Y-%m-%d')

customers_us = pd.DataFrame({'customer_id': random.sample(range(10000, 80000), n_customers),
                             'first_name': [fake.first_name() for x in range(n_customers)],
                             'last_name': [fake.last_name() for x in range(n_customers)],
                             'street': [fake.address().split('\n')[0] for x in range(n_customers)],
                             'city': [x[1] for x in addresses],
                             'state': [x[2] for x in addresses],
                             'zipcode': [int(x[0]) for x in addresses],
                             'country': 'US',
                             'join_date': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_customers)]
                             })

customers_int = pd.DataFrame({'customer_id': random.sample(range(80001, 99999), n_customers),
                             'first_name': [fake.first_name() for x in range(n_customers)],
                             'last_name': [fake.last_name() for x in range(n_customers)],
                             'street': [fake.street_address().split('\n')[0] for x in range(n_customers)],
                             'city': [fake.city() for x in range(n_customers)],
                             'state': [fake.city() for x in range(n_customers)],
                             'zipcode': [fake.postcode() for x in range(n_customers)],
                             'country': [fake.country_code() for x in range(n_customers) if x != 'US'],
                             'join_date': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_customers)]
                             })

customers = pd.concat([customers_us, customers_int],
                      axis=0,
                      ignore_index=True)

#generate products df
combos = []
for category in ['phone', 'laptop', 'watch', 'tablet', 'headphones']:
    for style in ['matte', 'glossy', 'titanium', 'plastic']:
        combos.append((category, style))

n_products = len(combos)
catalogue = ['new_release', 'core_line', 'limited_edition']

products = pd.DataFrame({'product_id': [fake.passport_number() for x in range(n_products)],
                         'category': [x[0] for x in combos], 
                         'style': [x[1] for x in combos],
                         'catalog': random.choices(catalogue, weights=(.30, .50, .20), k=n_products),
                         'msrp': [round(random.normalvariate(300, 37), 1) for i in range(n_products)]
                         })

#generate marketing df
marketing = products[['catalog', 'category']].drop_duplicates(subset=['catalog', 'category']).copy(deep=True)
campaigns = ['keynote', 'influencer', 'backtoschool', 'blackfriday']
marketing['campaign'] = pd.Series(random.choices(campaigns, 
                                                weights=[0.10, 0.40, 0.30, 0.20], 
                                                k=len(marketing)), 
                                                index=marketing.index)
utm_sources = ['facebook', 'amazon', 'instagram', 'billboard', 'subway', 'referral']
marketing['utm_source'] = pd.Series(random.choices(utm_sources, 
                                                weights=[0.10, 0.5, 0.20, 0.080, 0.020, 0.10], 
                                                k=len(marketing)), 
                                                index=marketing.index)
diutm={
    'facebook': 'digital',
    'amazon': 'digital',
    'instagram': 'digital',
    'billboard': 'print',
    'subway': 'print',
    'referral': 'human'
}
marketing['utm_medium'] = marketing['utm_source'].map(diutm)
dispend = {
    'digital': 0.02,
    'print': 0.1,
    'human': 0.00
}
marketing['unit_spend'] =  marketing['utm_medium'].map(dispend)
marketing['impressions'] = [int(round(random.normalvariate(10000000, 7600), 0)) for x in range(marketing.shape[0])]
marketing.reset_index(drop=True, inplace=True)

#generate sales df
n_sales = 120000
statuses = ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Canceled', 'Returned']
couriers = ['DHL', 'Amazon', 'FedEx', 'UPS']
channels = ['retail', 'reseller', 'online']

sales = pd.DataFrame({'order_id': [fake.isbn13() for x in range(n_sales)],
                      'order_date': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_sales)],
                      'status': random.choices(statuses, weights=(0.050, 0.100, 0.300, 0.400, 0.050, 0.100), k=n_sales),
                      'courier': random.choices(couriers, weights=(0.10, 0.50, 0.20, 0.20), k=n_sales),
                      'sales_channel': random.choices(channels, weights=(0.30, 0.10, 0.60), k=n_sales),
                      'service_level': random.choices(['Standard', 'Expedited'], weights=(0.70, 0.30), k=n_sales),
                      'product_id': [random.choice(products.product_id.unique().tolist()) for x in range(n_sales)],
                      'quantity': random.choices(range(1, 4), k=n_sales),
                      'customer_id': [random.choice(customers.customer_id.unique().tolist()) for x in range(n_sales)]
                      })
