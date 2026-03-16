"""
Created on Wed Mar 11 22:54:44 2026
Created by Meesala Venkatesh
Data Analysis project-1
Project Title - Customer Intelligence & Revenue Optimization System

"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

os.makedirs(r"C:\Users\user\DA1project\python\charts", exist_ok=True) #created charts folder

df = pd.read_csv(r"C:\Users\user\DA1project\data\SampleSuperstore.csv",encoding='latin1')
print(df.head())
print(df.shape)

print(df.columns)

#Checking null values 
""" no null values """
print(df.isnull().sum())

#Cheking duplicates in dataset
""" no Duplicate rows """
print(df.duplicated().sum())

#Checking data types
print(df.dtypes)


#Convertig dates properly
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print(df.dtypes)
"Shows both order date, ship date in datetime64[ns]"

# converting to standard column names 
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
 
print(df.columns)

# Saving clean file
df.to_csv(r"C:\Users\user\DA1project\data\cleaned_superstore.csv",index=False)
print("Cleaned file saved successfully")

print(df.head())
print(df.shape)
print(df.dtypes)

df = pd.read_csv(r"C:\Users\user\DA1project\data\cleaned_superstore.csv")

print(df.columns)

df.columns = df.columns.str.replace('-', '_')

print(df.columns)

df.to_csv(r"C:\Users\user\DA1project\data\cleaned_superstore.csv",index=False)
print("Final cleaned file saved")

df = pd.read_csv(r"C:\Users\user\DA1project\data\cleaned_superstore.csv",
                 parse_dates=['order_date', 'ship_date'])

print (df.head()) #shows the first 5 rows of data)

print(df.shape) # shows the attributes count Rows * Columns (9994,21)
print(df.info()) # shows the datatypes
print(df.describe()) # shows the numeric summary

#EDA Analysis:
    
# Checking Missing values(NULL)
missing_values = df.isnull().sum()
if missing_values.sum() > 0:
    print("Null values exist")
    print(missing_values[missing_values > 0])
else:
    print("No null values exist")
# No Null values detected in dataset

# Outlier Detection
#Sales Outlier detection 
#Boxplot for Outliers
plt.boxplot(df['sales'])
plt.title("Sales Outlier Detection")
plt.savefig(r"C:\Users\user\DA1project\python\charts\sales_outlier_detection.png")
plt.show()
# detect outliers Numerically(IQR Method)
Q1 = df['sales'].quantile(0.25)
Q3 = df['sales'].quantile(0.75)
IQR = Q3 - Q1
sales_outliers = df[
    (df['sales'] < Q1 - 1.5 * IQR) |
    (df['sales'] > Q3 + 1.5 * IQR)]
if sales_outliers.shape[0] > 0:
    print("sales outliers exist")
    print("Number of outliers:", sales_outliers.shape[0])
else:
    print("No sales outliers found")
#print(sales_outliers.shape)
# Outliers retained because they may represent genuine high-value business transactions.
#Because in business datasets:
#not every outlier is bad.
#A huge sale may be a valid transaction.
#Large sales outliers exist, likely due to enterprise orders


#Profit Outlier detection
#Boxplot for Outliers
plt.boxplot(df['profit'])
plt.title("Profit Outlier Detection")
plt.savefig(r"C:\Users\user\DA1project\python\charts\profit_outlier_detection.png")
plt.show()
# detect outliers Numerically(IQR Method)
Q1 = df['profit'].quantile(0.25)
Q3 = df['profit'].quantile(0.75)
IQR = Q3 - Q1
profit_outliers = df[
    (df['profit'] < Q1 - 1.5 * IQR) |
    (df['profit'] > Q3 + 1.5 * IQR)]
if profit_outliers.shape[0] > 0:
    print("Profit outliers exist")
    print("Number of outliers:", profit_outliers.shape[0])
else:
    print("No profit outliers found")
# Profit outliers retained because they may represent valid high-value or loss-making transactions.

#---------------------------------------------------------------------------------------------------#

#Business analysis insights

# Top 10 Customers by Profit
top_customers = df.groupby('customer_name')['profit'].sum().sort_values(ascending=False).head(10)
print(top_customers)
top_customers.plot(kind='bar')
plt.title("Top 10 Customers by Profit")
plt.show()
#Insight:
#these 10 customers Dominate Profitability 

#Monthly sales Trend 
monthly_sales = df.groupby(df['order_date'].dt.month)['sales'].sum()
print(monthly_sales)
monthly_sales.plot(kind='line')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.savefig(r"C:\Users\user\DA1project\python\charts\monthly_sales.png")
plt.show()
#Insight:
# shows Revenue spikes during year-end months.


#Profit by Category
category_profit = df.groupby('category')['profit'].sum()
print(category_profit)
category_profit.plot(kind='bar')
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.savefig(r"C:\Users\user\DA1project\python\charts\category profit.png")
plt.show()
#Insight:
# Shows Technology Category has highest profitability.


#Region wise sales
region_sales = df.groupby('region')['sales'].sum()
print(region_sales)
region_sales.plot(kind='bar')
plt.title("Region Wise Sales")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.savefig(r"C:\Users\user\DA1project\python\charts\region_sales.png")
plt.show()
#Insight:
# Shows that West region leads in sales.


#Correlation Analysis (How Discount effects profits)
correlation = df[['sales','profit','discount']].corr()
print(correlation)
#Insight:
#Discount negatively correlates with profit


#Loss-Making Products(Which products hurt profitability?)
loss_products = df.groupby('product_name')['profit'].sum().sort_values().head(10)
print(loss_products)
loss_products.plot(kind='bar')
plt.title("Top 10 Loss Making Products")
plt.xlabel("Product Name")
plt.ylabel("Profit")
plt.savefig(r"C:\Users\user\DA1project\python\charts\loss_products.png")
plt.show()
# Insight:
# Certain products consistently generate losses and may require pricing review.

#Repeat Purchase Frequency + Profit by Customer (Which loyal customers actually generate value?)
#Top Repeat buyers
repeat_customers = df.groupby('customer_name').agg({
    'order_id':'count',
    'profit':'sum'
}).sort_values(by='order_id', ascending=False).head(10)
print(repeat_customers)
#Repeat frequency plotting
repeat_customers['order_id'].plot(kind='bar')
plt.title("Top Repeat Customers by Orders")
plt.xlabel("Customer Name")
plt.ylabel("Order Count")
plt.savefig(r"C:\Users\user\DA1project\python\charts\repeat_customers.png")
plt.show()
# Profit of Repeat customers
repeat_customers['profit'].plot(kind='bar')
plt.title("Profit from Top Repeat Customers")
plt.xlabel("Customer Name")
plt.ylabel("Profit")
plt.savefig(r"C:\Users\user\DA1project\python\charts\profit_repeat_customers.png")
plt.show()
# Insight:
# High purchase frequency does not always mean high profitability.
 

"""
This EDA Analyisis Covers
sales trend
profitability
loss analysis
customer loyalty
"""
#---------------RFM Customer Segmentation.------------------#
"""RFM means:
R = Recency → how recently customer purchased
F = Frequency → how often customer purchased
M = Monetary → how much customer spent

