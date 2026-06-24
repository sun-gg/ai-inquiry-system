import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI询盘对比系统V1", layout="wide")

st.title("📊 AI询盘周对比分析系统（V1稳定版）")

file = st.file_uploader("上传Excel（分析总表）", type=["xlsx"])

if file:

    # =====================
    # 1. 读取数据
    # =====================
    xls = pd.ExcelFile(file)

    df = pd.read_excel(xls, "分析总表")

    st.subheader("📌 原始数据预览")
    st.dataframe(df)

    # =====================
    # 2. 自动识别“指标列结构”
    # =====================
    if "指标" not in df.columns:
        st.error("❌ 找不到【指标】列，请检查Excel结构")
        st.stop()

    # =====================
    # 3. 清洗数据
    # =====================
    df["24周"] = pd.to_numeric(df["24周"], errors="coerce")
    df["23周"] = pd.to_numeric(df["23周"], errors="coerce")

    # =====================
    # 4. 计算核心变化
    # =====================
    df["变化值"] = df["24周"] - df["23周"]

    # 防止除0
    df["变化率%"] = np.where(
        df["23周"] != 0,
        (df["变化值"] / df["23周"]) * 100,
        None
    )

    # =====================
    # 5. 排序（找重点变化）
    # =====================
    df_sorted = df.sort_values("变化值", ascending=False)

    # =====================
    # 6. 展示结果
    # =====================
    st.subheader("📊 24周 vs 23周 对比结果")

    st.dataframe(
        df_sorted[["指标", "24周", "23周", "变化值", "变化率%"]]
    )

    # =====================
    # 7. AI简易结论（规则版）
    # =====================
    st.subheader("🧠 自动结论")

    inquiry_row = df[df["指标"].str.contains("询盘", na=False)]

    if not inquiry_row.empty:

        now = inquiry_row["24周"].values[0]
        prev = inquiry_row["23周"].values[0]

        diff = now - prev

        if diff > 0:
            st.success(f"📈 询盘上涨：+{diff}")
        elif diff < 0:
            st.error(f"📉 询盘下降：{diff}")
        else:
            st.warning("⚠️ 询盘无变化")

    # =====================
    # 8. Top变化指标
    # =====================
    st.subheader("🔥 变化最大指标TOP5")

    st.dataframe(df_sorted.head(5))
