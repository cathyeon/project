import pandas
from sklearn import train_test_split

#from medium article https://towardsdatascience.com/how-to-build-a-simple-song-recommender-296fcbc8c85

#these lines of code did not work on IDE
#triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
#songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'
#song_df_1 = pandas.read_table(triplets_file,header=None)
#song_df_1.columns = ['user_id', 'song_id', 'listen_count']
#song_df_2 =  pandas.read_csv(songs_metadata_file)
#song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")
#print('Data imported')

song_df = pandas.read_csv('song_df.csv')
print(song_df.head())
users = song_df['user_id'].unique()
print(len(users))
songs = song_df['song_id'].unique()
print(len(songs))
train_data, test_data = train_test_split(song_df, test_size = 0.20, random_state=0)
