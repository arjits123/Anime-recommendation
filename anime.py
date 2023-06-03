import streamlit as st
import pickle
import pandas as pd

st.title('Anime Recommender System')
anime = pickle.load(open('anime.pkl', 'rb'))
ratings = pickle.load(open('ratings.pkl', 'rb'))
# rec_percent = pickle.load(open('rec_percent.pkl','rb'))

selected_anime_name = st.selectbox('Please select the anime name you want to watch:', anime['name'].values )
# anime_id =  anime[anime['name'] == selected_anime_name]['anime_id']


def anime_recommendation(anime_name):
    
    animeID =  anime[anime['name'] == anime_name]['anime_id']
    
    # find users similar to us 
    similar_users = ratings[(ratings["anime_id"] == animeID.iloc[0]) & (ratings["rating"] > 8)]["user_id"].unique()
    similar_user_recs = ratings[(ratings["user_id"].isin(similar_users)) & (ratings["rating"] > 8)]["anime_id"]
    
    #percentatge of the user who are similar to us and like the movie
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .20]
    
    # all of the users and there recommendations
    all_users = ratings[ratings["anime_id"].isin(similar_user_recs.index) & (ratings['rating'] > 8)]
    all_users_recs = all_users['anime_id'].value_counts() / len(all_users["user_id"].unique())
    
    # find the percentage
    rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(anime, left_index=True, right_on="anime_id")["cleaned_name"]


if st.button('recommend'):

    recommendations = anime_recommendation(selected_anime_name)
    for i in recommendations:
        st.write(i)
    
    # st.write(selected_anime_name)