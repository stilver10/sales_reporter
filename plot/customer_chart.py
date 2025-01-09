import pandas as pd
from typing import Optional, List
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc # 폰트 세팅을 위한 모듈 추가
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)


def pie_chart_generator(
    df_grouped: pd.DataFrame,
    year: int,
    etc_threshold: Optional[float] = 0.02
) -> None:

    data = df_grouped[df_grouped['매출년도'] == year]
    data = data.sort_values(by=('금액'), ascending=False)

    # 2% 기준값 계산
    threshold = data['금액'].sum() * etc_threshold
    etc_mask = data['금액'] < threshold
    etc_sum = data[etc_mask]['금액'].sum()
    
    # 새로운 데이터프레임 생성
    filter_data = data[~etc_mask].copy()
    if etc_sum > 0:
        etc_row = pd.DataFrame({
            '매출년도': [year],
            '거래처명': ['etc.'],
            '금액': [etc_sum]
        })
        filter_data = pd.concat([filter_data, etc_row])

    # 차트 생성성
    fig = plt.figure()
    plt.pie(x = filter_data['금액'],
        autopct='%1.2f%%',
        labels = filter_data['거래처명'],
        colors = plt.cm.tab20.colors,
        labeldistance = 1,
        startangle = 90,
        radius = 1,
        counterclock = False,
        rotatelabels = True
    )
    plt.title(f'{year}년')
    return fig


def customer_report_chart(
    df_grouped: pd.DataFrame,
    valid_years: List[int],
    etc_threshold: Optional[float] = 0.02
) -> None:
    fig = [pie_chart_generator(df_grouped, year, etc_threshold) for year in valid_years]
    return fig


def customer_historical_chart(
    df_grouped: pd.DataFrame,
) -> tuple:
    data = (df_grouped.groupby('매출년도')
            .apply(lambda x: x.nlargest(10, '금액'))
            .reset_index(level=[0,1], drop=True)
            )
    data['금액'] = data['금액'] / 100_000_000

    fig, ax = plt.subplots()
    sns.barplot(
        data=data,
        x='매출년도',
        y='금액',
        hue='거래처명',
        palette='tab10',
        ax=ax
    )
    plt.legend(loc='upper right', fontsize='xx-small')
    handles, labels = ax.get_legend_handles_labels()  # 범례 핸들과 라벨 가져오기
    for i, container in enumerate(ax.containers):
        hue_label = labels[i]  # i번 컨테이너와 i번 라벨을 매핑
        for bar in container:
            bar_x = bar.get_x() + bar.get_width() / 2.0
            bar_height = bar.get_height()

            # 막대 위에 hue_label 표시
            ax.text(
                x=bar_x,
                y=bar_height,
                s=hue_label,
                ha='center',
                va='bottom',
                fontsize=4,
                rotation=90
            )

    # y축 포매터 세팅(백만원 단위로 표시)
    ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax.set_ylabel('매출액 (억 원)')
    ax.set_title('상위 거래처 10곳 매출액 추이')

    # x축 눈금: 매년 하나씩 표시되도록 설정 (필요시 주석 처리)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))

    # y축 최소/최대 범위 설정 (10% 여유)
    y_min = data['금액'].min() * 0.9
    y_max = data['금액'].max() * 1.1
    ax.set_ylim(y_min, y_max)

    return fig


def million_formatter(x, p):
    return format(int(x), ',')