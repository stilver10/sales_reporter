import pandas as pd
from typing import List
from analyze_tools import calculate_growth
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False 
# plt.rcParams['font.family'] = 'NanumGothic'
sns.set_style("whitegrid")

def yearly_report_chart(
    df_grouped: pd.DataFrame, valid_years: List[int]
) -> tuple:

    df_grouped['금액'] = df_grouped['금액'] / 1_000_000


    # 연도별 매출액 추이
    fig1, ax = plt.subplots()
    sns.lineplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        hue='매출년도',
        style="매출년도",
        markers=True,
        ax=ax
    )
    ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax.set_ylabel('매출액 (백만원)')
    ax.set_title('월별 매출액 추이')


    # 월별 매출 분포도
    fig2, ax = plt.subplots()
    sns.violinplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        color=".9",
        inner=None,
        ax=ax
    )
    sns.swarmplot(
        data=df_grouped,
        x="매출월",
        y="금액",
        hue='매출년도',
        size=3,
        ax=ax
    )
    ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax.set_ylabel('매출액 (백만원)')
    ax.set_title('월별 매출 분포도')


    # 연도별 판매량 대비 매출액 분산도
    fig3 = sns.lmplot(
        data=df_grouped,
        x='수량',
        y='금액',
        hue='매출년도',
        col='매출년도',
    )
    fig3.figure.suptitle('연도별 판매량 대비 매출액 분산도', y=1.05)
    for ax in fig3.axes.flat:
        ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))
        ax.set_ylabel('매출액 (백만원)')



    # 직전년도 대비 월별 매출액 증감률(%)
    df_grouped = df_grouped[df_grouped['매출년도'].isin(valid_years[-2:])]
    df_growth = calculate_growth(
        df_grouped, valid_years[-2:],
        '매출월',
        '금액'
        ).reset_index(names=['매출월'])
    df_growth.columns = ['매출월', '금액 증감량', '금액 증감률(%)']
    df_growth['매출월'] = df_growth['매출월'].astype(str)

    fig4, ax1 = plt.subplots()
    sns.barplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        hue='매출년도',
        ax=ax1
    )
    ax1.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax1.set_ylabel('매출액 (백만원)')

    ax2 = ax1.twinx()
    sns.lineplot(
        data=df_growth,
        x='매출월',
        y='금액 증감률(%)',
        ax=ax2,
        lw=1.5,
        color='red'
    )
    y1_min, y1_max = 1200, 2000 # ax1 = y축 {금액.min(), 금액.max()}
    y2_min, y2_max = -40, 40 # ax2 = y축 {금액 증감률(%).min(), 금액 증감률(%).max()}
    
    ax1.set_ylim(y1_min, y1_max)
    ax2.set_ylim(y2_min, y2_max)
    ax1.yaxis.set_major_locator(MaxNLocator(4))
    ax2.yaxis.set_major_locator(MaxNLocator(4))

    fig4.suptitle('직전년도 대비 월별 매출액 추이 및 증감률(%)')


    return fig1, fig2, fig3, fig4

def million_formatter(x, p):
    return format(int(x), ',')