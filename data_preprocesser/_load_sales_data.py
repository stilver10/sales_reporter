from pathlib import Path
import pandas as pd


def load_sales_data(file_path: Path) -> pd.DataFrame:

    try:
        raw_data = pd.read_excel(
            file_path,
            sheet_name='data base',
            usecols=['매출년도', '매출월', '거래처명', '제품명', '수량', '단가', '금액'],
            skiprows=3,
        )

        # 형식 변환
        raw_data['매출년도'] = raw_data['매출년도'].astype(str).str.extract(r'(\d{4})').astype(int)
        raw_data['매출월'] = raw_data['매출월'].astype(str).str.extract(r'(\d+)').astype(int)
        raw_data['수량'] = raw_data['수량'].fillna(0).astype(float)
        raw_data['금액'] = raw_data['금액'].fillna(0).astype(float)

        # # 무한대 값 제거 및 단가가 0인 경우 금액을 0으로 설정
        # raw_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        # raw_data.loc[raw_data['단가'] == 0, '금액'] = 0
        ############## 값의 무결성 확인 (수량*단가 == 금액) ##############
        null_counts = raw_data.isnull().sum()
        print("### Null 값 개수: ###\n", null_counts)
        print("### 각 행의 Null 값: ###\n", raw_data[raw_data.isna().any(axis=1)])
        

        return raw_data

    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        raise Exception(f"데이터 로드 중 오류가 발생했습니다: {e}")