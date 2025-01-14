import pandas as pd

def merge_product_data(
    raw_data, valid_years
) -> pd.DataFrame:

    product_list = pd.read_csv("C:/Users/stilv/OneDrive/바탕 화면/2024_거래제품명.csv")
    product_list = product_list.sort_values(['제품군', '제품명'])
    print(product_list)
    product_list.to_csv('product_list.csv', index=False, encoding='utf-8-sig')
    filtered_data = raw_data[raw_data['매출년도'] == (valid_years[-1])]
    filtered_data2 = pd.DataFrame(filtered_data['제품명'].unique(), columns=['제품명'])
    result = (pd.merge(product_list, filtered_data, on='제품명')
             .groupby(['제품군', '거래처명', '제품명', '매출월'])[['수량', '금액']]
             .sum()
             .reset_index()
             .sort_values(['제품군', '거래처명', '제품명', '매출월', '금액'])
            )
    result.to_csv('test.csv', index=False, encoding='utf-8-sig')
    return result