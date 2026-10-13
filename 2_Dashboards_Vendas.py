import streamlit as st
import pandas as pd 
import plotly.express as px

st.title("📊 Dashboard de Vendas - Olist")
st.markdown("** Problema:** Onde estáa receita e como está a satisfação do cliente?")

df = pd.read_csv("data/pedidos.csv", parse_dates=["data_compra"])

regioes = st.multiselect("Região", df["regiao"].unique(),
                         default=list(df["regiao"].unique()))
df_f = df[df["regiao"].isin(regioes)]

c1,c2,c3 = st.column_config(3)
c1.metric("Receita", f"R$ {df_f['valor'].sum():,.0f}")
c2.metric("Pedidos", f"{len(df_f):,}")
c3.metric("Ticket médio", f"R$ {df_f['valor'].mean():,.2f}")
mensal = df_f.groupby(df_f["data_compra"].dt.to_period("M"))["valor"].sum().reset_index()
mensal["data_compra"] = mensal["data_compra"].astype(str)
st.plotly_chart(px.line(mensal, x="data_compra", y="valor", markers=True))