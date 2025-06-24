import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("💰 Personal Finance Dashboard")


st.subheader("📊 Visualization")
col1, col2 = st.columns(2)

df = pd.read_csv("personal_financial_data.csv")
df['Jumlah'] = df['Jumlah'].astype(float)
df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date

# --- 1. Line chart: Total expense per month ---
monthly_expense = df[df['Tipe'] == 'Pengeluaran'].groupby('Bulan')['Jumlah'].sum().reset_index()

with col1:
    fig = plt.figure(figsize=(10, 4))
    plt.ticklabel_format(style='plain', axis='y') # to show value in label y
    plt.plot(monthly_expense['Bulan'], monthly_expense['Jumlah'], marker='o', linestyle='-')
    plt.title('Total Monthly Expenses')
    plt.xlabel('Month Date')
    plt.ylabel('Amount (Rp)')
    # plt.tight_layout()
    plt.show()
    st.pyplot(fig)

# --- 2. Multi-line chart: Expense vs Income per month  ---
df_summary = df.groupby(['Bulan', 'Tipe'])['Jumlah'].sum().reset_index()
df_summary.head()

with col2:
    fig = plt.figure(figsize=(10, 4))
    plt.ticklabel_format(style='plain', axis='y') # to show value in label y
    plt.plot(df_summary[df_summary['Tipe'] == 'Pemasukan']['Bulan'], df_summary[df_summary['Tipe'] == 'Pemasukan']['Jumlah'],label='Income')
    plt.plot(df_summary[df_summary['Tipe'] == 'Pengeluaran']['Bulan'], df_summary[df_summary['Tipe'] == 'Pengeluaran']['Jumlah']*-1,label='Expense')
    plt.title('Income vs Expense Per Month')
    plt.xlabel('Date')
    plt.ylabel('Amount (Rp)')
    plt.legend()
    # plt.tight_layout()
    plt.show()
    st.pyplot(fig)


col3,col4,col5 = st.columns(3)

#  Expense proportion by category ---
category_sum = df[df['Tipe'] == 'Pengeluaran'].groupby('Kategori')['Jumlah'].sum().reset_index()
category_sum.head()

with col3:
    fig = plt.figure(figsize=(4, 3))
    plt.pie(category_sum['Jumlah']*-1, labels=category_sum['Kategori'], autopct='%1.1f%%', startangle=90)
    plt.title('Expense Distribution by Category')
    plt.show()  
    st.pyplot(fig)

category_sum = df[df['Tipe'] == 'Pemasukan'].groupby('Kategori')['Jumlah'].sum().sort_values()

with col4:
    fig = plt.figure(figsize=(4,3))
    plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90)
    plt.title('Income Distribution by Category')  
    st.pyplot(fig)

df_summary = df[df['Tipe'] == 'Pengeluaran'].groupby('Kategori')['Jumlah'].sum().reset_index()
df_summary.head()

with col5:
    fig = plt.figure(figsize=(4, 3))
    plt.ticklabel_format(style='plain', axis='y') # to show value in label y
    plt.bar(df_summary['Kategori'], df_summary['Jumlah'])
    plt.title('Total Expenses by Category')
    plt.ylabel('Amount (Rp)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
st.subheader("📌 Summary & Insight")