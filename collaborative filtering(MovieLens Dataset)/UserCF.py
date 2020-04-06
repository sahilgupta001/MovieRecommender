import heapq
from collections import defaultdict
from operator import itemgetter

from MovieLens import MovieLens
from surprise import KNNBasic
from surprise import KNNBaseline
from surprise import KNNWithMeans

#Load the ratings dataset from the load module
print("Loading the ratings data...")
ml = MovieLens()
ratings = ml.loadMovieLensLatestSmall()


# Preparing the trainset of full dataset
print("\nPreparing the full train set of the data...\n")
trainset = ratings.build_full_trainset()


# Preparing the simlarity function
sim_options = {'name': 'cosine',
               'user_based': True}
model = KNNBasic(sim_options = sim_options)
# model = KNNBaseline(sim_options = sim_options)
# model = KNNWithMeans(sim_options = sim_options)
model.fit(trainset)
similarity_scores = model.compute_similarities()

# Computing the top N recommendations

# Choosing the user to test for recommendations
print("\nChoosing the user for recommendations...")
userId = '85'
k = 10 #

# Finding the calculated similarities for the choosen user
print("\nFinding the calculated similarities for the choosen user")
similar_users = heapq.nlargest(k, list(enumerate(similarity_scores[int(userId)])), key = lambda x: x[1])

# Recommending on the basis of Cosine Similarity
print("\nCalculating the ratings by checking for the similar users who rated the item...")
candidates = defaultdict(float)
for user in similar_users:
    index = user[0]
    similarity_score = user[1]
    theirRatings = trainset.ur[index]
    for rating in theirRatings:
        candidates[rating[0]] += (rating[1] / 5.0) * similarity_score

# Mark the movies that the user has already watched
print("\nRemoving the movies that the user has already watched...")
watched = {}
for itemId, ratings in trainset.ur[userId]:
    watched[itemId] = 1

# Get the top-rated items from the ssimilar users
print("\nWe Recommend...\n")
pos = 0
for itemId, rating in sorted(candidates.items(), key = itemgetter(1), reverse = True):
    if not itemId in watched:
        movieId = trainset.to_raw_iid(itemId)
        print(ml.getMovieName(int(movieId)), rating)
        pos += 1
        if (pos > 9):
            break


