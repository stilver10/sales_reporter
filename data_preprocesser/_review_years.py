import pandas as pd
from typing import Optional, List


def calculate_years(
    raw_data: pd.DataFrame, start_year: Optional[int] = None, end_year: Optional[int] = None
) -> List[int]:

    latest_year = raw_data['매출년도'].max()
    earliest_year = raw_data['매출년도'].min()

    # 잘못된 연도 범위 처리
    if start_year is not None and end_year is not None and start_year > end_year:
        raise ValueError(
            f"잘못된 연도 범위: start_year ({start_year})는 end_year ({end_year})보다 작거나 같아야 합니다."
        )

    # start_year와 end_year가 모두 없는 경우: 최근 3년 반환
    if start_year is None and end_year is None:
        years = [latest_year - i for i in range(2, -1, -1)]
    # start_year 또는 end_year가 있는 경우: 해당 범위의 연도 반환
    else:
        if start_year is None:
            start_year = earliest_year
        if end_year is None:
            end_year = latest_year
        years = list(range(start_year, end_year + 1))

    # 실제 데이터프레임에 존재하는 연도와 교집합 반환
    existing_years = set(raw_data['매출년도'])
    valid_years = [year for year in years if year in existing_years]


    if not valid_years:
        raise ValueError("실제 데이터프레임에 존재하는 연도가 없습니다.")
    elif valid_years != years:
        raise ValueError("일부 연도가 데이터프레임에 존재하지 않습니다.")

    return valid_years