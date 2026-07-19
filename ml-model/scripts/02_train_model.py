#step 4-5 handing imbalance and training the model 
import pandas as pd
import os
from sklearn.model_selection import train_test_split 

script_folder = os.path.dirname(os.path.abspath(__file__))  #Ask Python: "where does this script file physically sit on my computer?"
csv_path = os.path.join(script_folder, "..", "data", "processed_features.csv") 

df = pd.read_csv(csv_path)

x = df.drop(columns=['order_id', 'bad_review'])
y = df['bad_review']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y) # splits data into training and test sets, stratify=y ensures that the proportion of classes in the target variable is maintained in both training and test sets
#test_size=0.2 hold back 20% for testing and 80% for training
#random_state=42 (Hitchhiker's Guide to the Galaxy) locks in a specific random split so its reporducible
# stratify=y forces both the train and test piles to keep the same 14% bad-review ratio as the full dataset. Without this, random chance could accidentally dump most bad reviews into one pile, skewing everything.
print("\n" + "="*40)
print("TRAIN/TEST SPLIT RESULTS")
print("="*40)
print(f"Training set size: {x_train.shape}")
print(f"Test set size: {x_test.shape}")
print(f"Bad review rate (train): {y_train.mean():.2%}")
print(f"Bad review rate (test):  {y_test.mean():.2%}")
print("Actual bad review rate in full dataset:", y.mean()) #just fo rm eto confirm the numbers are right, should be 0.14 or 14%
