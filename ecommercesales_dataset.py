import pandas as pd

march21data = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/pl_march_2021.csv', 
            usecols=['index', 'Sku', 'Style Id', 'Catalog', 'Category']
            ).rename(dict(zip(['index', 'Sku', 'Style Id', 'Catalog', 'Category'], 
                              ['index', 'sku', 'style_id', 'catalog', 'category'])), 
                              axis=1) #union base

may22data = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/may_2022.csv', 
            usecols=['index', 'Sku', 'Style Id', 'Catalog', 'Category']
            ).rename(dict(zip(['index', 'Sku', 'Style Id', 'Catalog', 'Category'], 
                              ['index', 'sku', 'style_id', 'catalog', 'category'])), 
                              axis=1) #union base

products = pd.concat([march21data, may22data], 
          axis=0, 
          ignore_index=True).drop_duplicates(subset='sku')

salesreport = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/sales_report.csv',
            usecols=['SKU Code', 'Design No.', 'Category', 'Size', 'Color']
            ).rename(dict(zip(['SKU Code', 'Design No.', 'Category', 'Size', 'Color'], 
                              ['sku', 'style_id', 'category', 'size', 'color'])), 
                              axis=1).dropna()

products[products['sku'].isin(salesreport['sku'].tolist())] #returns no matches

pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/amazon_sale_report.csv').columns

pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/international_sale_report.csv').columns
