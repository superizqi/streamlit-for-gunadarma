import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression

# Format Y-axis Rupiah
def format_rupiah(x, _):
    return f'Rp {x:,.0f}'.replace(',', '.')

st.set_page_config(layout="wide")
st.title("💰 Personal Finance Dashboard")

# Dummy Data
np.random.seed(42)
months = pd.date_range(start='2024-01-01', periods=12, freq='M').strftime('%B')
income = np.random.randint(5_000_000, 15_000_000, size=12)
expense = np.random.randint(3_000_000, 12_000_000, size=12)
savings = income - expense

df = pd.DataFrame({
    'Month': months,
    'Income': income,
    'Expense': expense,
    'Savings': savings
})

# Filter bulan
st.markdown("### 📅 Filter Bulan")
selected_months = st.multiselect(
    "Pilih bulan yang ingin ditampilkan:",
    options=df['Month'].tolist(),
    default=df['Month'].tolist()
)
filtered_df = df[df['Month'].isin(selected_months)]

# Visualisasi - ROW 1
st.subheader("📊 Visualisasi Keuangan")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(filtered_df['Month'], filtered_df['Income'], color='green')
    ax.set_title("Income (Bar)")
    ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.barh(filtered_df['Month'], filtered_df['Expense'], color='red')
    ax.set_title("Expense (BarH)")
    ax.xaxis.set_major_formatter(FuncFormatter(format_rupiah))
    st.pyplot(fig)


col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered_df['Month'], filtered_df['Savings'], marker='o', color='blue')
    ax.set_title("Savings (Line)")
    ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered_df['Month'], filtered_df['Income'], label='Income', marker='o', color='green')
    ax.plot(filtered_df['Month'], filtered_df['Expense'], label='Expense', marker='o', color='red')
    ax.plot(filtered_df['Month'], filtered_df['Savings'], label='Savings', marker='o', color='blue')
    ax.set_title("Income vs Expense vs Savings")
    ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Visualisasi - ROW 2
col5, col6 = st.columns(2)

# with col5:
#     fig, ax = plt.subplots(figsize=(10, 3))
#     ax.scatter(filtered_df['Income'], filtered_df['Expense'], color='purple')
#     ax.set_xlabel("Income")
#     ax.set_ylabel("Expense")
#     ax.set_title("Income vs Expense")
#     ax.xaxis.set_major_formatter(FuncFormatter(format_rupiah))
#     ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
#     st.pyplot(fig)

with col5:
    totals = [
        filtered_df['Income'].sum(),
        filtered_df['Expense'].sum(),
        filtered_df['Savings'].sum()
    ]
    labels = ['Income', 'Expense', 'Savings']
    colors = ['green', 'red', 'blue']
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.pie(totals, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.legend()
    ax.set_title("Distribusi Total")
    ax.axis('equal')
    st.pyplot(fig)

# Summary & Insight
st.subheader("📌 Summary & Insight")
col7, col8 = st.columns(2)

with col7:
    st.markdown("#### 🔍 Statistik")
    if not filtered_df.empty:
        max_saving = filtered_df.loc[filtered_df['Savings'].idxmax()]
        min_saving = filtered_df.loc[filtered_df['Savings'].idxmin()]
        st.metric("📈 Highest Saving", f"Rp {max_saving['Savings']:,.0f}", max_saving['Month'])
        st.metric("📉 Lowest Saving", f"Rp {min_saving['Savings']:,.0f}", min_saving['Month'])
        st.metric("📊 Avg Income", f"Rp {filtered_df['Income'].mean():,.0f}")
        st.metric("📊 Avg Expense", f"Rp {filtered_df['Expense'].mean():,.0f}")
    else:
        st.warning("Tidak ada data setelah filter.")

with col8:
    st.markdown("#### 📌 Insight")
    if not filtered_df.empty:
        avg_saving = filtered_df['Savings'].mean()
        total_income = filtered_df['Income'].sum()
        total_expense = filtered_df['Expense'].sum()
        total_savings = filtered_df['Savings'].sum()
        saving_rate = 100 * total_savings / total_income if total_income else 0

        if avg_saving < 1_000_000:
            msg = "⚠️ Rata-rata tabungan rendah."
        elif avg_saving > 3_000_000:
            msg = "✅ Tabungan sangat baik."
        else:
            msg = "🟡 Cukup baik, bisa ditingkatkan."

        st.success(msg)
        st.markdown(f"""
        - **Total Income**: Rp {total_income:,.0f}  
        - **Total Expense**: Rp {total_expense:,.0f}  
        - **Total Savings**: Rp {total_savings:,.0f}  
        - **Savings Rate**: {saving_rate:.1f}%
        """)
    else:
        st.info("Pilih minimal 1 bulan untuk insight.")

# Prediksi 12 bulan ke depan
# st.subheader("🔮 Prediksi Savings 12 Bulan ke Depan (Linear Regression)")

# df_pred = df.copy()
# df_pred['Month_Num'] = range(1, 13)

# X = df_pred[['Month_Num']]
# y = df_pred['Savings']
# model = LinearRegression()
# model.fit(X, y)

# future_months = pd.date_range(start='2025-01-01', periods=12, freq='M')
# future_nums = np.arange(13, 25).reshape(-1, 1)
# future_savings = model.predict(future_nums)

# pred_df = pd.DataFrame({
#     'Month': future_months.strftime('%b %Y'),
#     'Predicted_Savings': future_savings.astype(int)
# })
# st.dataframe(pred_df)

# Chart prediksi (compact)
# fig, ax = plt.subplots(figsize=(15, 3))
# ax.plot(df_pred['Month_Num'], y, marker='o', label='Actual Savings', color='blue')
# ax.plot(range(13, 25), future_savings, marker='x', linestyle='--', label='Predicted Savings', color='orange')
# ax.set_title("Savings: Aktual & Prediksi 12 Bulan ke Depan")
# ax.set_xlabel("Bulan ke-")
# ax.set_ylabel("Savings")
# ax.yaxis.set_major_formatter(FuncFormatter(format_rupiah))
# ax.legend()
# st.pyplot(fig)
