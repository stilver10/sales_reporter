import pandas as pd
from typing import Optional


def generate_pivot_table(
    df_grouped: pd.DataFrame,
    index_column: str,
    value_column: str,
    value_column2: Optional[str] = None,
) -> pd.DataFrame:
    
    # 그룹화할 열 설정
    columns_to_group = [value_column] + ([value_column2] if value_column2 is not None else [])

    df = df_grouped.pivot(
        index=index_column,
        columns='매출년도',
        values=columns_to_group
    )

    return df