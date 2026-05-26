import pandas as pd

def calc_remaining_lease(row):
    if pd.notna(row['remaining_lease']) and row['remaining_lease'] != 'NaN':
        return row['remaining_lease'] # preserve existing value
    
    sale_year, sale_month = [int(x) for x in row['month'].split('-')]
    lease_start = int(row['lease_commence_date'])

    elapsed_months = (sale_year - lease_start) * 12 + sale_month
    remaining_months_total = (99 * 12) - elapsed_months

    remaining_years = min(remaining_months_total // 12, 99) # cap at 99
    remaining_months = remaining_months_total % 12 if remaining_years < 99 else 0

    return f"{remaining_years} years {remaining_months:02d} months"

