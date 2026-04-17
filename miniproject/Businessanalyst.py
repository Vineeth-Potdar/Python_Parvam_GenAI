import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import calendar

# ==========================================
# 0. Generate Synthetic Dataset
# ==========================================
np.random.seed(42)
days = 365
dates = pd.date_range(start='2025-01-01', periods=days, freq='D')

products = {
    'Product_A': {'price': 100, 'cost': 60},
    'Product_B': {'price': 150, 'cost': 90},
    'Product_C': {'price': 200, 'cost': 130}
}

product_choices = np.random.choice(list(products.keys()), days)
prices = [products[p]['price'] for p in product_choices]
costs = [products[p]['cost'] for p in product_choices]

df = pd.DataFrame({
    'Date': dates,
    'Product': product_choices,
    'Region': np.random.choice(['North', 'South', 'East', 'West'], days),
    'Units_Sold': np.random.randint(20, 150, days),
    'Unit_Price': prices,
    'Unit_Cost': costs,
    'Discount_Pct': np.random.uniform(0.0, 0.25, days)
})

# ==========================================
# 1. Data Processing
# ==========================================
df['Gross_Revenue'] = df['Units_Sold'] * df['Unit_Price']
df['Discount_Amount'] = df['Gross_Revenue'] * df['Discount_Pct']
df['Net_Revenue'] = df['Gross_Revenue'] - df['Discount_Amount']

df['Total_Cost'] = df['Units_Sold'] * df['Unit_Cost']
df['Profit'] = df['Net_Revenue'] - df['Total_Cost']

# ==========================================
# 2. Time-Based Analysis
# ==========================================
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

monthly_agg = df.groupby(['Month', 'Month_Name']).agg(
    Total_Units=('Units_Sold', 'sum'),
    Total_Revenue=('Net_Revenue', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()

# ==========================================
# 3. Statistical Analysis & Insights
# ==========================================
# Month-over-Month (MoM) Growth
monthly_agg['MoM_Revenue_Growth_%'] = monthly_agg['Total_Revenue'].pct_change() * 100

stats = {
    'Total_Revenue': df['Net_Revenue'].sum(),
    'Total_Profit': df['Profit'].sum(),
    'Overall_Margin': (df['Profit'].sum() / df['Net_Revenue'].sum()) * 100
}

best_month = monthly_agg.loc[monthly_agg['Total_Profit'].idxmax()]
worst_month = monthly_agg.loc[monthly_agg['Total_Profit'].idxmin()]
highest_growth_month = monthly_agg.loc[monthly_agg['MoM_Revenue_Growth_%'].idxmax()]

# ==========================================
# 4. Data Visualization: MATPLOTLIB
# ==========================================
print("Generating Matplotlib Static Charts...")

plt.style.use('ggplot')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Matplotlib: Profit and Growth Analysis', fontsize=16, fontweight='bold')

# Plot 1: Monthly Profit (Bar Chart)
bars = ax1.bar(monthly_agg['Month_Name'], monthly_agg['Total_Profit'], color='#2ca02c')
ax1.set_title('Monthly Profit Generation')
ax1.set_ylabel('Profit ($)')
best_idx = monthly_agg['Total_Profit'].idxmax()
bars[best_idx].set_color('#1f77b4') # Highlight best month

# Plot 2: Month-over-Month Growth (Bar)
colors = ['red' if x < 0 else 'green' for x in monthly_agg['MoM_Revenue_Growth_%']]
ax2.bar(monthly_agg['Month_Name'], monthly_agg['MoM_Revenue_Growth_%'], color=colors)
ax2.axhline(0, color='black', linewidth=1)
ax2.set_title('Month-over-Month Revenue Growth (%)')
ax2.set_ylabel('Growth (%)')

plt.tight_layout()
plt.show()

# ==========================================
# 5. Data Visualization: PLOTLY
# ==========================================
print("Generating Plotly Interactive Dashboards...")

# Plot 3: Interactive Revenue & Profit Trend (Line Chart)
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=monthly_agg['Month_Name'], y=monthly_agg['Total_Revenue'], 
                               mode='lines+markers', name='Revenue', line=dict(color='#1f77b4', width=3)))
fig_trend.add_trace(go.Scatter(x=monthly_agg['Month_Name'], y=monthly_agg['Total_Profit'], 
                               mode='lines+markers', name='Profit', line=dict(color='#2ca02c', width=3)))

fig_trend.update_layout(title='Interactive Revenue & Profit Trends', 
                        xaxis_title='Month', yaxis_title='Amount ($)', 
                        hovermode='x unified', template='plotly_white')
fig_trend.show()

# Plot 4: Interactive Product Share (Pie Chart)
product_sales = df.groupby('Product')['Net_Revenue'].sum().reset_index()
fig_pie = px.pie(product_sales, names='Product', values='Net_Revenue', 
                 title='Interactive Revenue Share by Product',
                 color_discrete_sequence=['#ff7f0e', '#1f77b4', '#2ca02c'], hole=0.3)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.show()

# ==========================================
# 6. Structured Terminal Report
# ==========================================
print("\n" + "="*50)
print(" 📊 EXECUTIVE SALES ANALYTICS SUMMARY ")
print("="*50)
print(f"Total Annual Revenue:   ${stats['Total_Revenue']:,.2f}")
print(f"Total Annual Profit:    ${stats['Total_Profit']:,.2f}")
print(f"Overall Profit Margin:  {stats['Overall_Margin']:.2f}%")
print(f"\n🏆 Best Performing Month: {best_month['Month_Name']} (Profit: ${best_month['Total_Profit']:,.2f})")
print(f"⚠️ Worst Performing Month: {worst_month['Month_Name']} (Profit: ${worst_month['Total_Profit']:,.2f})")
print(f"🚀 Highest MoM Growth:    {highest_growth_month['Month_Name']} at {highest_growth_month['MoM_Revenue_Growth_%']:.1f}%")
print("="*50)