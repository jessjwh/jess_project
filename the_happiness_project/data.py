import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

file_path = r'/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'
happiness_report = pd.read_csv(file_path)

happiness_report.fillna(happiness_report.mean(numeric_only=True), inplace=True)

available_columns = happiness_report.columns
print(f"Available columns: {available_columns}")

all_columns = ['Life Ladder', 'Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy At Birth', 
               'Freedom To Make Life Choices', 'Generosity', 'Perceptions Of Corruption', 
               'Positive Affect', 'Negative Affect', 'Confidence In National Government']

features = all_columns[1:]  
target = 'Life Ladder'

features = [col for col in features if col in available_columns]

scaler = StandardScaler()
happiness_report[features] = scaler.fit_transform(happiness_report[features])

X = happiness_report[features]
y = happiness_report[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

lr_predictions = lr_model.predict(X_test)
rf_predictions = rf_model.predict(X_test)

lr_mse = mean_squared_error(y_test, lr_predictions)
rf_mse = mean_squared_error(y_test, rf_predictions)

lr_r2 = r2_score(y_test, lr_predictions)
rf_r2 = r2_score(y_test, rf_predictions)

print(f"Linear Regression - MSE: {lr_mse}, R²: {lr_r2}")
print(f"Random Forest - MSE: {rf_mse}, R²: {rf_r2}")

lr_feature_importance = pd.DataFrame({'Feature': features, 'Coefficient': lr_model.coef_})
rf_feature_importance = pd.DataFrame({'Feature': features, 'Importance': rf_model.feature_importances_})

plt.figure(figsize=(12, 10))
corr = happiness_report.select_dtypes(include=[float, int]).corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show(block=False)
plt.pause(1) 
input("Press Enter to continue...")

plt.figure(figsize=(10, 8))
sns.barplot(x='Feature', y='Coefficient', data=lr_feature_importance.sort_values(by='Coefficient', ascending=False))
plt.title("Linear Regression Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show(block=False)
plt.pause(1) 
input("Press Enter to continue...")

plt.figure(figsize=(10, 8))
sns.barplot(x='Feature', y='Importance', data=rf_feature_importance.sort_values(by='Importance', ascending=False))
plt.title("Random Forest Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show(block=False)
plt.pause(1)  
input("Press Enter to continue...")