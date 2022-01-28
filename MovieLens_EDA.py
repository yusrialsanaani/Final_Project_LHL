
  #from google.colab import drive
  #drive.mount('/content/drive')
  #path = '/content/drive/My Drive/Colab Notebooks/Final_Project/data100k/'
import pandas as pd

class MovieLens_EDA:
    
    path = 'C:/Users/Admin/OneDrive - just.edu.jo/Documents/GitHub/DS_Bootcamp/Final Project/Final_Project_LHL/data/data100k/'
    def load_MovieLens(self):
        # Load the movies dataset
        movies = pd.read_csv(path+'movies.csv')
        # Load the ratings dataset
        ratings = pd.read_csv(path+'ratings.csv')
        # Load the links dataset
        links = pd.read_csv(path+'links.csv')
        # Load the tags dataset
        tags = pd.read_csv(path+'tags.csv')
        return (movies, ratings, links, tags)
    
    def get_unique_genres(self,df):
        # Printing unique genres. This is also given in the dataset description file
        genres_unique = pd.DataFrame(df.genres.str.split('|').tolist()).stack().unique()
        return genres_unique
    # Extract the release year fron the movie titles using regular expressions
    def release_year(self,title):
        year=re.search(r'\(\d{4}\)', title)
        if year:
            year=year.group()
            return int(year[1:5])
        else:
            return 0
    # Extract the release year fron the movie titles
    def release_year1(self,df):
        df['release_year'] = df.title.map(lambda x: re.findall('\d\d\d\d', x))
        df.release_year = df.release_year.apply(lambda x: 0 if not x else int(x[-1]))
        return df
  #movies['release_year1'] = movies.title.str.extract("\((\d{4})\)", expand=True).astype(str)
  #movies.sample(20)
    def plot_movies_per_year(self, df, size = (15,3)):
        df = df[['release_year', 'movieId']]
        df = df.groupby(['release_year']).count().reset_index().rename(columns={'release_year':'Year', 'movieId':'Movies #'})
        df.plot.bar('Year', 'Movies #', title='Number of movies released per year', figsize= size);
    def timestamp_convert(self,df):
        df['timestamp'] = df['timestamp'].apply(datetime.datetime.fromtimestamp)
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['date'] = df['timestamp'].dt.date
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df


    def ratings_statistics(self,ratings):
        print(colored('Summary of some statistics for ratings dataset:\n', 'green', attrs=['bold']))
        # Show the unique rating years and months:
        print('The ratings are distributed over {} years from {} to {} as follows:'.format(
            len(ratings.year.unique()),min(ratings.year.unique()),max(ratings.year.unique())))
        print(colored('Years:', 'blue', attrs=['bold']), np.sort(ratings.year.unique()))
        print(colored('Months:', 'blue', attrs=['bold']), np.sort(ratings.month.unique()))
        # Show the unique number of users:
        print('\nNumber of unique users:', ratings.userId.nunique())
        # Show the unique number of movies:
        print('\nNumber of unique movies:', ratings.movieId.nunique())
        # Show the unique ratings:
        print('\nUnique ratings:', np.sort(ratings.rating.unique()))
        # Determine and display the min and max ratings received
        print('\nLowest rating: {}'.format(ratings.rating.min()))
        print('\nHighest rating: {}'.format(ratings.rating.max()))
        print('\nAverage rating:', round(ratings.rating.mean(), 2))
        print('\nFrequency of each rating:\n', ratings['rating'].value_counts())


    def tags_statistics(self,tags):
        print(colored('Summary of some statistics for tags dataset:\n', 'green', attrs=['bold']))
        # Show the unique rating years and months:
        print('The tags are distributed over {} years from {} to {} as follows:'.format(
            len(tags.year.unique()),min(tags.year.unique()),max(tags.year.unique())))
        print(colored('Years:', 'blue', attrs=['bold']), np.sort(tags.year.unique()))
        print(colored('Months:', 'blue', attrs=['bold']), np.sort(tags.month.unique()))
        # Show the unique number of users:
        print('\nNumber of unique users:', tags.userId.nunique())
        # Show the unique number of movies:
        print('\nNumber of unique movies:', tags.movieId.nunique())
        # Show the unique tags:
        print('\nNumber of unique tags :', len(tags.tag.unique()))
    
    def genre_count(self, input_df):
        """
        This function takes in the movies dataframe and cleans the genre column 
        before extracting the unique genres together with their respective
        frequencies in the dataset. This information is then used to create a bar graph
        showing how frequently each genre occurs in the dataset
        """   
        df = input_df.copy()
        dict_count = {}
        # Extract the unique genres
        #all_genres = set(','.join([genres.replace('|',',').lower() for genres in df.genres]).split(','))    
        # Log the frequency of each genre 
        for genre in all_genres:
            dict_count[genre] = ','.join([genres.replace('|',',').lower() for genres in df.genres]).count(genre)
         
        # Sort the genres according to their frequency
        sorted_dict = sorted(dict_count.items(), key=lambda x: x[1],reverse=True)
        genre, frequency = zip(*sorted_dict)
        # Create bar plot 
        fig = plt.figure(4, figsize=(15,10))
        sns.barplot(x=np.array(frequency), y=list(genre), palette='Reds_r')
        #sns.barplot(x=frequency, y=list(genre), palette='Reds_r')
        plt.title('Genre frequency\n',fontsize=25)
        plt.xlabel('Genre_count', fontsize=15)
        plt.ylabel('Genres', fontsize=15)
        plt.show()

  # Sparsity
    def sparsity(self,ratings):
        n_users = ratings['userId'].nunique()
        n_movies = ratings['movieId'].nunique()
        print('number of users: {}\nnumber of movies: {}'.format(n_users, n_movies))
        print('sparsity level is {}%'.format(round((1.0 - len(ratings)/float(n_users*n_movies))*100, 4)))


    def wordcloud_genres(self,genre_data):
        # create a list of the genres
        genre_census = list()
        for each in genre_data:
            string_split = each.split('|')
            for i in string_split:
                genre_census.append(i)
        # create a dictionary where key=genre, value=movie count
        movie_count_by_genre = dict()
        # use for loop to add genres as key
        for i in genre_census:
            movie_count_by_genre[i] = 0
        # using for loop count the number of movies in each genre (with repetition) as values
        for i in genre_census:
            if i in genre_census:
                movie_count_by_genre[i] += 1
        # sort the dictionary based on highest movie count
        total_movie_count = []
        for key,val in movie_count_by_genre.items():
            total_movie_count.append([key,val])
            total_movie_count.sort(key = lambda x:x[1], reverse = True)
        # display the genres by highest movie count
        total_movie_count_list = total_movie_count
        total_movie_count_dict = {}
        for i in total_movie_count_list:
            total_movie_count_dict[i[0]] = i[1]
        # create the wordcloud by movie frequency
        genre_wordcloud = WordCloud(width=1000,height=500, background_color='white')
        genre_wordcloud.generate_from_frequencies(total_movie_count_dict)
        plt.figure(figsize=(12, 9))
        plt.imshow(genre_wordcloud, interpolation="bilinear")
        plt.axis('off')
        return plt.show()


