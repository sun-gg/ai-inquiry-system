import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 AI询盘系统（最终稳定版）")

file = st.file_uploader("上传Excel", type=["xlsx"])

if file:

    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, "分析总表")

    st.subheader("📌 原始数据")
    st.dataframe(df)

    # =========================
    # 1. 自动找到 24周 / 23周列
    # =========================
    cols = df.columns.astype(str)

    col_24 = [c for c in cols if "24" in c or "本周" in c]
    col_23 = [c for c in cols if "23" in c or "上周" in c]

    if not col_24 or not col_23:
        st.error("❌ 找不到24周/23周列，请检查Excel命名")
        st.stop()

    col_24 = col_24[0]
    col_23 = col_23[0]

    # =========================
    # 2. 数值清洗
    # =========================
    df[col_24] = pd.to_numeric(df[col_24], errors="coerce")
    df[col_23] = pd.to_numeric(df[col_23], errors="coerce")

    # =========================
    # 3. 计算变化
    # =========================
    df["变化值"] = df[col_24] - df[col_23]

    df["变化率%"] = np.where(
        df[col_23] != 0,
        (df["变化值"] / df[col_23]) * 100,
        None
    )

    # =========================
    # 4. 输出结果
    # =========================
    st.subheader("📊 核心对比结果")

    st.dataframe(df[["指标", col_24, col_23, "变化值", "变化率%"]])

    # =========================
    # 5. 自动结论
    # =========================
    st.subheader("🧠 AI判断")

    if "询盘" in df["指标"].astype(str).values:
        row = df[df["指标"].astype(str).str.contains("询盘")].iloc[0]

        diff = row["变化值"]

        if diff > 0:
            st.success(f"📈 询盘上涨：+{diff}")
        else:
            st.error(f"📉 询盘下降：{diff}")
