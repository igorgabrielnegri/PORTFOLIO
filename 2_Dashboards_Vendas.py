import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Dashboard de Vendas — Olist")
st.markdown("**Problema:** onde está a receita e como está a satisfação do cliente?")

# 1. Carregamento — caminhos reais aqui
pedidos = pd.read_csv("data/olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
itens = pd.read_csv("data/olist_order_items_dataset.csv")
produtos = pd.read_csv("data/olist_products_dataset.csv")
clientes = pd.read_csv("data/olist_customers_dataset.csv")
avaliacoes = pd.read_csv("data/olist_order_reviews_dataset.csv")

# 2. Base consolidada
base = (
    itens
    .merge(pedidos[["order_id", "order_status", "order_purchase_timestamp", "customer_id"]], on="order_id")
    .merge(produtos[["product_id", "product_category_name"]], on="product_id")
    .merge(clientes[["customer_id", "customer_state"]], on="customer_id")
    .merge(avaliacoes[["order_id", "review_score"]].drop_duplicates("order_id"), on="order_id")
)
base = base[base["order_status"] == "delivered"].copy()

# 3. Filtro interativo
estados = st.multiselect("Estado (UF)", base["customer_state"].unique(),
                         default=list(base["customer_state"].unique()))
base_f = base[base["customer_state"].isin(estados)]

# 4. KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Receita", f"R$ {base_f['price'].sum():,.0f}")
c2.metric("Pedidos", f"{base_f['order_id'].nunique():,}")
c3.metric("Nota média", f"{base_f['review_score'].mean():.2f}")

# 5. Gráfico mensal
mensal = base_f.groupby(base_f["order_purchase_timestamp"].dt.to_period("M"))["price"].sum().reset_index()
mensal["order_purchase_timestamp"] = mensal["order_purchase_timestamp"].astype(str)
st.plotly_chart(px.line(mensal, x="order_purchase_timestamp", y="price", markers=True))