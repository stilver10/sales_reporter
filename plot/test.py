import pandas as pd
from typing import Optional, List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import font_manager, rc # 폰트 세팅을 위한 모듈 추가
font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)



def test_chart(
    df_grouped: pd.DataFrame,
    valid_years: List[int],
    etc_threshold: Optional[float] = 0.02
) -> None:
    # 서브플롯 생성
    fig, axes = plt.subplots(1, len(valid_years), figsize=(8*len(valid_years), 5))
    
    for idx, year in enumerate(valid_years):
        data = df_grouped[df_grouped['매출년도'] == year]
        data = data.sort_values(by='금액', ascending=False)
        
        threshold = data['금액'].sum() * etc_threshold
        etc_mask = data['금액'] < threshold
        etc_sum = data[etc_mask]['금액'].sum()
        
        filter_data = data[~etc_mask].copy()
        
        if etc_sum > 0:
            new_row = pd.DataFrame({'거래처명': ['기타'], '금액': [etc_sum], '매출년도': [year]})
            filter_data = pd.concat([filter_data, new_row])
        
        # 파이 차트 그리기
        wedges, texts, autotexts = axes[idx].pie(
            filter_data['금액'],
            labels=filter_data['거래처명'],
            autopct='%1.1f%%',
            labeldistance=1,
            startangle=90,
            radius=1.5,
            counterclock=False,
            rotatelabels=True
        )
        axes[idx].set_title(f'{year}년')

    plt.subplots_adjust(wspace=0.3)
    return fig