import pandas as pd
from typing import Optional, List
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc # 폰트 세팅을 위한 모듈 추가
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)


def million_formatter(x, p):
    return format(int(x), ',')


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
        filter_data = pd.concat([filter_data, etc_row], ignore_index=True)

    # -----------------------------
    # 1) '거래처명' 카테고리 순서 지정
    # -----------------------------
    # - 만약 이미 '거래처명'에 '동서', '(동서)'가 없다면 자동으로 무시되니 에러 나지 않음.
    custom_order = ['동서', '(동서)']  # 원하는 순서 (앞부분)
    unique_names = list(filter_data['거래처명'].unique())

    # 현재 데이터에 있는 것들 중 '동서', '(동서)'를 제외한 나머지
    the_rest = [c for c in unique_names if c not in custom_order]

    # 최종 카테고리 순서: ['동서', '(동서)'] + 나머지(etc. 포함)
    final_categories = custom_order + the_rest
    filter_data['거래처명'] = pd.Categorical(
        filter_data['거래처명'],
        categories=final_categories,
        ordered=True
    )
    # 카테고리 순서로 정렬
    filter_data.sort_values('거래처명', inplace=True)

    # -----------------------------
    # 2) 파이차트 색상 팔레트 커스터마이징
    # -----------------------------
    import copy
    import numpy as np

    # 기본 팔레트: tab20 (20가지 색)
    base_colors = list(plt.cm.tab20.colors)

    # 색상을 지정할 딕셔너리
    color_dict = {}
    used_index = 0

    for name in final_categories:
        if name == '동서':
            color_dict[name] = '#c7fdb5'
        elif name == '(동서)':
            color_dict[name] = '#aaff32'
        elif name == 'etc.':
            # etc. 회색 지정
            color_dict[name] = '#808080'
        else:
            # 나머지는 base_colors에서 순서대로 할당
            color_dict[name] = base_colors[used_index % len(base_colors)]
            used_index += 1

    # filter_data에 있는 거래처명 순서대로 color_list 생성
    color_list = [color_dict[name] for name in filter_data['거래처명']]


    fig = plt.figure()
    wedges, labels, pct_texts = plt.pie(x = filter_data['금액'],
        autopct='%1.2f%%',
        labels = filter_data['거래처명'],
        colors = color_list,
        labeldistance = 1,
        startangle = 90,
        radius = 1,
        counterclock = False,
        rotatelabels = True
    )
    for label, pct_text in zip(labels, pct_texts):
        pct_text.set_rotation(label.get_rotation())

    plt.title(f'{year}년')
    return fig


def customer_report_chart(
    df_grouped: pd.DataFrame,
    valid_years: List[int],
    etc_threshold: Optional[float] = 0.02
) -> List[plt.Figure]:
    figs = [pie_chart_generator(df_grouped, year, etc_threshold) for year in valid_years]
    return figs


def customer_historical_chart(
    df_grouped: pd.DataFrame,
) -> plt.Figure:

    #-----------------------------------------------------------------------
    # 1) 각 연도별 Top3, Top4~10 추출
    #-----------------------------------------------------------------------
    # groupby('매출년도') 후, 연도별로 nlargest(3) / nlargest(10) → 그중 4~10 추출
    top3_list = []
    top4_10_list = []

    # 연도별로 그룹화
    for year, group in df_grouped.groupby('매출년도'):
        # (1) 각 연도별 Top10 뽑아서 큰 순으로 정렬
        top10 = group.nlargest(10, '금액')
        top10 = top10.sort_values('금액', ascending=False)

        # (2) 기본적으로 앞 3개 = top3, 나머지 = top4~10
        year_top3 = top10.iloc[:3].copy()
        year_top4_10 = top10.iloc[3:].copy()

        # (4) '매출년도' 컬럼 부착 (groupby 이후 level이 사라지므로)
        year_top3['매출년도'] = year
        year_top4_10['매출년도'] = year

        top3_list.append(year_top3)
        top4_10_list.append(year_top4_10)

    # (5) 최종 DataFrame 병합
    top3 = pd.concat(top3_list, ignore_index=True)
    top4_10 = pd.concat(top4_10_list, ignore_index=True)

    # 금액 단위 변경 예: 억 원
    top3['금액'] = top3['금액'] / 100_000_000
    top4_10['금액'] = top4_10['금액'] / 100_000_000

    base_colors = list(plt.cm.tab10.colors)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
    sns.barplot(
        data=top3,
        x='매출년도',
        y='금액',
        hue='거래처명',
        palette=base_colors,        # palette='tab10',
        width=1,
        ax=ax1
    )
    ax1.set_title('각 연도별 상위 3곳')
    ax1.set_ylabel('매출액 (억 원)')
    ax1.yaxis.set_major_formatter(FuncFormatter(million_formatter))

    handles1, labels1 = ax1.get_legend_handles_labels()
    for i, container in enumerate(ax1.containers):
        hue_label = labels1[i]
        for bar in container:
            bar_x = bar.get_x() + bar.get_width() / 2.0
            bar_height = bar.get_height()
            ax1.text(
                x=bar_x,
                y=bar_height,
                s=hue_label,
                ha='center',
                va='bottom',
                fontsize=8,
                rotation=90
            )
    ax1_names = top3['거래처명'].unique().tolist()

    filtered_indices_1 = [i for i, (hd1, lb1) in enumerate(zip(handles1, labels1))
                          if lb1 in ax1_names]
    filtered_handles_1 = [handles1[i] for i in filtered_indices_1]
    filtered_labels_1 = [labels1[i] for i in filtered_indices_1]
    ax1.legend(filtered_handles_1, filtered_labels_1, loc='upper right', fontsize=4)

    y_min1 = top3['금액'].min() * 0.9
    y_max1 = top3['금액'].max() * 1.1
    ax1.set_ylim(y_min1, y_max1)


    sns.barplot(
        data=top4_10,
        x='매출년도',
        y='금액',
        hue='거래처명',
        palette=base_colors,        # palette='tab10',
        width=0.9,
        ax=ax2
    )

    ax2.set_title('상위 거래처 4~10곳 매출액 추이')
    ax2.yaxis.set_major_formatter(FuncFormatter(million_formatter))
    ax2.set_ylabel('매출액 (억 원)')

    handles2, labels2 = ax2.get_legend_handles_labels()
    for i, container in enumerate(ax2.containers):
        hue_label = labels2[i]  # i번 컨테이너와 i번 라벨을 매핑
        for bar in container:
            bar_x = bar.get_x() + bar.get_width() / 2.0
            bar_height = bar.get_height()

            # 막대 위에 hue_label 표시
            ax2.text(
                x=bar_x,
                y=bar_height,
                s=hue_label,
                ha='center',
                va='bottom',
                fontsize=4,
                rotation=90
            )
    ax2_names = top4_10['거래처명'].unique().tolist()

    filtered_indices_2 = [i for i, (hd2, lb2) in enumerate(zip(handles2, labels2))
                          if lb2 in ax2_names]
    filtered_handles_2 = [handles2[i] for i in filtered_indices_2]
    filtered_labels_2 = [labels2[i] for i in filtered_indices_2]
    ax2.legend(filtered_handles_2, filtered_labels_2, loc='upper right', fontsize=4)
    y_min2 = top4_10['금액'].min() * 0.9
    y_max2 = top4_10['금액'].max() * 1.1
    # ax_min = min(y_min1, y_min2)
    # ax_max = max(y_max1, y_max2)
    ax2.set_ylim(y_min2, y_max2)

    return fig