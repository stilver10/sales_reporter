import pandas as pd 
from typing import List
from data_preprocesser import aggregate_data
from analyze_tools import calculate_growth, generate_pivot_table


def monthly_sales_and_revenue(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.DataFrame:

    index_column = '매출월'

    df_grouped = aggregate_data(
        raw_data,
        valid_years,
        index_column,
        value_column = '수량',
        value_column2 = '금액'
    )

    df_pivot = generate_pivot_table(
    df_grouped,
    index_column,
    value_column = '수량',
    value_column2 = '금액'
    )

    if len(valid_years) == 1:
        # 최근 1년의 수량과 금액만 반환
        monthly_report = df_pivot.swaplevel(0, 1, axis= 'columns')

        return monthly_report


    column_order = [(year, metric) for year in sorted(valid_years) for metric in ['수량', '금액']]
    df_monthly = df_pivot.swaplevel(0, 1, axis=1).reindex(columns=column_order)

    qnt_df = calculate_growth(df_grouped, valid_years[-2:], index_column, '수량').swaplevel(axis=1)
    sales_df = calculate_growth(df_grouped, valid_years[-2:], index_column, '금액').swaplevel(axis=1)
    
    monthly_report = pd.concat(
        [df_monthly,
        qnt_df[['전년 대비 증감률(%)']],
        sales_df[['전년 대비 증감률(%)']]
        ],
        axis=1
    )


    return monthly_report, df_grouped