#Step 1: Load the data
import pandas as pd
import os

script_folder = os.path.dirname(os.path.abspath(__file__))  #Ask Python: "where does this script file physically sit on my computer?"
csv_path = os.path.join(script_folder, "..", "data", "order_features.csv") # go up one level (..), then into data folder, then find the file order_features.csv

print("Looking for file at:", csv_path)

df = pd.read_csv(csv_path)

print(df.shape)
print(df.head())

#Step 2: EDA (Exploratory Data Analysis)
print()
print("Duplicate order IDs:", df['order_id'].duplicated().sum())
print("Missing product categories:", df['product_category'].isnull().sum())
print()
print("Bad review counts:")
print(df['bad_review'].value_counts())

#Step 3 — Feature Engineering 
print()
#dropping duplicate order IDs,446 duplicates 
df = df.drop_duplicates(subset=['order_id'])
print("Rows after dropping duplicate order IDs:", df.shape[0])

#filling missing categories, 1273
df['product_category'] = df['product_category'].fillna('Unknown')
print("Missing product categories remaining:", df['product_category'].isnull().sum())