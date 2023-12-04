import pandas as pd
import random
import barnum
from datetime import timedelta
from datetime import datetime
from faker import Faker
fake = Faker()

#generate customers df
n_customers = 2000
addresses = [barnum.create_city_state_zip() for x in range(n_customers)]

start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2022-12-01', '%Y-%m-%d')

customers = pd.DataFrame({'customer_id': random.sample(range(1000, 3000), n_customers),
                             'first_name': [fake.first_name() for x in range(n_customers)],
                             'last_name': [fake.last_name() for x in range(n_customers)],
                             'street': [fake.address().split('\n')[0] for x in range(n_customers)],
                             'city': [x[1] for x in addresses],
                             'state': [x[2] for x in addresses],
                             'zipcode': [int(x[0]) for x in addresses],
                             'country': 'US',
                             'join_date': [fake.date_between(start_date=start_date, end_date=end_date) for x in range(n_customers)]
                             })

#generate medical history df
c_ids = customers.customer_id.to_list()
medical_history = pd.DataFrame({'customer_id': c_ids,
                                'age': [random.randint(40, 80) for x in range(len(c_ids))],
                                'height_inches': [round(random.normalvariate(67.0, 2.5), 1) for x in range(len(c_ids))],
                                'initial_weight': [round(random.normalvariate(190, 35), 2) for x in range(len(c_ids))],
                                'current_weight': [round(random.normalvariate(190, 50), 2) for x in range(len(c_ids))],
                                'diabetic_risk': [bool(random.getrandbits(1)) for x in range(len(c_ids))],
                                'cardiac_risk': [bool(random.getrandbits(1)) for x in range(len(c_ids))],
                                'insurance_coverage': random.choices(['None', 'Full', 'Partial'], weights=(0.30, 0.50, 0.20), k=len(c_ids))
                             })

#generate products df
products = pd.DataFrame({'product_id': [fake.passport_number() for x in range(2)],
                         'category': ['scale', 'meal_kit'],
                         'shipping_frequency': ['one_time', 'weekly'],
                         'shipping_cost': [19.99, 8.99],
                         'production_cost': [50.00, 12.00],
                         'billable_price': [130.00, 26.00]
                         })

#generate marketing df
combos = []
p_ids = products['product_id'].to_list()
campaigns = ['insurance', 'wellness_check']
utm_sources = ['facebook', 'amazon', 'instagram', 'billboard', 'subway', 'referral']

for p in p_ids:
    for c in campaigns:
        for u in utm_sources:
            combos.append((p,c,u))

marketing = pd.DataFrame({'product_id': [x[0] for x in combos],
                          'campaign': [x[1] for x in combos],
                          'utm_source': [x[2] for x in combos]

})

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
marketing['impressions'] = [int(round(random.normalvariate(100000, 70), 0)) for x in range(marketing.shape[0])]
marketing = marketing.reset_index(drop=True)

#generate sales df
n_sales = 12000
statuses = ['Delivered', 'Canceled', 'Returned']
couriers = ['Amazon', 'FedEx', 'UPS']

p_id = products[products['category'] == 'scale']['product_id'].values[0]
sales_scales = pd.DataFrame({'order_id': [fake.isbn13() for x in range(len(c_ids))],
                      'status': random.choices(statuses, weights=(0.800, 0.150, 0.050), k=len(c_ids)),
                      'courier': random.choices(couriers, weights=(0.50, 0.20, 0.30), k=len(c_ids)),
                      'service_level': random.choices(['Standard', 'Expedited'], weights=(0.30, 0.70), k=len(c_ids)),
                      'product_id': [p_id for x in range(len(c_ids))],
                      'quantity': [1 for x in range(len(c_ids))],
                      'customer_id': c_ids
                      })
sales_scales['order_date'] = [(customers[customers['customer_id'] == x]['join_date'].values[0] + timedelta(days=random.randint(1, 5))) for x in sales_scales['customer_id'].to_list()]
sales_scales['ship_date'] = [x + timedelta(days=random.randint(1, 9)) for x in sales_scales['order_date'].to_list()]

c_ids = sales_scales[sales_scales['status'] == 'Delivered']['customer_id'].to_list()
p_id = products[products['category'] == 'meal_kit']['product_id'].values[0]
sales_mealkits = pd.DataFrame({'order_id': [fake.isbn13() for x in range(len(c_ids))],
                      'status': random.choices(statuses, weights=(0.950, 0.050, 0.000), k=len(c_ids)),
                      'courier': random.choices(couriers, weights=(0.50, 0.20, 0.30), k=len(c_ids)),
                      'product_id': [p_id for x in range(len(c_ids))],
                      'quantity': [random.randint(1, 3) for x in range(len(c_ids))],
                      'customer_id': c_ids
                      })
sales_mealkits['order_date'] = [(customers[customers['customer_id'] == x]['join_date'].values[0] + timedelta(days=random.randint(5, 10))) for x in sales_mealkits['customer_id'].to_list()]
sales_mealkits['ship_date'] = [x + timedelta(days=random.randint(1, 5)) for x in sales_mealkits['order_date'].to_list()]

#recurring orders
while sales_mealkits.shape[0] < n_sales:
    sales_more_mealkits = pd.DataFrame({'order_id': [fake.isbn13() for x in range(len(c_ids))],
                        'status': random.choices(statuses, weights=(0.950, 0.050, 0.000), k=len(c_ids)),
                        'courier': random.choices(couriers, weights=(0.50, 0.20, 0.30), k=len(c_ids)),
                        'product_id': [p_id for x in range(len(c_ids))],
                        'quantity': [random.randint(1, 2) for x in range(len(c_ids))],
                        'customer_id': c_ids
                        })
    sales_more_mealkits['order_date'] = [(sales_mealkits[sales_mealkits['customer_id'] == x]['ship_date'].max() + timedelta(days=random.randint(3, 12))) for x in sales_more_mealkits['customer_id'].to_list()]
    sales_more_mealkits['ship_date'] = [x + timedelta(days=random.randint(1, 7)) for x in sales_more_mealkits['order_date'].to_list()]
    sales_mealkits = pd.concat([sales_mealkits, sales_more_mealkits], axis=0, ignore_index=True)


sales = pd.concat([sales_scales, sales_mealkits], axis=0, ignore_index=True)

with pd.ExcelWriter('/Users/alex/Downloads/weightlossservice.xlsx', engine='openpyxl') as writer:
    customers.to_excel(writer, sheet_name='customers')
    medical_history.to_excel(writer, sheet_name='medical_history')
    marketing.to_excel(writer, sheet_name='marketing')
    products.to_excel(writer, sheet_name='products')
    sales.to_excel(writer, sheet_name='sales')
