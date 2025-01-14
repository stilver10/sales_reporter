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
        raw_data['수량'] = raw_data['수량'].replace(r'^\s*$', '0', regex=True).astype(float)
        raw_data['단가'] = raw_data['단가'].replace(r'^\s*$', '0', regex=True).astype(float)
        raw_data['금액'] = raw_data['금액'].replace(r'^\s*$', '0', regex=True).astype(float)


        #  값의 무결성 확인 (수량*단가 == 금액) 
        integrity = raw_data.apply(lambda row: row['수량'] * row['단가'], axis=1)
        raw_data['이상값'] = raw_data['금액'] != integrity

        missing_value_counts = raw_data['이상값'].sum()
        print(f'이상값 개수: {missing_value_counts}')
        missing_value = raw_data[raw_data['이상값']]       

        raw_data.loc[
            (raw_data['거래처명'] == '유림식품') & 
            (raw_data['제품명'].isin(['둥굴레분말', '볶은-현미', '배합비']))
            , '거래처명'] = '동서'

        raw_data.loc[
            (raw_data['거래처명'] == '신우식품') &
            (raw_data['제품명'].isin(['둥굴레분말', '볶은-현미']))
            , '거래처명'] = '동서'

        raw_data.loc[
            (raw_data['거래처명'] == '동천') &
            (raw_data['제품명'].isin(['둥굴레믹스', '볶은-현미']))
            , '거래처명'] = '동서' 

        return raw_data, missing_value

    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        raise Exception(f"데이터 로드 중 오류가 발생했습니다: {e}")