####
def wordcloud_genres(self,genre_data):
    # create a list of the genres
    genre_census = list()
    for each in genre_data:
      string_split = each.split('|')
      for i in string_split:
        genre_census.append(i)
    # create a dictionary where key=genre, value=movie count
    movie_count_by_genre = dict()
    # use for loop to add genres as key
    for i in genre_census:
      movie_count_by_genre[i] = 0
      # using for loop count the number of movies in each genre (with repetition) as values
    for i in genre_census:
      if i in genre_census:
        movie_count_by_genre[i] += 1
    # sort the dictionary based on highest movie count
    total_movie_count = []
    for key,val in movie_count_by_genre.items():
      total_movie_count.append([key,val])
      total_movie_count.sort(key = lambda x:x[1], reverse = True)
    # display the genres by highest movie count
    total_movie_count_list = total_movie_count
    total_movie_count_dict = {}
    for i in total_movie_count_list:
      total_movie_count_dict[i[0]] = i[1]
    # create the wordcloud by movie frequency
    genre_wordcloud = WordCloud(width=1000,height=500, background_color='white')
    genre_wordcloud.generate_from_frequencies(total_movie_count_dict)
    plt.figure(figsize=(12, 9))
    plt.imshow(genre_wordcloud, interpolation="bilinear")
    plt.axis('off')
    return plt.show()
