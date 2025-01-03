import pandas as pd
from typing import Optional, List


def aggregate_data(
    raw_data: pd.DataFrame,
    valid_years: List[int],
    index_column: str,
    value_column: str,
    value_column2: Optional[str] = None,
) -> pd.DataFrame:
    """
    데이터를 그룹화하고 집계하는 함수.
    """
    filtered_data = raw_data[raw_data['매출년도'].isin(valid_years)]

    # 그룹화할 열 설정
    columns_to_group = [value_column] + ([value_column2] if value_column2 is not None else [])
    # 데이터 그룹화 및 집계
    df = (
        filtered_data.groupby(['매출년도', index_column])[columns_to_group]
        .sum()
        .reset_index()
    )

    return df