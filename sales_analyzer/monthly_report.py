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


    column_order = [(year, metric) for year in sorted(valid_years) for metric in ['수량', '금액']]
    df_monthly = df_pivot.swaplevel(0, 1, axis=1).reindex(columns=column_order)

    qnt_df = calculate_growth(df_grouped, valid_years[-2:], index_column, '수량').swaplevel(axis=1)
    sales_df = calculate_growth(df_grouped, valid_years[-2:], index_column, '금액').swaplevel(axis=1)
    


    original_index = df_monthly.index.tolist()
    
    first_half = df_monthly.iloc[0:6].sum()
    second_half = df_monthly.iloc[6:12].sum()
    total = df_monthly.sum()
    
    subtotals_df = pd.DataFrame([
        first_half,
        second_half,
        total
    ], index=['상반기 소계', '하반기 소계', '연간 합계'])
    
    new_index = []
    for i, idx in enumerate(original_index):
        new_index.append(idx)
        if idx == 6:
            new_index.append('상반기 소계')
        elif idx == 12:
            new_index.append('하반기 소계')
            new_index.append('연간 합계')

    
    monthly_report = pd.concat(
        [df_monthly,
        qnt_df[['전년 대비 증감률(%)']],
        sales_df[['전년 대비 증감률(%)']],
        ],
        axis=1
    )
    monthly_report = pd.concat(
        [monthly_report,
        subtotals_df
        ]
    ).reindex(new_index)


    return monthly_report, df_grouped