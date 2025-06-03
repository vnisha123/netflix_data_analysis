import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


st.title("🎬 Netflix Data Analysis")


@st.cache_data
def load_data():
    df = pd.read_csv("netflix_data_cleaned.csv")  
    return df

df = load_data()


st.subheader("Dataset Overview")
st.write(f"Total entries: {df.shape[0]}")
st.write(df.head())



st.sidebar.header('Filter Options')


type_filter = st.sidebar.multiselect('Select Type:', options=df['type'].unique(), default=df['type'].unique())


country_filter = st.sidebar.multiselect('Select Country:', options=df['country'].dropna().unique(), default=df['country'].dropna().unique()[:5])


year_filter = st.sidebar.slider('Select Release Year Range:', 
                                int(df['release_year'].min()), 
                                int(df['release_year'].max()), 
                                (int(df['release_year'].min()), int(df['release_year'].max())))


filtered_df = df[
    (df['type'].isin(type_filter)) & 
    (df['country'].isin(country_filter)) & 
    (df['release_year'] >= year_filter[0]) & 
    (df['release_year'] <= year_filter[1])
]


st.subheader('Filtered Dataset')
st.write(f'Showing {filtered_df.shape[0]} records')
st.dataframe(filtered_df.head())

st.subheader('Count of Movies vs TV Shows')
type_counts = filtered_df['type'].value_counts()

fig1, ax1 = plt.subplots()
sns.barplot(x=type_counts.index, y=type_counts.values, palette='Set2', ax=ax1)
ax1.set_ylabel('Count')
st.pyplot(fig1)

st.subheader('Top 10 Countries by Number of Shows')
top_countries = filtered_df['country'].value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, palette='mako', ax=ax2)
ax2.set_xlabel('Number of Shows')
st.pyplot(fig2)


st.subheader('Content Released Per Year')
yearly_data = filtered_df.groupby('release_year').size().reset_index(name='count')
yearly_data = yearly_data.sort_values('release_year')

fig3, ax3 = plt.subplots()
sns.lineplot(data=yearly_data, x='release_year', y='count', marker='o', color='orange', ax=ax3)
ax3.set_ylabel('Number of Titles')
st.pyplot(fig3)


df['genres'] = df['listed_in'].str.split(', ')
all_genres = df['genres'].explode()
top_genres = all_genres.value_counts().head(10)




st.subheader('Top 10 Netflix Genres')


fig, ax = plt.subplots(figsize=(10,6))


sns.barplot(x=top_genres.values, y=top_genres.index, palette='magma', ax=ax)
ax.set_title('Top 10 Netflix Genres')
ax.set_xlabel('Number of Titles')
ax.set_ylabel('Genre')


st.pyplot(fig)


content_trends = df.groupby('release_year')['type'].value_counts().unstack().fillna(0)


fig, ax = plt.subplots(figsize=(12,6))
content_trends.plot(kind='line', ax=ax, marker='o')
ax.set_title('Content Trends Over Time (Movies vs TV Shows)')
ax.set_xlabel('Release Year')
ax.set_ylabel('Count')
st.pyplot(fig)





