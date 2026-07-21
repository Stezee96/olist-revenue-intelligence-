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
print(f"Bad review rate (train): {y_train.mean():.2%}") #removes the decimal and converts to percentage, 0.14 becomes 14%
print(f"Bad review rate (test):  {y_test.mean():.2%}")
print("Actual bad review rate in full dataset:", y.mean()) #just form eto confirm the numbers are right, should be 0.14 or 14%

#step 5: train the first model
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LogisticRegression(class_weight='balanced', max_iter=1000) #class_weight='balanced' tells the model to pay more attention to the minority class (bad reviews) during training, max_iter=1000 increases the number of iterations for convergence
model.fit(x_train_scaled, y_train) 

print("\n" + "="*40) #divider line for clarity in the console output
print("MODEL TRAINING RESULTS")
print("="*40) #mistake in the code, should be print("="*40) 
print("Model type:", type(model).__name__) #pprint name 

#Step 6: Evaluate the model on the test set
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(x_test_scaled) #model looks at the test set and predicts whether each order is a bad review or not, based on the features it learned during training. 0 or 1 for each order in the test set.
cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(f"{'':20} {'Predicted GOOD':>15} {'Predicted BAD':>15}") #ADDED HEADER FOR CLARITY OVER THE CONFUSION MATRIX
print(f"{'Actually GOOD':20} {cm[0,0]:>15} {cm[0,1]:>15}")
print(f"{'Actually BAD':20} {cm[1,0]:>15} {cm[1,1]:>15}")

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))

from sklearn.metrics import roc_auc_score

y_prob = model.predict_proba(x_test_scaled)[:, 1] #predict_proba returns the probability of each class (good or bad review)
auc = roc_auc_score(y_test, y_prob) #roc_auc_score calculates the area under the ROC curve
print(f"ROC AUC Score: {auc:.3f}")