import pandas as pd
from typing import List

def calculate_growth(
    df_grouped: pd.DataFrame,
    valid_years: List[int],
    index_column: str,
    value_column: str,
) -> pd.DataFrame:
        

    if len(valid_years) < 2:
        # print("증감률을 계산하려면 최소한 2개 이상의 연도가 필요합니다.")
        return None

    current_year = valid_years[-1]
    previous_year = valid_years[-2]
    # period = f"{previous_year} 대비 {current_year}"

    # 기준연도와 비교연도 데이터 추출
    current_data = df_grouped[df_grouped['매출년도'] == current_year].set_index(index_column)[value_column]
    previous_data = df_grouped[df_grouped['매출년도'] == previous_year].set_index(index_column)[value_column]
    
    # 증감률과 증감량 계산 (NaN은 자동으로 처리됨)
    growth_amount = current_data - previous_data
    growth_rate = (current_data - previous_data) / previous_data * 100

    
    result_df = pd.DataFrame({
        (value_column, f'전년 대비 증감량'): growth_amount,
        (value_column, f'전년 대비 증감률(%)'): growth_rate
    }, index=current_data.index)

    multi_cols = pd.MultiIndex.from_tuples([
        (value_column, f'전년 대비 증감량'),
        (value_column, f'전년 대비 증감률(%)')
    ])
    result_df.columns = multi_cols

    return result_df