import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 AI询盘分析系统（修复稳定版）")

file = st.file_uploader("上传Excel", type=["xlsx"])

if file:

    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, "分析总表")

    st.subheader("📌 原始数据")
    st.dataframe(df)

    # =========================
    # 1. 删除全空列（关键修复）
    # =========================
    df = df.dropna(axis=1, how="all")

    # =========================
    # 2. 删除全空行
    # =========================
    df = df.dropna(axis=0, how="all")

    # =========================
    # 3. 强制把数值列转数字
    # =========================
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # =========================
    # 4. 找最后两行（24周 vs 23周）
    # =========================
    numeric_df = df.select_dtypes(include=[np.number])

    if len(numeric_df) < 2:
        st.error("❌ 数据不足两行")
        st.stop()

    last = numeric_df.iloc[-1]
    prev = numeric_df.iloc[-2]

    # =========================
    # 5. 自动计算变化
    # =========================
    result = []

    for col in numeric_df.columns:

        now = last[col]
        before = prev[col]

        diff = now - before

        pct = (diff / before * 100) if before != 0 else None

        result.append({
            "指标": col,
            "24周": now,
            "23周": before,
            "变化值": diff,
            "变化率%": pct
        })

    result_df = pd.DataFrame(result)

    # =========================
    # 6. 输出
    # =========================
    st.subheader("📊 对比分析结果")

    st.dataframe(result_df.sort_values("变化值", ascending=False))

    # =========================
    # 7. 自动结论
    # =========================
    st.subheader("🧠 AI结论")

    # 找询盘
    inquiry_cols = [c for c in numeric_df.columns if "询盘" in str(c)]

    if inquiry_cols:
        col = inquiry_cols[0]
        diff = last[col] - prev[col]

        if diff > 0:
            st.success(f"📈 询盘上涨 +{diff}")
        else:
            st.error(f"📉 询盘下降 {diff}")
    else:
        st.warning("⚠️ 未找到询盘字段")
