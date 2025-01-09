import os 
from pathlib import Path
from data_preprocesser import load_sales_data, calculate_years
from sales_analyzer import monthly_sales_and_revenue, sales_order_customer, sales_order_product, save_result
from plot import yearly_report_chart, customer_report_chart, customer_historical_chart

def main():
    # 실행 파일 위치 출력
    current_directory = Path(os.path.dirname(__file__))
    print(f'저장 파일 위치: {current_directory}')

    # 데이터베이스 파일 경로 설정
    db_file_path = Path("C:/Users/stilv/OneDrive/바탕 화면/매출 데이터베이스.xlsx")
    print(f'db 파일 경로: {db_file_path}')

    # 원본 데이터 로드
    raw_data, missing_value = load_sales_data(db_file_path)
    valid_years = calculate_years(raw_data, start_year = 2020, end_year = 2024)
    print('조회년도:', valid_years)

    monthly_report, monthly_grouped = monthly_sales_and_revenue(raw_data, valid_years)
    customer_report, cusomer_grouped = sales_order_customer(raw_data, valid_years)
    product_report, product_grouped = sales_order_product(raw_data, valid_years)

    yearly_chart = yearly_report_chart(monthly_grouped, valid_years)
    customer_chart = customer_historical_chart(cusomer_grouped)
    fig = customer_report_chart(cusomer_grouped, valid_years)

    charts = []
    charts.append(yearly_chart)
    charts.append(customer_chart)
    charts.extend(fig)
    # test_chart(cusomer_grouped, valid_years)

    save_result(
        current_directory,
        missing_value,
        monthly_report,
        customer_report,
        product_report,
        yearly_chart,
        customer_chart,
        fig,
    )

if __name__ == "__main__":

    main()