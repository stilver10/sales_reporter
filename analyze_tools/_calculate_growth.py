import pandas as pd
from typing import List

def calculate_growth(
    df: pd.DataFrame,
    valid_years: List[int],
    index_column: str,
    value_column: str,
) -> pd.MultiIndex:
        

    # 데이터프레임 복사 및 기본 처리
    unique_indices = df[index_column].unique()
    result_df = pd.DataFrame(index=unique_indices)
    """
    증감률과 증감량을 계산하는 메소드.
    """
    if len(valid_years) < 2:
        # print("증감률을 계산하려면 최소한 2개 이상의 연도가 필요합니다.")
        return None

    for i in range(1, len(valid_years)):
        current_year = valid_years[i]
        previous_year = valid_years[i - 1]
        period = f"{previous_year} 대비 {current_year}"

        # 기준연도와 비교연도 데이터 추출
        current_data = df[df['매출년도'] == current_year].set_index(index_column)[value_column]
        previous_data = df[df['매출년도'] == previous_year].set_index(index_column)[value_column]
        
        # 증감률과 증감량 계산 (NaN은 자동으로 처리됨)
        growth_amount = current_data - previous_data
        growth_rate = (current_data - previous_data) / previous_data * 100

        # 결과 데이터프레임에 추가 (MultiIndex 사용)
        result_df[(period, f'{value_column} 증감량')] = growth_amount
        result_df[(period, f'{value_column} 증감률(%)')] = growth_rate

    return result_df