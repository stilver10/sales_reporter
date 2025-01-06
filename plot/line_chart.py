import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'NanumGothic'
sns.set_style("whitegrid")

def monthly_report_chart(
    df_grouped: pd.DataFrame
) -> pd.MultiIndex:



    # plt.title('월별 판매 수량')
    a = sns.lineplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        hue='매출년도',
        style="매출년도",
        markers=True
    ).set(title='월별 매출액')


    b = sns.catplot(
        data=df_grouped,
        x='매출월',
        y='금액',
        kind='violin',
        color=".9",
        inner=None
    )
    b = sns.swarmplot(
        data=df_grouped,
        x="매출월",
        y="금액",
        hue='매출년도',
        size=3)
    # .set(title='월별 매출 분포도')

    g = sns.lmplot(
        data=df_grouped,
        x='수량',
        y='금액',
        hue='매출년도',
        col='매출년도',
    )
    g.figure.suptitle('연도별 판매량 대비 매출액 분산도', y=1.05)


    plt.show()
    return