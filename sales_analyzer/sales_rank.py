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

    df_quantity = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량')
    df_sales = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액')
    

    # MultiIndex를 명시적으로 설정
    df_quantity.columns = pd.MultiIndex.from_tuples(df_quantity.columns)
    df_sales.columns = pd.MultiIndex.from_tuples(df_sales.columns)

    # 레벨 교환 및 정렬
    df_quantity = df_quantity.swaplevel(0, 1, axis=1)
    df_quantity.sort_index(axis=1, level=0, inplace=True)
    df_sales = df_sales.swaplevel(0, 1, axis=1)
    df_sales.sort_index(axis=1, level=0, inplace=True)

    customer_report = pd.concat([df_pivot, df_quantity, df_sales], axis= 'columns')
    # df_order_customer = merge_quantity_and_sales(df_quantity, df_sales)

    return customer_report


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

    df_quantity = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량')
    df_sales = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액')
    

    # MultiIndex를 명시적으로 설정
    df_quantity.columns = pd.MultiIndex.from_tuples(df_quantity.columns)
    df_sales.columns = pd.MultiIndex.from_tuples(df_sales.columns)

    # 레벨 교환 및 정렬
    df_quantity = df_quantity.swaplevel(0, 1, axis=1)
    df_quantity.sort_index(axis=1, level=0, inplace=True)
    df_sales = df_sales.swaplevel(0, 1, axis=1)
    df_sales.sort_index(axis=1, level=0, inplace=True)

    product_report = pd.concat([df_pivot, df_quantity, df_sales], axis= 'columns')
    # df_order_customer = merge_quantity_and_sales(df_quantity, df_sales)

    return product_report