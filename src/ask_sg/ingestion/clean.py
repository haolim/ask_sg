# TODO(deferred):
# 1. df.apply(calc_remaining_lease, axis=1) is row-by-row Python — slow
#    on large data. Acceptable for a one-time ingestion script.
#    Fix: vectorise using pandas column arithmetic if speed becomes an issue.

# HDB Data:
#   1. No remaining lease in 1990-2014 data.
#   2. Remaining lease in 2015-2016 data does not have 'years' and 'months' text as in 2017+ data.
#   3. The CSV file cover separate date ranged with no overlap (checked in Oct 2026). Only one file should be loaded for each date range.
#   2017+ file is currently in data/raw.

import pandas as pd
import glob
import logging
from pathlib import Path
from ask_sg.ingestion.calculate_remaining_lease import calc_remaining_lease


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def load_csvs(data_dir: str) -> pd.DataFrame:
    files = glob.glob(str(Path(data_dir) / "*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in: {data_dir}")
    
    logger.info(f"Loading {len(files)} file(s) from {data_dir}")

    return pd.concat(
        (pd.read_csv(f) for f in files), ignore_index=True
    )

def validate_month_format(df: pd.DataFrame) -> None:
    # create a mask of rows where the month format is invalid, and if any such rows exist, raise an error.
    invalid_mask = ~df['month'].str.match(r'^\d{4}-\d{2}$')
    if invalid_mask.any():
        invalid = df.loc[invalid_mask, 'month'].unique()
        raise ValueError(f"Invalid month format found: {invalid}")

def split_month(df: pd.DataFrame) -> pd.DataFrame:
    df[['sold_year', 'sold_month']] = (
        df['month'].str.split('-', expand=True).astype(int)
    )

    return df.drop(columns=['month'])

def split_remaining_lease(df: pd.DataFrame) -> pd.DataFrame:
    pattern = r'(?P<remaining_lease_year>\d+)\s+years?\s*(?:(?P<remaining_lease_month>\d+)\s*months?)?'
    lease = df['remaining_lease'].str.extract(pattern)

    na_rows = lease['remaining_lease_year'].isna()
    if na_rows.any():
        number_only = ( # Column data is provided as '79' and '79 years 6 months', this takes care of those data that only contain a number.
            df.loc[na_rows, 'remaining_lease'] # select only the rows where extraction failed, from the remaining_lease column
            .apply(lambda x: str(int(x)) if pd.notna(x) else None) # for each value x in those rows: if it's not null (pd.notna(x)),
                                                                    # convert it to an integer then back to a string (this handles values like 61.0 becoming "61"). If it is null, return None.
            .str.extract(r'(?P<remaining_lease_year>^\d+$)')
        )
        lease.loc[na_rows, 'remaining_lease_year'] = number_only['remaining_lease_year'] # fill in the gaps in the lease DataFrame with the numbers we just extracted.

    df['remaining_lease_year'] = lease['remaining_lease_year'].astype('Int64')
    df['remaining_lease_month'] = lease['remaining_lease_month'].astype('Int64')

    df['remaining_lease_month'] = df['remaining_lease_month'].fillna(0)

    failed = df['remaining_lease_year'].isna()
    if failed.any():
        raise ValueError(f"{failed.sum()} rows failed remaining_lease_extraction")
    
    return df.drop(columns=['remaining_lease'])

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"lease_commence_date": "lease_commence_year"})

def clean(data_dir: str) -> pd.DataFrame:
    df = load_csvs(data_dir)
    logger.info(f"Loaded {len(df):,} rows")

    validate_month_format(df)
    df['remaining_lease'] = df.apply(calc_remaining_lease, axis=1)
    df = split_month(df)
    df = split_remaining_lease(df)
    df = rename_columns(df)

    logger.info(f"Cleaning complete. {len(df):,} rows ready.")
    return df

# def main():
#     df = clean(data_dir="data/raw")
#     df.info()
#     df.describe()
#     #output_path = "data/output_data/output.csv"
#     #df.to_csv(output_path, index_label="id")
#     #logger.info(f"Saved to {output_path}")



# if __name__ == "__main__":
#     main()

