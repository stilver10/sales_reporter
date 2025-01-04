import os 
from pathlib import Path
from data_preprocesser import load_sales_data, calculate_years
from sales_analyzer import monthly_sales_and_revenue, sales_order_customer, sales_order_product

def main():
    # 실행 파일 위치 출력
    current_directory = Path(os.path.dirname(__file__))
    print(f'저장 파일 위치: {current_directory}')

    # 데이터베이스 파일 경로 설정
    db_file_path = Path('c:/Users/hyeon/Desktop/영업부 코드/2018~2022 매출 데이터베이스.xlsx')
    print(f'db 파일 경로: {db_file_path}')

    # 원본 데이터 로드
    raw_data = load_sales_data(db_file_path)
    valid_years = calculate_years(raw_data, start_year = None, end_year = None)
    print('##############','\t', '조회년도:', valid_years, '\t', '##############')

    monthly_report = monthly_sales_and_revenue(raw_data, valid_years)
    customer_report = sales_order_customer(raw_data, valid_years)
    product_report = sales_order_product(raw_data, valid_years)
    print(monthly_report, '\n', customer_report, '\n', product_report, '\n', )

if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement.
    main()