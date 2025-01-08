import pandas as pd 
from typing import List
from data_preprocesser import aggregate_data
from analyze_tools import calculate_growth, generate_pivot_table


def sales_order_customer(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.DataFrame:
    """
    고객별 매출 데이터를 처리하고 반환하는 메소드.
    """

    index_column = '거래처명'

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
    ).sort_values(by=('금액', valid_years[-1]), ascending=False)


    if len(valid_years) == 1:
        # 최근 1년의 수량과 금액만 반환
        return df_pivot

    qnt_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량')
    sales_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액')


    customer_report = pd.concat(
        [df_pivot[['수량']],
        qnt_df,
        df_pivot[['금액']],
        sales_df
        ],
        axis=1
    )
    
    return customer_report, df_grouped


def sales_order_product(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.DataFrame:
    """
    고객별 매출 데이터를 처리하고 반환하는 메소드.
    """

    index_column = '제품명'

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
    ).sort_values(by=('금액', valid_years[-1]), ascending=False)


    if len(valid_years) == 1:
        # 최근 1년의 수량과 금액만 반환
        return df_pivot

    qnt_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량')
    sales_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액')


    product_report = pd.concat(
        [df_pivot[['수량']],
        qnt_df,
        df_pivot[['금액']],
        sales_df
        ],
        axis=1
    )
    
    return product_report, df_grouped