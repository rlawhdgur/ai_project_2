# 홈

# 필요한 라이브러리
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
import sqlite3
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
# 다른 함수 import
from update import update_data
from update import run_update


def run_title():
    """홈페이지에서 인덱스화면을 표시하는 함수입니다.
    Args:
        

    Returns:
        

    Raises:
        ValueError : 
    """
    # 서울시공공데이터에서 인증키를 받아 데이터를 받아옴
    # https://data.seoul.go.kr/dataList/OA-21276/S/1/datasetView.do
    #url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/
    # service_key : 

    # run_update()
    data = update_data()
    # data = pd.read_csv('data/bds_data.csv', encoding='cp949')

    data2 = data.copy()

    # now = datetime.now()
    # before_day = now - relativedelta(days=1)
    # before_month = before_day - relativedelta(months=1)
    # before_day = before_day.strftime("%Y-%m-%d")
    # before_month = before_month.strftime("%Y-%m-%d")

    # 실거래 현황
    
    # st.subheader("""
    # 👑실거래 현황 (최신순)
    # - *최근 일주일간 서울시 실거래가 현황입니다!*
    # *※ 매일 오전 10시 5분 데이터 갱신 ※*
    # """)
    # st.write("기간 : " + f'{before_month}' + " ~ " +f'{before_day}' + " (계약일 기준)")
    latest = data.loc[1,['CNTRCT_DE']].values[0]
    st.write("기간 : 2022.01.01 ~ " +f'{latest}' + " (계약일 기준)")
    # data = data[data['CNTRCT_DE']>=f'{before_month}']

    data['FLR_NO'] = data['FLR_NO'].astype(str) + '층'
    cols = ['BOBN', 'BUBN']
    data['번지'] = data[cols].apply(lambda row: '-'.join(row.values.astype(str))
                                            if row['BUBN'] != 0
                                            else row['BOBN'], axis=1)
    data['BLDG_NM'] = data['BLDG_NM'].str.replace('아파트', '')
    data['BLDG_NM'] = data['BLDG_NM'].str.replace('오피스텔', '')                             
    cols1 = ['SGG_NM', 'BJDONG_NM', '번지', 'BLDG_NM', 'HOUSE_GBN_NM', 'FLR_NO']
    data['주소'] = data[cols1].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
    data = data.drop(['SGG_CD', 'BJDONG_CD', 'SGG_NM', 'BJDONG_NM', 'BOBN', 'BUBN', 'FLR_NO', 'BLDG_NM', '번지', 'HOUSE_GBN_NM'], axis=1)
    data['RENT_AREA'] = data['RENT_AREA'].apply(lambda x: math.trunc(x / 3.3058))
    data.columns = ['계약일', '전월세 구분', '임대면적(평)', '보증금(만원)', '임대료(만원)', '건축년도', '주소']
    data = data[['계약일', '주소', '보증금(만원)', '임대료(만원)', '임대면적(평)', '건축년도', '전월세 구분']]
    data = data.reset_index(drop=True)
    data.index = data.index+1
    st.write(data)