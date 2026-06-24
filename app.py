import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 AI询盘对比系统 V2（自动识别版）")

file = st.file_uploader("上传Excel", type=["xlsx"])

if file:

    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, "分析总表")

    st.subheader("📌 原始数据")
    st.dataframe(df)

    # =========================
    # 1. 自动清洗列名
    # =========================
    df.columns = df.columns.astype(str)

    # =========================
    # 2. 只保留数值列
    # =========================
    numeric_df = df.select_dtypes(include=[np.number])

    if len(numeric_df) < 2:
        st.error("❌ 数据行不足2行，无法对比")
        st.stop()

    # =========================
    # 3. 取最后两周
    # =========================
    last = numeric_df.iloc[-1]
    prev = numeric_df.iloc[-2]

    # =========================
    # 4. 自动计算差值
    # =========================
    result = []

    for col in numeric_df.columns:

        now = last[col]
        before = prev[col]

        diff = now - before

        if before != 0:
            pct = (diff / before) * 100
        else:
            pct = None

        result.append({
            "指标": col,
            "24周": now,
            "23周": before,
            "变化值": diff,
            "变化率%": pct
        })

    result_df = pd.DataFrame(result)

    # =========================
    # 5. 展示
    # =========================
    st.subheader("📊 自动对比结果")

    st.dataframe(result_df.sort_values("变化值", ascending=False))

    # =========================
    # 6. 自动结论（简版）
    # =========================
    st.subheader("🧠 AI简易判断")

    # 找询盘相关列（自动匹配）
    inquiry_cols = [c for c in numeric_df.columns if "询盘" in str(c)]

    if inquiry_cols:

        col = inquiry_cols[0]

        diff = last[col] - prev[col]

        if diff > 0:
            st.success(f"📈 询盘上升：+{diff}")
        else:
            st.error(f"📉 询盘下降：{diff}")

    else:
        st.warning("⚠️ 未识别到询盘字段")
