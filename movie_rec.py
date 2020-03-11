# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt 

column_names=["user_id","item_id","rating","timestamp"]
df=pd.read_csv("file.tsv",sep='\t',names=column_names)

movie_titles=pd.read_csv("Movie_Id_Titles.csv")
data=pd.merge(df,movie_titles,on="item_id")
data=data.drop(["timestamp"],axis=1)

#group movies by title and calculate the mean of the ratings for a movie
#data.groupby("title")["rating"].mean().sort_values(ascending=True)

#group movies title and count number of ratings received by the movie
#data.groupby("title")["rating"].count().sort_values(ascending=True)

ratings=pd.DataFrame(data.groupby("title")["rating"].mean())
ratings["No. of ratings"]=pd.DataFrame(data.groupby("title")["rating"].count())

plt.figure(figsize=(10,4))
plt.title("Rating count",loc="right")
ratings["No. of ratings"].hist(bins=70)

plt.figure(figsize=(10,4))
plt.title("Mean Rating",loc="left")
ratings["rating"].hist(bins=70)

#finding correlation
moviemat=pd.pivot_table(data,index="user_id",columns="title",values="rating",)
seconds_1994_ratings=moviemat['8 Seconds (1994)']
similar_seconds_1994_ratings=moviemat.corrwith(seconds_1994_ratings)

corr_seconds=pd.DataFrame(similar_seconds_1994_ratings,columns=["Correlation"])
#corr_seconds.dropna()