import os
from pathlib import Path
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def save_result(
    file_path: Path,
    missing_value: pd.DataFrame,
    monthly_report: pd.DataFrame,
    customer_report: pd.DataFrame,
    product_report: pd.DataFrame,
    yearly_chart: tuple,
    customer_chart: tuple,
    fig: tuple
) -> None:

    directory = file_path.parent / '연간 매출 보고서'
    original_directory = directory
    counter = 1
    while directory.exists():
        directory = original_directory.with_name(f"{original_directory.stem}({counter})")
        counter += 1
    os.mkdir(directory)

    missing_value.to_csv(path_or_buf= directory / '이상값.csv', encoding='utf-8-sig')

    file_path = directory / '매출 보고서.xlsx'
    with pd.ExcelWriter(file_path) as writer:
        monthly_report.to_excel(writer, sheet_name='월별 매출액')
        customer_report.to_excel(writer, sheet_name='거래처별 매출액')
        product_report.to_excel(writer, sheet_name='품목별 매출액')


    yearly_chart[0].figure.savefig(directory / '월별 매출액 추이.pdf')
    # yearly_chart[1].figure.savefig(directory / '월별 매출 분포도.pdf')
    # yearly_chart[2].figure.savefig(directory / '연도별 판매량 대비 매출액 분산도.pdf')
    yearly_chart[3].figure.savefig(directory / '직전년도 대비 월별 매출액 추이 및 증감률(%).pdf')
    customer_chart.figure.savefig(directory / '5억원 이상 거래처 매출액 추이.pdf')

    with PdfPages(directory / '거래처별 매출액 점유율.pdf') as pdf:
        for figure in fig:
            pdf.savefig(figure)

    print(f'"{directory}"에 저장되었습니다.')