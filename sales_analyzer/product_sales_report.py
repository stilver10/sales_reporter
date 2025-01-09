import pandas as pd 
from typing import List
from analyze_tools import calculate_growth


def sales_order_product(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.DataFrame:
    """
    고객별 매출 데이터를 처리하고 반환하는 메소드.
    """

    index_column = '제품명'

    filtered_data = raw_data[raw_data['매출년도'].isin(valid_years)]
    df_grouped = (
        filtered_data
        .groupby(['매출년도', index_column])[['수량', '금액']]
        .sum()
        .reset_index()
    )
    # 연도별 총합 계산
    yearly_total = raw_data.groupby('매출년도')[['수량', '금액']].sum()
    # 점유율 계산을 위한 데이터 준비
    df_grouped = df_grouped.merge(yearly_total, on='매출년도', suffixes=('', '_total'))
    df_grouped['수량_점유율(%)'] = df_grouped['수량'] / df_grouped['수량_total'] * 100
    df_grouped['금액_점유율(%)'] = df_grouped['금액'] / df_grouped['금액_total'] * 100
    df_grouped = df_grouped.drop(['수량_total', '금액_total'], axis=1)

    df_pivot = df_grouped.pivot(
        index=index_column,
        columns='매출년도',
        values=['수량', '금액', '수량_점유율(%)', '금액_점유율(%)']
    ).sort_values(by=('금액', valid_years[-1]), ascending=False)


    if len(valid_years) == 1:
        # 최근 1년의 수량과 금액만 반환
        return df_pivot
    
    qnt_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량')
    sales_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액')
    qnt_share_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '수량_점유율(%)')
    sales_share_df = calculate_growth(df_grouped, valid_years, index_column, value_column = '금액_점유율(%)')

    product_report = pd.concat(
        [df_pivot[['수량']],
        qnt_df,
        df_pivot[['금액']],
        sales_df,
        df_pivot[['수량_점유율(%)']],
        qnt_share_df[['수량_점유율(%)']],
        df_pivot[['금액_점유율(%)']],
        sales_share_df[['금액_점유율(%)']]
        ],
        axis=1
    )

    return product_report, df_grouped