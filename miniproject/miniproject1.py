import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_sales_data(start_date='2024-01-01', periods=120, seed=42):
    np.random.seed(seed)
    date_index = pd.date_range(start_date, periods=periods, freq='D')
    regions = ['North', 'South', 'East', 'West']

    data = []
    for date in date_index:
        region = np.random.choice(regions, p=[0.25, 0.25, 0.25, 0.25])
        product_counts = {
            'Product_A': int(np.random.poisson(40) + 20),
            'Product_B': int(np.random.poisson(30) + 10),
            'Product_C': int(np.random.poisson(25) + 5),
        }
        base_prices = {'Product_A': 20.0, 'Product_B': 15.0, 'Product_C': 12.0}

        discount = np.round(np.random.choice([0.00, 0.05, 0.10, 0.15], p=[0.35, 0.35, 0.20, 0.10]), 2)
        cost_margin = {'Product_A': 0.55, 'Product_B': 0.50, 'Product_C': 0.45}

        for product, units in product_counts.items():
            price = base_prices[product]
            revenue = units * price * (1 - discount)
            unit_cost = price * cost_margin[product]
            cost = units * unit_cost
            profit = revenue - cost

            data.append(
                {
                    'Date': date,
                    'Region': region,
                    'Product': product,
                    'Units': units,
                    'Unit_Price': price,
                    'Discount': discount,
                    'Revenue': revenue,
                    'Cost': cost,
                    'Profit': profit,
                }
            )

    df = pd.DataFrame(data)
    return df


def process_sales_data(df):
    daily = df.groupby('Date').agg(
        total_units_sold=('Units', 'sum'),
        total_revenue=('Revenue', 'sum'),
        total_cost=('Cost', 'sum'),
        total_profit=('Profit', 'sum'),
    ).reset_index()

    daily['Profit_Margin'] = np.where(
        daily['total_revenue'] != 0,
        daily['total_profit'] / daily['total_revenue'] * 100,
        0,
    )

    daily['Month'] = daily['Date'].dt.month_name()
    daily['Day_of_Week'] = daily['Date'].dt.day_name()
    daily['Quarter'] = daily['Date'].dt.to_period('Q').astype(str)
    daily['Month_Number'] = daily['Date'].dt.month

    return daily


def aggregate_monthly(daily):
    monthly = (
        daily.groupby(['Month_Number', 'Month', 'Quarter'])
        .agg(
            monthly_units=('total_units_sold', 'sum'),
            monthly_revenue=('total_revenue', 'sum'),
            monthly_cost=('total_cost', 'sum'),
            monthly_profit=('total_profit', 'sum'),
        )
        .reset_index()
        .sort_values('Month_Number')
    )

    monthly['Profit_Margin'] = np.where(
        monthly['monthly_revenue'] != 0,
        monthly['monthly_profit'] / monthly['monthly_revenue'] * 100,
        0,
    )

    monthly['Revenue_Growth_%'] = monthly['monthly_revenue'].pct_change() * 100
    monthly['Profit_Growth_%'] = monthly['monthly_profit'].pct_change() * 100
    monthly['Unit_Growth_%'] = monthly['monthly_units'].pct_change() * 100

    return monthly


def compute_statistics(daily, monthly):
    stats = {
        'total_revenue': daily['total_revenue'].sum(),
        'average_daily_revenue': daily['total_revenue'].mean(),
        'revenue_std_dev': daily['total_revenue'].std(),
        'total_profit': daily['total_profit'].sum(),
        'average_daily_profit': daily['total_profit'].mean(),
        'profit_std_dev': daily['total_profit'].std(),
        'average_profit_margin': daily['Profit_Margin'].mean(),
    }
    return stats


def business_insights(monthly):
    best_month = monthly.loc[monthly['monthly_profit'].idxmax()]
    worst_month = monthly.loc[monthly['monthly_profit'].idxmin()]
    highest_growth = monthly.loc[monthly['Revenue_Growth_%'].idxmax()]

    trends = {
        'best_month': best_month,
        'worst_month': worst_month,
        'highest_growth_month': highest_growth,
        'monthly_trend': monthly[['Month', 'monthly_revenue', 'monthly_profit', 'Profit_Margin']].copy(),
    }
    return trends


