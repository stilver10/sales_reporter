import pandas as pd 
from typing import List
from data_preprocesser import aggregate_data
from analyze_tools import calculate_growth, generate_pivot_table


def monthly_sales_and_revenue(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.MultiIndex:
    """
    월별 매출 및 수익 집계 및 증감률/증감량 계산.
    """

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


    # 증감률 및 증감량 계산
    df_qnt_monthly = calculate_growth(df_grouped, valid_years, index_column, '수량')
    df_sales_monthly = calculate_growth(df_grouped, valid_years, index_column, '금액')

    # 데이터프레임 멀티인덱스로 변환
    column_order = [(year, metric) for year in sorted(valid_years) for metric in ['수량', '금액']]
    df_monthly = df_pivot.swaplevel(0, 1, axis= 'columns').reindex(columns=column_order)
    monthly_report = pd.concat([df_monthly, df_qnt_monthly, df_sales_monthly], axis= 'columns')

    return monthly_report