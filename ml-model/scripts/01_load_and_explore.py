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

#step 3: encoding the text columns into numbers
df['different_state'] = (df['customer_state'] != df['seller_state']).astype(int) # Comparing the state columns and producing t or f
print()
print("Orders shipped across states:", df['different_state'].sum())

#text to number
df_encoded = pd.get_dummies(df, columns=['product_category', 'customer_state', 'seller_state'], drop_first=True) #drop_first avoids dummy varriable 
print()
print("Shape before endoding:", df.shape)
print("Shape after encoding:", df_encoded.shape)

#Splitting into features (x) and target (y)
X = df_encoded.drop(columns=['order_id', 'bad_review']) 
y = df_encoded['bad_review']

print ()
print("Features shape (X):", X.shape)
print("Target shape (y):", y.shape)

output_path = os.path.join(script_folder, "..", "data", "processed_features.csv")
df_encoded.to_csv(output_path, index=False)
print("Saved processed data to:", output_path)