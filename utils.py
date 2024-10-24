from datetime import timedelta

def calculate_growth(current, previous):
    return ((current / previous) - 1) * 100 if previous != 0 else float('inf')

def calculate_metrics_with_growth(df, days):
    end_date = df['day'].max()
    start_date = end_date - timedelta(days=days-1)
    period_df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
    
    previous_start = start_date - timedelta(days=days)
    previous_df = df[(df['day'] >= previous_start) & (df['day'] < start_date)]
    
    metrics = {}
    for metric in ['spend', 'revenue', 'profit', 'net_profit']:
        current_value = period_df[metric].sum()
        previous_value = previous_df[metric].sum()
        
        growth = calculate_growth(current_value, previous_value)
        
        metrics[f'{metric}_{days}d'] = current_value
        metrics[f'{metric}_{days}d_growth'] = growth
    
    return metrics
