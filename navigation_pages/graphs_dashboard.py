import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


st.header("Analytics Dashboard")
st.caption("View trends in your invoice data")
df = pd.read_csv("/Users/yohan/Documents/Minor Project/InvoiceGPT/navigation_pages/Final_Invoice.csv")

payment_counts = df['payment_method'].value_counts().reset_index()
payment_counts.columns = ['payment_method', 'count']

# Create a bar chart using Plotly
fig = px.bar(payment_counts, x='payment_method', y='count',
             title='Payment Method Distribution',
             labels={'payment_method': 'Payment Method', 'count': 'Count'},
             color='count',  # Color by mean tax value
             color_continuous_scale=px.colors.sequential.Viridis,
             text='count' )
fig.update_traces(texttemplate='%{text}', textposition='outside')  # Place text outside the bars

# Display the plot in Streamlit
st.plotly_chart(fig)


df['invoice_date'] = pd.to_datetime(df['invoice_date'])
df = df.sort_values(by='invoice_date')

# Create the line chart using Plotly
fig = px.line(df, x='invoice_date', y='net_total', title='Sub Total Over Time',
              labels={'invoice_date': 'Invoice Date', 'net_total': 'Net Total'}, markers=True)

# Show the plot
st.plotly_chart(fig)


df['products_services'] = df['products_services'].str.split(', ')
df = df.explode('products_services')

# Count the occurrences of each product/service
item_counts = df['products_services'].value_counts().reset_index()
item_counts.columns = ['item', 'count']

# Create a pie chart using Plotly
fig = px.pie(item_counts, names='item', values='count', title='Distribution of Products/Services')

st.plotly_chart(fig)



# Split the 'products_services' column into individual items and explode it into separate rows
df['products_services'] = df['products_services'].str.split(', ')
df = df.explode('products_services')

# Calculate mean tax for each item
mean_tax = df.groupby('products_services')['tax'].mean().reset_index()
mean_tax.columns = ['item', 'mean_tax']  # Renaming columns for clarity

# Sort the mean tax DataFrame in descending order
mean_tax = mean_tax.sort_values(by='mean_tax', ascending=False)

# Create a bar chart using Plotly
fig = px.bar(mean_tax, x='item', y='mean_tax', title='Mean Tax of Each Product',
             labels={'item': 'Product', 'mean_tax': 'Mean Tax'},
             color='mean_tax',  # Color by mean tax value
             color_continuous_scale=px.colors.sequential.Viridis,
             text=mean_tax['mean_tax'].map(lambda x: f"{x:.2f}")  # Format to 2 decimal places
            )

# Update text labels and layout
fig.update_traces(texttemplate='%{text}', textposition='outside')  # Keep text outside bars
fig.update_layout(width=1000)


# Show the bar chart
st.plotly_chart(fig)


df['products_services'] = df['products_services'].str.split(', ')
df = df.explode('products_services')

# Calculate total discount for each product
total_discount = df.groupby('products_services')['discount'].sum().reset_index()

# Rename the columns for clarity
total_discount.columns = ['Product', 'Total Discount']

# Sort the total_discount DataFrame in descending order
total_discount = total_discount.sort_values(by='Total Discount', ascending=False)

# Create a bar chart using Plotly
fig = px.bar(total_discount, x='Product', y='Total Discount',
             title='Total Discount Given to Each Product',
             labels={'Product': 'Product', 'Total Discount': 'Total Discount'},
             color='Total Discount',  # Color by total discount value
             color_continuous_scale=px.colors.sequential.Viridis,
             text=total_discount['Total Discount'].map(lambda x: f"{x:.2f}"))

fig.update_traces(texttemplate='%{text}', textposition='outside')  # Keep text outside bars

# Show the plot in Streamlit
st.plotly_chart(fig)


