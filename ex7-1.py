import streamlit as st

st.title("第7回 Streamlit レイアウト演習 - テンプレート")
st.caption("st.sidebar, st.columns, st.expander を使ってみましょう。")

st.markdown("---")
st.subheader("演習1: サイドバー (st.sidebar)")
st.write("**課題**: サイドバーに自分の名前と学籍番号を表示するテキスト入力を配置。")

# ここに演習1のコードを記述してください
# ヒント: st.sidebar.text_input() を使います
name = st.sidebar.text_input("名前")
student_id = st.sidebar.text_input("学籍番号")
if name and student_id:
    st.sidebar.write("名前: " + name)
    st.sidebar.write("学籍番号: " + student_id)


st.markdown("---")
st.subheader("演習2: カラムレイアウト (st.columns)")
st.write("**課題**: メインエリアを2列に分け、左列に好きなものの画像、右列にその説明文を表示。")

# ここに演習2のコードを記述してください
# ヒント: st.columns(2), st.image() を使います
col1,col2 = st.columns(2)
with col1:
    st.image("https://static.streamlit.io/examples/cat.jpg")
with col2:
    st.write("猫")
    with st.expander("詳細"):
        st.write("ふさふさです。")


st.markdown("---")
st.subheader("演習3: エキスパンダー (st.expander)")
st.write("**課題**: 説明文の下にエキスパンダーを設け、さらに詳細な情報を隠して表示できるようにする。")

# ここに演習3のコードを記述してください
# ヒント: with st.expander("タイトル"): を使います



st.markdown("---")
st.info("💡 コメントアウトされたコードを参考に、各演習課題を完成させてください。") 