def plot_dashboard(monthly):
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].bar(monthly['Month'], monthly['monthly_profit'], color='#4c72b0')
    axes[0, 0].set_title('Monthly Profit')
    axes[0, 0].set_ylabel('Profit ($)')
    axes[0, 0].tick_params(axis='x', rotation=45)

    axes[0, 1].plot(monthly['Month'], monthly['monthly_revenue'], marker='o', label='Revenue', color='#dd8452')
    axes[0, 1].plot(monthly['Month'], monthly['monthly_profit'], marker='o', label='Profit', color='#55a868')
    axes[0, 1].set_title('Revenue vs Profit Trend')
    axes[0, 1].set_ylabel('Amount ($)')
    axes[0, 1].legend()
    axes[0, 1].tick_params(axis='x', rotation=45)

    axes[1, 0].bar(monthly['Month'], monthly['Revenue_Growth_%'], color='#8172b3')
    axes[1, 0].set_title('Month-over-Month Revenue Growth')
    axes[1, 0].set_ylabel('Growth (%)')
    axes[1, 0].axhline(0, color='black', linewidth=0.8)
    axes[1, 0].tick_params(axis='x', rotation=45)

    axes[1, 1].plot(monthly['Month'], monthly['Profit_Margin'], marker='s', color='#8c564b')
    axes[1, 1].set_title('Monthly Profit Margin')
    axes[1, 1].set_ylabel('Margin (%)')
    axes[1, 1].tick_params(axis='x', rotation=45)

    for ax in axes.flat:
        ax.grid(alpha=0.2)

    fig.suptitle('Sales Analytics Dashboard', fontsize=18)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


def print_summary(stats, trends, monthly):
    print('\n' + '=' * 60)
    print('SALES ANALYTICS DASHBOARD SUMMARY')
    print('=' * 60)
    print(f"Total Revenue: ${stats['total_revenue']:,.2f}")
    print(f"Total Profit: ${stats['total_profit']:,.2f}")
    print(f"Average Daily Revenue: ${stats['average_daily_revenue']:,.2f}")
    print(f"Average Daily Profit: ${stats['average_daily_profit']:,.2f}")
    print(f"Revenue Std Dev: ${stats['revenue_std_dev']:,.2f}")
    print(f"Profit Std Dev: ${stats['profit_std_dev']:,.2f}")
    print(f"Average Profit Margin: {stats['average_profit_margin']:.2f}%")
    print('-' * 60)

    print('BEST PERFORMING MONTH:')
    print(f"  {trends['best_month']['Month']} ({trends['best_month']['Quarter']})")
    print(f"  Profit: ${trends['best_month']['monthly_profit']:,.2f}")
    print(f"  Revenue: ${trends['best_month']['monthly_revenue']:,.2f}")
    print(f"  Profit Margin: {trends['best_month']['Profit_Margin']:.2f}%")
    print('-' * 60)

    print('WORST PERFORMING MONTH:')
    print(f"  {trends['worst_month']['Month']} ({trends['worst_month']['Quarter']})")
    print(f"  Profit: ${trends['worst_month']['monthly_profit']:,.2f}")
    print(f"  Revenue: ${trends['worst_month']['monthly_revenue']:,.2f}")
    print(f"  Profit Margin: {trends['worst_month']['Profit_Margin']:.2f}%")
    print('-' * 60)

    print('HIGHEST MONTH-OVER-MONTH REVENUE GROWTH:')
    print(f"  {trends['highest_growth_month']['Month']} ({trends['highest_growth_month']['Quarter']})")
    print(f"  Growth: {trends['highest_growth_month']['Revenue_Growth_%']:.2f}%")
    print('-' * 60)

    print('KEY TRENDS:')
    if monthly['monthly_profit'].is_monotonic_increasing:
        print('  - Monthly profit shows a sustained upward trend.')
    else:
        print('  - Profit trends fluctuate across months, signaling variable performance.')

    if monthly['monthly_revenue'].iloc[-1] > monthly['monthly_revenue'].iloc[0]:
        print('  - Revenue improved over the observed period.')
    else:
        print('  - Revenue declined from the first to the last month.')

    print('  - The dashboard visualizes how profit margin and growth behave by month.')
    print('=' * 60)


def main():
    df_sales = generate_sales_data()
    daily = process_sales_data(df_sales)
    monthly = aggregate_monthly(daily)
    stats = compute_statistics(daily, monthly)
    trends = business_insights(monthly)

    print_summary(stats, trends, monthly)
    plot_dashboard(monthly)


if __name__ == '__main__':
    main()
