#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import joblib
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')


# In[4]:


car_dataset = pd.read_csv('car_data_sl.csv')


# In[5]:


car_dataset.head()


# In[6]:


car_dataset.shape


# In[7]:


car_dataset.info


# In[8]:


car_dataset.isnull().sum()


# In[9]:


car_dataset.describe()


# In[10]:


print('\nFuel Type:')
print(car_dataset['Fuel_Type'].value_counts())
print('\nSeller Type:')
print(car_dataset['Seller_Type'].value_counts())
print('\nTransmission:')
print(car_dataset['Transmission'].value_counts())
print('\nOwner:')
print(car_dataset['Owner'].value_counts())


# In[11]:


plt.figure(figsize=(10, 6))
plt.hist(car_dataset['Selling_Price'], bins=30, color='#3498db', edgecolor='black')
plt.title('Distribution of Car Selling Prices', fontsize=14, fontweight='bold')


# In[12]:


plt.figure(figsize=(10 , 8))
numeric_data = car_dataset.select_dtypes(include=[np.number])
correlation = numeric_data.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, square=True, linewidths=1, fmt='.2f')
plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)


# In[13]:


#Fuel type vs Selling Price
plt.figure(figsize=(12, 5))
plt.subplot(1,2,1)
sns.boxplot(x='Fuel_Type', y='Selling_Price', data=car_dataset, palette='Set2')
plt.title('Fuel Type vs Selling Price', fontweight='bold')
plt.xlabel('Fuel type')
plt.ylabel('Selling Price (Lakhs)')


# In[14]:


#Transmission vs Selling Price
plt.subplot(1,2,2)
sns.boxplot(x='Transmission', y='Selling_Price',data=car_dataset, palette='Set1')
plt.title('Transmission vs Selling Price', fontweight='bold')
plt.xlabel('Transmission')
plt.ylabel('Sellling Price (Lakhs)')
plt.show()


# In[15]:


