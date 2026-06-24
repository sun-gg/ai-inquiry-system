import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI询盘分析系统", layout="wide")

st.title("📊 AI询盘周对比分析系统")

file = st.file_uploader("上传Excel（含：分析总表 + P4P计划对比表）", type=["xlsx"])

if file:
    xls = pd.ExcelFile(file)

    df_main = pd.read_excel(xls, "分析总表")
    df_p4p = pd.read_excel(xls, "P4P计划对比表")

    st.subheader("📌 分析总表")
    st.dataframe(df_main)

    st.subheader("📌 P4P计划对比表")
    st.dataframe(df_p4p)

    st.subheader("🧠 自动分析（简版）")

    # 取最后两周
    try:
        df_main = df_main.sort_values(df_main.columns[0])
        last = df_main.iloc[-1]
        prev = df_main.iloc[-2]

        inquiry_change = last["询盘数"] - prev["询盘数"]
        click_change = last["点击次数"] - prev["点击次数"]
        visit_change = last["访问人数"] - prev["访问人数"]

        st.write("📈 询盘变化：", inquiry_change)
        st.write("👆 点击变化：", click_change)
        st.write("👀 访问变化：", visit_change)

        if inquiry_change > 0:
            st.success("询盘上涨：流量或转化改善")
        else:
            st.error("询盘下降：需要检查流量或转化")

    except Exception as e:
        st.warning("请检查表字段是否一致")
        st.write(e)