# 건의사항

# 라이브러리
import streamlit as st
import sqlite3
import time
import pandas as pd

conn = sqlite3.connect('suggestion.db', check_same_thread=False)
cur = conn.cursor()

# 테이블 생성
def create_tb():
    cur.execute('CREATE TABLE IF NOT EXISTS suggestion(author CHAR, email VARCHAR, title TEXT, comment TEXT, date TEXT, status TEXT)' )
    conn.commit()

# db 입력
def add_data(author, pword, title, date, comment, status):
    params = (author, pword, title, str(date), comment, status)
    cur.execute("INSERT INTO suggestion(author, email, title, date, comment, status) VALUES (?,?,?,?,?,?)",params)
    conn.commit()

# 목록 불러오기
def sugg_list():
    cur.execute('SELECT author, title, date, comment, status FROM suggestion')
    sugg = cur.fetchall()
    return sugg

# # 수정 (update)
# def data_update(username):
#     pass
# # 삭제 (delete)
# def data_delete(username):
#     cur.execute('DELETE FROM suggestion WHERE AUTHOR =:AUTHOR' ,{'AUTHOR':author})
#     conn.commit()
#     # conn.close()

# 검색 (작성자명)
def get_by_author(author):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE author like '%{}%'".format(author))
	data = cur.fetchall()
	return data
# 검색(제목)
def get_by_title(title):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE title like '%{}%'".format(title))
	data = cur.fetchall()
	return data
# 검색(내용)
def get_by_comment(comment):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE comment like '%{}%'".format(comment))
	data = cur.fetchall()
	return data

# 처리상태 수정
def update_status(email):
    cur.execute('UPDATE suggestion SET status = "처리완료" WHERE email="{}"'.format(email))
    conn.commit()
def recover_status(email):
    cur.execute('UPDATE suggestion SET status = "접수" WHERE email="{}"'.format(email))
    conn.commit()

def delete_post(email):
    cur.execute('DELETE FROM suggestion WHERE email = "{}"'.format(email))
    conn.commit()
     # conn.close()

# 게시글 수정/삭제
def update_sugg(title, comment, author, pword):
    cur.execute('UPDATE suggestion SET ??')
    conn.commit()

# LOGIN SAMPLE CODE
# conn = sqlite3.connect('data.db')
# c = conn.cursor()
# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)')
# def add_userdata(username,password):
# 	c.execute('INSERT INTO users(username,password) VALUES (?,?)',(username,password))
# 	conn.commit()
# def login_user(username,password):
# 	c.execute('SELECT * FROM users WHERE username =? AND password = ?',(username,password))
# 	data = c.fetchall()
# 	return data


# ▲ DB 관련
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def run_suggestions():
    """홈페이지에서 건의사항 화면을 표시하는 함수입니다.
    Args:
        

    Returns:
        

    Raises:
        ValueError : 
    """

    st.subheader("""
    건의사항💢
    - *궁금하시거나 불편하신 점 있으시면 게시판 등록해주세요!!*
    """)

    # 문의사항 입력
    with st.expander("문의하기"):
        sugg_tab1, sugg_tab2 = st.tabs(["글 등록", "수정/삭제"]) 
        with sugg_tab1:
            form_submit = st.form(key="submit")
            with form_submit:
                create_tb()
                cols = st.columns((1,1))
                author = cols[0].text_input("작성자명 ", max_chars = 12)
                pword = cols[1].text_input("비밀번호", type = "password")
                email = st.text_input("이메일")
                title = st.text_input("제목", max_chars = 50)
                comment = st.text_area("내용 ")
                submit = st.form_submit_button(label="작성")
                date = time.strftime('%Y.%m.%d %H:%M:%S')
                status = "접수"
                # 문의사항 접수
                if submit:
                    if author == "" or pword == "" or email == "" or title == "" or comment == "":
                        st.error('빈칸을 확인해주세요.')

                    else:
                        add_data(author, pword, email, title, comment, date, status)
                        st.success("문의하신 내용이 접수되었습니다! 답변은 이메일로 발송됩니다. 감사합니다.")
                        st.snow() 

        with sugg_tab2:
            form_update = st.form(key="update")
            with form_update:
                cols = st.columns((1,1))
                author = cols[0].text_input("작성자명 ", max_chars = 12)
                pword = cols[1].text_input("비밀번호", type = "password")
                # email = st.text_input("이메일")
                title = st.text_input("제목", max_chars = 50)
                comment = st.text_area("내용 ")
                if st.form_submit_button("수정"):
                    pass
                    # update_sugg(title, comment, author, pword)

    # 검색
    with st.expander("검색"):
        cols = st.columns((1,1))
        search_term = cols[0].text_input(' ')
        search_option = cols[1].selectbox(" ",("--검색옵션--","내용","작성자명","제목"))
        if st.button("검색"):
                if search_term == "":
                    st.warning("검색어를 입력하세요")
                elif search_option == "내용":
                    result=get_by_comment(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                elif search_option =="작성자명":
                    result=get_by_author(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                elif search_option =="제목":
                    result=get_by_title(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                else :
                    st.warning("검색옵션을 입력하세요")


    # 목록
    tab1, tab2 = st.tabs(["자주 묻는 질문", "목록"])

    with tab1:
        st.markdown("작업중 아래는 예시")

        if st.checkbox("📈전세예측 조회 방법"):
            st.markdown('''
                        > 전세예측 조회방법
                        1. 전세예측 탭을 클릭한다 2. 전세/월세 그래프 중 하나를 선택한다
                        ''')

    with tab2:
        list = sugg_list()
        # st.write(list)
        df = pd.DataFrame(list, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
        st.dataframe(df, use_container_width=True)


    # 관리자 기능
    admin_option = st.checkbox("관리자 메뉴")
    if admin_option:
        cols = st.columns((1,1))
        command = cols[0].text_input("command")
        email = cols[1].text_input("email")
        if st.button ("확인"):
            if command == "ok_myroomadmin":
                update_status(email)
            elif command == "no_myroomadmin":
                recover_status(email)
            elif command == "del_myroomadmin":
                st.checkbox("삭제하시겠습니까? 작성하신 이메일을 다시 확인해주세요.")
                # del_reason = st.text_input("삭제사유")
                delete_post(email)
            else :
                st.warning("잘못된 명령입니다")