import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Olympic_cleaned.csv")

st.title("Olympics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

# Year filter
year_options = ["All"] + sorted(df['Year'].unique().tolist())
year = st.sidebar.selectbox("Select Year", year_options)

# Apply year filter
if year == "All":
    df_year = df
else:
    df_year = df[df['Year'] == year]

# Country filter using NOC (real Olympic countries)
country_options = ["All"] + sorted(df_year['NOC'].dropna().unique().tolist())
country = st.sidebar.selectbox("Select Country", country_options)

# Apply country filter
if country == "All":
    df_filtered = df_year
else:
    df_filtered = df_year[df_year['NOC'] == country]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Athletes", df_filtered['Name'].nunique())
col2.metric("Total Sports", df_filtered['Sport'].nunique())
col3.metric("Total Countries", df_filtered['NOC'].nunique())
col4.metric("Total Events", df_filtered['Event'].nunique())

st.divider()

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(df_filtered)

# Top Sports Chart
st.subheader("Top 10 Sports")

top_sports = df_filtered['Sport'].value_counts().head(10)

fig1, ax1 = plt.subplots(figsize=(8,4))
ax1.bar(top_sports.index, top_sports.values, width=0.4, color="#4B9CD3")
ax1.set_ylabel("Number of Athletes")
ax1.set_xlabel("Sport")
plt.xticks(rotation=45)

st.pyplot(fig1)

# Medal Distribution
st.subheader("Medal Distribution")

medal_counts = df_filtered['Medal'].value_counts()

fig2, ax2 = plt.subplots(figsize=(6,4))
ax2.bar(medal_counts.index, medal_counts.values,
        width=0.4,
        color=['gold','silver','#cd7f32'])

ax2.set_ylabel("Count")
ax2.set_xlabel("Medal Type")

st.pyplot(fig2)

# Gender Distribution
st.subheader("Gender Distribution")

gender_counts = df_filtered['Sex'].value_counts()

fig3, ax3 = plt.subplots(figsize=(6,4))
ax3.bar(gender_counts.index, gender_counts.values,
        width=0.4,
        color=['#FF6B6B','#4B9CD3'])

ax3.set_ylabel("Number of Athletes")
ax3.set_xlabel("Gender")

st.pyplot(fig3)

# Top Countries by Medals
st.subheader("Top 10 Countries by Medals")

top_countries = df_filtered[df_filtered['Medal'].notna()]['NOC'].value_counts().head(10)

fig4, ax4 = plt.subplots(figsize=(8,4))
ax4.bar(top_countries.index, top_countries.values, width=0.4, color="#FF8C42")

ax4.set_xlabel("Country")
ax4.set_ylabel("Medals")

plt.xticks(rotation=45)

st.pyplot(fig4)

# Age Distribution
st.subheader("Age Distribution")

fig5, ax5 = plt.subplots(figsize=(6,4))
ax5.hist(df_filtered['Age'].dropna(), bins=20, color="#4B9CD3")

ax5.set_xlabel("Age")
ax5.set_ylabel("Number of Athletes")

st.pyplot(fig5)

# Sports with Most Medals
st.subheader("Sports with Most Medals")

sport_medals = df_filtered[df_filtered['Medal'].notna()]['Sport'].value_counts().head(10)

fig6, ax6 = plt.subplots(figsize=(8,4))
ax6.bar(sport_medals.index, sport_medals.values, width=0.4, color="#6A5ACD")

ax6.set_xlabel("Sport")
ax6.set_ylabel("Medals")

plt.xticks(rotation=45)

st.pyplot(fig6)

st.subheader("Medal Table")

medal_table = df_year[df_year['Medal'].notna()].groupby('Team')['Medal'].value_counts().unstack().fillna(0)

st.dataframe(medal_table.sort_values(by='Gold', ascending=False))


st.subheader("Medals Over Years")

medals_year = df[df['Medal'].notna()].groupby('Year').size()

fig, ax = plt.subplots()

ax.plot(medals_year.index, medals_year.values, color="purple")

ax.set_xlabel("Year")
ax.set_ylabel("Total Medals")

st.pyplot(fig)


st.subheader("Top Athletes With Most Medals")

top_athletes = df[df['Medal'].notna()]['Name'].value_counts().head(10)

st.bar_chart(top_athletes)


st.subheader("Sport Participation")

sport_counts = df_filtered['Sport'].value_counts().head(10)

st.bar_chart(sport_counts)    


st.subheader("Height vs Weight")

fig, ax = plt.subplots()

ax.scatter(df_filtered['Height'], df_filtered['Weight'], alpha=0.5)

ax.set_xlabel("Height")
ax.set_ylabel("Weight")

st.pyplot(fig)