###


    def wordcloud_titles(self, movie_titles):
        # create a series of movie titles and convert each row to string
        movie_titles = movie_titles.astype('str')
        # store all the movie titles
        title_corpus = ''.join(movie_titles)
        # eliminate stopwords and create wordcloud
        title_wordcloud = WordCloud(stopwords=STOPWORDS, width=1000, height=500, background_color='white').generate(title_corpus)
        plt.figure(figsize=(15, 10))
        plt.imshow(title_wordcloud, interpolation="bilinear")
        plt.axis('off')
        plt.show()
    
    
    def rating_des(self,df):
        # Count how many ratings are in each category (1 star, 2 star, ect)
        grouped = pd.DataFrame(df.groupby(['rating'])['title'].count())
        grouped.rename(columns={'title':'rating_count'}, inplace=True)
        pie, ax = plt.subplots(figsize=[15,10])
        labels = ['0.5 Star', '1 Stars', '1.5 Stars', '2 Stars', '2.5 Stars', '3 Star', '3.5 Stars', '4 Stars', '4.5 Stars', '5 Stars']
        plt.pie(x=grouped['rating_count'], autopct="%.1f%%", labels=labels, pctdistance=0.8)
        plt.title("Rating distribution");
  
    def avg_rating(self,df):
        # Determine the average rating and number of ratings for each movie
        ratings_mean_count = pd.DataFrame(df.groupby(['title'])[['rating']].mean())
        ratings_mean_count['rating_counts'] = pd.DataFrame(df.groupby(['title'])['rating'].count())
        ratings_mean_count['popularity'] = pd.DataFrame(df.groupby(['title'])['rating'].count()*df.groupby(['title'])['rating'].mean())
        # Create a plot of the number of ratings 
        f, ax = plt.subplots(figsize=(8,4))
        ax.hist(ratings_mean_count['rating_counts'], bins=70)
        ax.set_title('Number of ratings\n')
        ax.set_yscale('log')
        ax.set_xlabel('Ratings Count')
        ax.set_ylabel('Frequency')

        f, ax = plt.subplots(figsize=(8,4))
        # Create a plot showing the average ratings distribution 
        ax.hist(ratings_mean_count['rating'], bins=10)
        ax.set_title('Average ratings\n')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Frequency')

        f, ax = plt.subplots(figsize=(8,4))
        # Create a plot showing the average ratings distribution 
        ax.hist(ratings_mean_count['popularity'], bins=100)
        ax.set_title('popularity\n')
        ax.set_xlabel('popularity')
        ax.set_ylabel('Frequency')
        ax.set_yscale('log')
        plt.tight_layout()
        plt.show()
        return ratings_mean_count
  
  # Which are the most popular movies?
  # We can take a weighted score taking into account both the ratings and the amount of views to answer this question:
    def weighted_average_score(self,df, k=0.8):
        n_views = df.groupby('movieId', sort=False).movieId.count()
        ratings = df.groupby('movieId', sort=False).rating.mean()
        scores = ((1-k)*(n_views/n_views.max()) + 
                  k*(ratings/ratings.max())).to_numpy().argsort()[::-1]
        df_deduped = df.groupby('movieId', sort=False).agg({'title':'first', 
                                                         'genres':'first', 
                                                         'rating':'mean'})
        return df_deduped.assign(views=n_views).iloc[scores]


