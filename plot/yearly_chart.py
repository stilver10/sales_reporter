import pandas as pd
import numpy as np
from typing import List
from analyze_tools import calculate_growth
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False 
sns.set_style("whitegrid")

def yearly_report_chart(
    df_grouped: pd.DataFrame,
    valid_years: List[int]
) -> tuple:

    df_grouped['금액'] = df_grouped['금액'] / 100_000_000


    """ # 월별 매출 분포도
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
    ax.set_ylabel('매출액 (억 원)')
    ax.set_title('월별 매출 분포도') """


    # 연도별 판매량 대비 매출액 분산도
    fig3 = sns.lmplot(
        data=df_grouped,
        x='수량',
        y='금액',
        hue='매출년도',
        col='매출년도',
    )
    fig3.figure.suptitle('연도별 판매량 대비 매출액 기울기(그래프 기울기가 가파를수록 톤 수 대비 매출이 올라감)', position = (0.5, 1.0+0.05))
    for ax in fig3.axes.flat:
        ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))
        ax.set_ylabel('매출액 (억 원)')



    # 월별 매출액 증감률(%)
    df_growth = calculate_growth(
        df_grouped, valid_years[-2:],
        '매출월',
        '금액'
        ).droplevel(0, axis=1)
    df_growth.index = df_growth.index.astype(str)
    
    fig4, ax1 = plt.subplots()
    sns.barplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        hue='매출년도',
        ax=ax1
    )
    ax1.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax1.set_ylabel('매출액 (억 원)')

    ax2 = ax1.twinx()
    sns.lineplot(
        data=df_growth,
        x='매출월',
        y='전년 대비 증감률(%)',
        ax=ax2,
        lw=1,
        color='red',
        marker='o',
        markersize=4,
        markerfacecolor='red'
    )
    ax1.legend(loc='upper right', fontsize='x-small')

    y1_min, y1_max = df_grouped['금액'].min() * 0.9, df_grouped['금액'].max() * 1.1
    y2_min, y2_max = -90, 90
    # 매출액 y축 간격 계산 (소수점 없이)
    y1_tick_step = round((y1_max - y1_min) / 6)  # 6개의 눈금으로 설정, 100 단위로 반올림
    y1_ticks = np.arange(
        np.floor(y1_min / y1_tick_step) * y1_tick_step,
        np.ceil(y1_max / y1_tick_step) * y1_tick_step + y1_tick_step,
        y1_tick_step,
    )
    # 전년 대비 증감률 y축 간격 계산 (소수점 없이)
    y2_tick_step = 30  # 고정된 25 단위 간격
    y2_ticks = np.arange(
        np.floor(y2_min / y2_tick_step) * y2_tick_step,
        np.ceil(y2_max / y2_tick_step) * y2_tick_step + y2_tick_step,
        y2_tick_step,
    )
    # y축 설정
    ax1.set_ylim(y1_ticks[0], y1_ticks[-1])
    ax1.set_yticks(y1_ticks)
    ax2.set_ylim(y2_ticks[0], y2_ticks[-1])
    ax2.set_yticks(y2_ticks)

    fig4.suptitle('월별 매출액 추이 및 증감률(%)')

    return fig3, fig4

def million_formatter(x, p):
    return format(int(x), ',')