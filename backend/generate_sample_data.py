import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data(rows=200):
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Toys']
    regions = ['North', 'South', 'East', 'West']
    products = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Monitor'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers'],
        'Home & Garden': ['Plant', 'Chair', 'Lamp', 'Table'],
        'Books': ['Novel', 'Textbook', 'Comic', 'Biography'],
        'Toys': ['Lego', 'Doll', 'Action Figure', 'Puzzle']
    }

    data = []
    start_date = datetime(2024, 1, 1)

    for i in range(rows):
        cat = random.choice(categories)
        prod = random.choice(products[cat])
        reg = random.choice(regions)
        
        # Date with some trend (more sales in later months)
        date = start_date + timedelta(days=random.randint(0, 365))
        
        # Sales amount correlates with category
        base_price = 0
        if cat == 'Electronics': base_price = random.uniform(200, 2000)
        elif cat == 'Clothing': base_price = random.uniform(20, 200)
        elif cat == 'Home & Garden': base_price = random.uniform(50, 500)
        elif cat == 'Books': base_price = random.uniform(10, 50)
        else: base_price = random.uniform(15, 100)
        
        units = random.randint(1, 10)
        total_sales = round(base_price * units, 2)
        profit_margin = random.uniform(0.1, 0.4)
        profit = round(total_sales * profit_margin, 2)
        
        customer_rating = random.randint(1, 5)

        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": cat,
            "Product": prod,
            "Region": reg,
            "Units_Sold": units,
            "Sales_Amount": total_sales,
            "Profit": profit,
            "Rating": customer_rating
        })

    df = pd.DataFrame(data)
    # create outliers
    df.loc[0, 'Sales_Amount'] = df['Sales_Amount'].max() * 3
    
    return df

if __name__ == "__main__":
    df = generate_data(300)
    output_path = "../sample_sales_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Sample data generated at: {output_path}")
