from loadData import LoadData
from similarity import Similarity

# Function 1
def get_index_from_id(id):
    return final_data[final_data.id == id]["Index"].values[0]
# Function 2
def get_title_from_index(index):
    return final_data[final_data.index == index]["title"].values[0]

#======================================================
# Main processing
#======================================================

# Reading the ratingset into a dataframe
ml = LoadData()
print("\nLoading the ratings data ...")
ratings = ml.loadRatings()

# Loading the movies data
print("\nLoading the movies data...")
movies = ml.loadMovieData()

# Loading the meta data of the movies
print("\nLoading the movies metadata...")
moviesMeta = ml.loadMetaData()

# Cleaning the data
print ("\nJoining and cleaning the data...")
data = ratings.join(movies.set_index('id'), on = 'id')
final_data = data.join(moviesMeta.set_index('id'), on = 'id')
for column in final_data.columns:
    final_data[column] = final_data[column].fillna('0')

#======================================================================
# Uncomment the line below to save the combined dataframe in a csv fileS
# final_data.to_csv("E:\Development work\MovieRecommendation\m2010-2019\combined.csv")
#======================================================================

# Users choice
movie_user_likes = "tt8291224"


#========================================================================
# Compute the similarity on the basis of genres and year-of-release
#========================================================================

print("\nComputing the similarity matrix for genre and year-of-release...")
sim = Similarity()
similarity_scores = sim.computeSimilarity(final_data)

print("\nPreparing recommendation List...")
movie_index = get_index_from_id(movie_user_likes)
similar_movie_albums = sorted(list(enumerate(similarity_scores[int(movie_index)])), key = lambda x:x[1], reverse = True)

print("\nOn the basis of genre and year-of-release")
print("\nWe Recommend...")
i = 0
for movie in similar_movie_albums:
    print(get_title_from_index(movie[0]))
    i += 1
    if (i >= 50):
        break

#=========================================================================
# Computing the similarity matrix for ratings and number of votes
#=========================================================================
print("\nComputing the similarity matrix for votes and ratings...")
sim = Similarity()
similarity_scores = sim.voteRatingSimilarity(final_data)

print("\nPreparing recommendation List...")
movie_index = get_index_from_id(movie_user_likes)
similar_movie_albums = sorted(list(enumerate(similarity_scores[int(movie_index)])), key=lambda x: x[1], reverse=True)
print("\nOn the basis of ratings and number of votes")
print("\nWe Recommend...")
i = 0
for movie in similar_movie_albums:
    print(get_title_from_index(movie[0]))
    i += 1
    if (i >= 50):
        break

# =========================================================================
# Computing the combined similarity matrix
# =========================================================================
print("\nComputing the combined similarity matrix...")
sim = Similarity()
similarity_scores = sim.overallSimilarity(final_data)

print("\nPreparing recommendation List...")
movie_index = get_index_from_id(movie_user_likes)
similar_movie_albums = sorted(list(enumerate(similarity_scores[int(movie_index)])), key=lambda x: x[1], reverse=True)
print("\nOn combined similarity basis")
print("\nWe Recommend...")
i = 0
for movie in similar_movie_albums:
    print(get_title_from_index(movie[0]))
    i += 1
    if (i >= 50):
        break






        # def combine_features(row):
        #     return str(row["ratings"]) + " " + str(row["votes"]) + " " + str(row["yor"]) + " " + str(row["is_adult"])
        #
        # final_data["combined_features"] = final_data.apply(combine_features, axis = 1)
        # vectorizer = CountVectorizer()
        # X = vectorizer.fit_transform(final_data["combined_features"])
        #
        # similarity_scores = cosine_similarity(X)
