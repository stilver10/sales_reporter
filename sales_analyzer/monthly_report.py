import pandas as pd 
from typing import List
from analyze_tools import calculate_growth


def monthly_sales_and_revenue(
    raw_data: pd.DataFrame, valid_years: List[int]
) -> pd.DataFrame:

    index_column = '매출월'

    filtered_data = raw_data[raw_data['매출년도'].isin(valid_years)]
    df_grouped = (
        filtered_data
        .groupby(['매출년도', index_column])[['수량', '금액']]
        .sum()
        .reset_index()
    )

    df_pivot = df_grouped.pivot(
        index=index_column,
        columns='매출년도',
        values=['수량', '금액']
    )


    if len(valid_years) == 1:
        # 최근 1년의 수량과 금액만 반환
        monthly_report = df_pivot.swaplevel(0, 1, axis= 'columns')

        return monthly_report

    df_first_half = (
        df_grouped[df_grouped[index_column].between(1, 6)]
        .groupby('매출년도')[['수량', '금액']]
        .sum()
        .reset_index()
    )
    df_first_half[index_column] = '상반기 소계'
    
    df_second_half = (
        df_grouped[df_grouped[index_column].between(7, 12)]
        .groupby('매출년도')[['수량', '금액']]
        .sum()
        .reset_index()
    )
    df_second_half[index_column] = '하반기 소계'

    df_year_total = (
        df_grouped
        .groupby('매출년도')[['수량', '금액']]
        .sum()
        .reset_index()
    )
    df_year_total[index_column] = '연간 합계'
    
    df_subtotals = pd.concat([df_grouped, df_first_half, df_second_half, df_year_total], ignore_index=True)


    qnt_df = calculate_growth(df_subtotals, valid_years[-2:], index_column, '수량').swaplevel(axis=1)
    sales_df = calculate_growth(df_subtotals, valid_years[-2:], index_column, '금액').swaplevel(axis=1)


    column_order = [(year, metric) for year in sorted(valid_years) for metric in ['수량', '금액']]
    df_pivot = df_subtotals.pivot(index=index_column, columns='매출년도', values=['수량', '금액'])
    df_pivot = df_pivot.swaplevel(0, 1, axis=1).reindex(columns=column_order)

    new_index = [
        1, 2, 3, 4, 5, 6, '상반기 소계', 
        7, 8, 9, 10, 11, 12, '하반기 소계', 
        '연간 합계'
    ]
    monthly_report = pd.concat(
        [df_pivot, qnt_df[['전년 대비 증감률(%)']], sales_df[['전년 대비 증감률(%)']]], 
        axis=1
    ).reindex(new_index)


    return monthly_report, df_grouped