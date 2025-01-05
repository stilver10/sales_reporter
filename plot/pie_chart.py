import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc # 폰트 세팅을 위한 모듈 추가
font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)

def monthly_report_chart(
    df_grouped: pd.DataFrame, valid_years: List[int]
) -> pd.MultiIndex:

    recent_year = valid_years[-1]
    data = df_grouped[df_grouped['매출년도'].isin([recent_year])]
    data = data.sort_values(by=('금액'), ascending=False)
    print(data)

    plt.pie(data['금액'],
        # labels = data['거래처명'],
        labeldistance = 0.1,
        startangle = 90,
        counterclock = False,
        rotatelabels = True)
    plt.legend(data['거래처명'])

    plt.show()
    return