RFM helps identify:
-VIP customers
-Loyal customers
-At-risk customers
-Lost customers
"""
df = pd.read_csv(r"C:\Users\user\DA1project\data\cleaned_superstore.csv")

# Creation of RFM Table:
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

rfm = df.groupby('customer_name').agg({
    'order_date': 'max',
    'order_id': 'count',
    'sales': 'sum'
}).reset_index()
#Renaming Columns properly
rfm.columns = ['customer_name', 'last_order_date', 'frequency', 'monetary']
#Creating Recency
latest_date = df['order_date'].max()
rfm['recency'] = (latest_date - rfm['last_order_date']).dt.days
# Checking data types
print(rfm.dtypes)
# TO view RFM Table
print(rfm.head())
# Now I have recency,frequency, monetary

# scoring Recency customers 1-4 groups.
rfm['R_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1])
#Recet customers get higher score.

#Frequency score
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4])

#Monetary score
rfm['M_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4])
# getting Combine scores
rfm['RFM_score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)
print(rfm.head())

# segmenting customers
def segment_customer(row):
    if row['RFM_score'] == '444':
        return 'VIP'
    elif row['R_score'] >= 3:
        return 'Loyal'
    elif row['R_score'] <= 2:
        return 'At Risk'
    else:
        return 'Regular'
rfm['segment'] = rfm.apply(segment_customer, axis=1)

print(rfm[['R_score','F_score','M_score']].dtypes)
# Count segments
print(rfm['segment'].value_counts())

#Visualize segments in bar chart
rfm['segment'].value_counts().plot(kind='bar')
plt.title("Customer Segments")
plt.savefig(r"C:\Users\user\DA1project\python\charts\customer_segments.png")
plt.show()

rfm.to_csv(r"C:\Users\user\DA1project\data\customer_rfm_analysis.csv", index=False)


"""
Result :-

So I identified customer segments for business retention strategy.
Segment Distribution
At Risk → 396 customers
Loyal → 365 customers
VIP → 32 customers

Business Insights:
-> The largest customer group is At Risk, which means a significant portion of customers have not purchased recently and may require retention strategies.
-> Loyal customers form a strong repeat customer base and should be targeted with upsell campaigns.
-> VIP customers are very few but likely contribute disproportionately to revenue and profit.

Business Recommendation:
 ->> Retention campaigns should prioritize At Risk customers before churn increases.
"""


#---------------Sales Forecasting------------------#

#predicting next few months sales trend
#Monthly sales aggregation
monthly_sales = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
monthly_sales = monthly_sales.reset_index()
monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)
print(monthly_sales)

#Creating Numeric Month index
monthly_sales['month_index'] = range(1, len(monthly_sales)+1)

#Forecast using Linear regression
X = monthly_sales[['month_index']]
y = monthly_sales['sales']
model = LinearRegression()
model.fit(X, y) #train the regression model internally
"""learns the relationship between month and sales.
It calculates internally:
-slope
-intercept """
print("Slope:", model.coef_)
print("Intercept:", model.intercept_)
#positive slope -> sales increasing, negative slope -> sales decreasing

#predict next 3 months
future_months = pd.DataFrame({'month_index':[len(monthly_sales)+1,
                                             len(monthly_sales)+2,
                                             len(monthly_sales)+3]})
forecast = model.predict(future_months)
print(forecast)
# viusalizing the sales forecast
plt.plot(monthly_sales['month_index'], y)
plt.plot(future_months['month_index'], forecast)
plt.title("Sales Forecast")
plt.savefig(r"C:\Users\user\DA1project\python\charts\sales_forecast.png")
plt.show()


"""
Result:-

i have predicted next 3 months sales using Linear regression method 
month-1 -> 69,957
month-2 -> 70,859
month-3 -> 71,761

Insights:
- The forecast shows a gradual upward sales trend, indicating expected business growth in upcoming periods.

Business Interpretation: 

As forecast slope is positive
- Historical sales indicate stable growth despite fluctuations, suggesting sustained future revenue if current trends continue.

As blue line has high volatility, while forecast line is smoother
- Actual sales fluctuate heavily, but long-term trend remains positive.


Final prediction- Although historical monthly sales showed strong volatility, linear regression identified an overall positive trend in future revenue.
"""