#Year vs Selling Price
plt.figure(figsize=(10,6))
plt.scatter(car_dataset['Year'], car_dataset['Selling_Price'], alpha=0.6, c='#e74c3c')
plt.title('Car Year vs Selling Price', fontsize=14, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Selling Price (Lakhs)')
plt.show()


# In[16]:


#Kms driven vs Selling Price

plt.figure(figsize=(10,6))
plt.scatter(car_dataset['Kms_Driven'], car_dataset['Selling_Price'], alpha=0.6, c='#9b59b6')
plt.title('Kilometers Driven vs Selling Price',fontsize=14, fontweight='bold')
plt.xlabel('Kilometers Driven')
plt.ylabel('Selling Price(Lakhs)')
plt.show()


# In[17]:


#Encoding 

car_dataset.replace({'Fuel_Type':{'Petrol':0, 'Diesel':1, 'CNG':2}}, inplace=True)
car_dataset.replace({'Seller_Type': {'Dealer':0, 'Individual':1}}, inplace= True)
car_dataset.replace({'Transmission': {'Manual':0, 'Automatic':1}}, inplace=True)

print("Encoded Dataset")
car_dataset.head()


# In[18]:


x = car_dataset.drop(['Car_Name', 'Selling_Price'], axis=1)


# In[19]:


x = car_dataset.drop(['Car_Name', 'Selling_Price'], axis=1)
y=car_dataset['Selling_Price']

print(x.head)


# In[20]:


print(y.head())


# In[21]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)
print(f'Training Sample: {x_train.shape[0]} (80%)')


# In[22]:


print(f'Testing Sample: {x_test.shape[0]} (20%)')


# In[23]:


#Model 1 Linear Regression

lin_reg = LinearRegression()
lin_reg.fit(x_train, y_train)

train_pred_lr = lin_reg.predict(x_train)
train_r2_lr = metrics.r2_score(y_train, train_pred_lr)
train_mae_lr = metrics.mean_absolute_error(y_train, train_pred_lr)
train_rmse_lr = np.sqrt(metrics.mean_squared_error(y_train, train_pred_lr))

print('r2 score', train_r2_lr)
print('mae', train_mae_lr)
print('rmse', train_rmse_lr)


# In[26]:


test_pred_lr = lin_reg.predict(x_test)
test_r2_lr = metrics.r2_score(y_test, test_pred_lr)
test_mae_lr = metrics.mean_absolute_error(y_test, test_pred_lr)
test_rmse_lr = np.sqrt(metrics.mean_squared_error(y_test, test_pred_lr))

print('r2 score', test_r2_lr)
print('mae', test_mae_lr)
print('rmse',test_rmse_lr)


# In[27]:


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(y_train, train_pred_lr, alpha=0.6, color='#2498db')
axes[0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Price')
axes[0].set_ylabel('Predicted Price')
axes[0].set_title('Linear Regression - Training')

axes[1].scatter(y_test, test_pred_lr, alpha=0.6, color='#2498db')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Price')
axes[1].set_ylabel('Predicted Price')
axes[1].set_title('Linear Regression - Testing')


# In[28]:


#Model 2 Lasso regresion

lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(x_train, y_train)

train_pred_lasso = lasso_reg.predict(x_train)
train_r2_score = metrics.r2_score(y_train, train_pred_lasso)
train_mae_lasso = metrics.mean_absolute_error(y_train, train_pred_lasso)
train_rmse_lasso = np.sqrt(metrics.mean_squared_error(y_train, train_pred_lasso))

print('r2 score', train_r2_score)
print('mae', train_mae_lasso)
print('rmse',train_rmse_lasso)


# In[29]:


test_pred_lasso = lasso_reg.predict(x_test)
test_r2_score = metrics.r2_score(y_test, test_pred_lasso)
test_mae_lasso = metrics.mean_absolute_error(y_test, test_pred_lasso)
test_rmse_lasso = np.sqrt(metrics.mean_squared_error(y_test, test_pred_lasso))

print('r2 score', test_r2_score)
print('mae', test_mae_lasso)
print('rmse',test_rmse_lasso)


# In[30]:


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(y_train, train_pred_lasso, alpha=0.6, color='#2498db')
axes[0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Price')
axes[0].set_ylabel('Predicted Price')
axes[0].set_title('Lasso Regression - Training')

axes[1].scatter(y_test, test_pred_lasso, alpha=0.6, color='#2498db')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Price')
axes[1].set_ylabel('Predicted Price')
axes[1].set_title('Lasso Regression - Testing')


# In[31]:


#model 3 Random Forest
rf_reg = RandomForestRegressor(n_estimators=100, random_state=2)
rf_reg.fit(x_train, y_train)

train_pred_rf = rf_reg.predict(x_train)
train_r2_rf = metrics.r2_score(y_train, train_pred_rf)
train_mae_rf = metrics.mean_absolute_error(y_train, train_pred_rf)
train_rmse_rf = np.sqrt(metrics.mean_squared_error(y_train, train_pred_rf))

print('r2 score', train_r2_rf)
print('mae', train_mae_rf)
print('rmse', train_rmse_rf)


# In[32]:


test_pred_rf = rf_reg.predict(x_test)
test_r2_rf = metrics.r2_score(y_test, test_pred_rf)
test_mae_rf = metrics.mean_absolute_error(y_test, test_pred_rf)
test_rmse_rf = np.sqrt(metrics.mean_squared_error(y_test, test_pred_rf))

print('r2 score', test_r2_rf)
print('mae', test_mae_rf)
print('rmse', test_rmse_rf)


# In[33]:


feature_importance = pd.DataFrame({
    'Feature': x.columns,
    'Importance': rf_reg.feature_importances_
}).sort_values('Importance', ascending=False)

print(feature_importance)


# In[34]:


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(y_train, train_pred_rf, alpha=0.6, color='#2498db')
axes[0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Price')
axes[0].set_ylabel('Predicted Price')
axes[0].set_title('Random Forest - Training')

axes[1].scatter(y_test, test_pred_rf, alpha=0.6, color='#2498db')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Price')
axes[1].set_ylabel('Predicted Price')


# In[35]:


plt.figure(figsize=(10,6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'], color ='#3498db')
plt.xlabel('Importnace')
plt.title('Feature Importance - random forest', fontsize=14, fontweight='bold')
plt.show()


# In[36]:


#Model Comparison

print('Linear Regression', test_r2_lr)
print('Lasso Regression',test_r2_score)
print('Random Forest', test_r2_rf)


# In[37]:


#Save Best Model
joblib.dump(rf_reg, 'car_prediction_model_sl.pkl')


# In[38]:


input_data = pd.DataFrame({
    'Year': [2015],
    'Present_Price': [7.0],
    'Kms_Driven': [50000],
    'Fuel_Type':[0],
    'Seller_Type':[1],
    'Transmission': [0],
    'Owner': [1]
})

prediction = rf_reg.predict(input_data)[0]
print(prediction)

