import csv
import pandas as pd
import numpy as np

class LoadData:
    ratings_path = "E:\Development work\MovieRecommendation\m2010-2019\mbollywood_ratings_2010-2019.csv"
    movies_path = "E:\Development work\MovieRecommendation\m2010-2019\mbollywood_2010-2019.csv"
    metaData_path = "E:\Development work\MovieRecommendation\m2010-2019\mbollywood_meta_2010-2019.csv"

    metaData = []
    genres = {}
    def loadRatings(self):
        ratings = []
        idList = []
        with open(self.ratings_path, encoding = 'ISO-8859-1', newline = "") as csvFile:
            ratingsReader = csv.reader(csvFile)
            next(ratingsReader)
            for id, rating, vote in ratingsReader:
                if (len(rating) < 1):
                    rating = 0
                if (len(vote) < 1):
                    vote = 0
                if (len(id) < 1 or id in idList):
                    continue
                idList.append(id)
                ratings.append((id, rating, vote))
        ratings = pd.DataFrame(ratings,  columns = ['id', 'ratings', 'votes'])
        ratings.insert(0, "Index", [i for i in range(len(ratings.axes[0]))])
        # ratings.to_csv("E:\Development work\MovieRecommendation\m2010-2019\combined.csv")
        ratings.fillna(0)
        return ratings

    def loadMovieData(self):
        movies = []
        idList = []
        with open(self.movies_path, encoding='ISO-8859-1', newline="") as csvFile:
            moviesReader = csv.reader(csvFile)
            next(moviesReader)
            for title, id, poster_path, wiki_link in moviesReader:
                if (len(id) < 1 or id in idList):
                    continue
                idList.append(id)
                movies.append((title, id, poster_path, wiki_link))
        movies = pd.DataFrame(movies, columns = ['title', 'id', 'poster_path', 'wiki_link'])
        movies.fillna(0)
        return movies

    def loadMetaData(self):
        idList = []
        with open(self.metaData_path, encoding='ISO-8859-1', newline="") as csvFile:
            metaReader = csv.reader(csvFile)
            next(metaReader)
            for id, title, original_title, is_adult, yor, runtime, genres in metaReader:
                if (len (yor) < 1 or not yor.isnumeric()):
                    yor = '0'
                if (len (is_adult) < 1 or not is_adult.isnumeric()):
                    is_adult = '0'
                if (len(id) < 1 or id in idList):
                    continue
                idList.append(id)
                self.metaData.append((id, is_adult, yor, genres))
        metaData = pd.DataFrame(self.metaData, columns=['id','is_adult', 'yor', 'genres'])
        return metaData

