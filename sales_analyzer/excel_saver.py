from pathlib import Path
import pandas as pd


def save_to_excel(
    self,
    file_path: Path,
    monthly_report: pd.DataFrame,
    customer_report: pd.DataFrame,
    product_report: pd.DataFrame
) -> None:
    """
    분석 결과를 Excel 파일로 저장하는 메소드.
    """
    try:
        # 파일이 이미 존재하는 경우 이름에 숫자를 추가하여 새 파일명 설정
        original_file_path = file_path
        counter = 1
        while file_path.exists():
            file_path = original_file_path.with_name(
                f"{original_file_path.stem}_{counter}{original_file_path.suffix}"
            )
            counter += 1

        with pd.ExcelWriter(file_path) as writer:
            monthly_report.to_excel(writer, sheet_name='monthly_result')
            customer_report.to_excel(writer, sheet_name='customer_result')
            product_report.to_excel(writer, sheet_name='product_result')

        print(f"{file_path} 에 저장되었습니다.")

    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")