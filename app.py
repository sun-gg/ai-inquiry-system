import streamlit as st
import pandas as pd

st.title("📊 24周 vs 23周 AI对比分析系统")

file = st.file_uploader("上传Excel", type=["xlsx"])

if file:
    xls = pd.ExcelFile(file)

    df = pd.read_excel(xls, "分析总表")

    st.subheader("原始数据")
    st.dataframe(df)

    # ===== 1. 找到最后两周 =====
    df = df.sort_values(df.columns[0])  # 第一列是“时间”

    week_now = df.iloc[-1]
    week_prev = df.iloc[-2]

    # ===== 2. 自动找数值列 =====
    numeric_cols = df.select_dtypes(include='number').columns

    result = []

    for col in numeric_cols:
        now = week_now[col]
        prev = week_prev[col]

        diff = now - prev

        # 防止除0
        if prev != 0:
            pct = (diff / prev) * 100
        else:
            pct = None

        result.append({
            "指标": col,
            "24周": now,
            "23周": prev,
            "变化值": diff,
            "变化率%": pct
        })

    result_df = pd.DataFrame(result)

    st.subheader("📊 核心对比结果（自动生成）")
    st.dataframe(result_df)
