import pandas as pd 


def merge_quantity_and_sales(
    df_quantity: pd.DataFrame, df_sales: pd.DataFrame
) -> pd.DataFrame:
    """
    수량과 금액 데이터를 병합하는 메소드.
    """
    df_merged = pd.merge(
        df_quantity, df_sales, left_index=True, right_index=True, how='inner'
    )

    # 최신 연도를 기준으로 정렬
    year_columns = df_sales.columns.get_level_values(1)
    numeric_years = pd.to_numeric(
        [year for year in year_columns if isinstance(year, int)]
    )
    latest_year_in_data = numeric_years.max()
    df_merged = df_merged.sort_values(
        by=('금액', latest_year_in_data), ascending=False
    )

    return df_merged