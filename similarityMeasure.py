from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import math
from loadData import LoadData
class Similarity:

    ml = LoadData()

    def Cosine_Similarity(self, data):
        combined_features = pd.DataFrame(self.ml.combined_features(data).items(), columns = ['id', 'combined_features'])
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(combined_features["combined_features"])
        similarity_scores = cosine_similarity(X)
        print("...done")
        return similarity_scores


    def computeSimilarity(self, data):
        genres = self.getGenres(data)
        self.similarities = np.zeros((len(data.index), len(data.index)))

        for i in range(len(data.index)):
            if (i % 100 == 0):
                print(i, "of", len(data.index))
            for j in range(i + 1, len(data.index)):
                yearSim = self.yearSimilarity(int(data["yor"][i]), int(data["yor"][j]))
                genreSimilarity = self.genreSimilarity(data["id"][i], data["id"][j], genres)
                self.similarities[i, j] = yearSim * genreSimilarity
                self.similarities[j, i] = self.similarities[i, j]
        print("..done")
        return self.similarities

    def voteRatingSimilarity(self, data):
        self.similarities = np.zeros((len(data.index), len(data.index)))
        for i in range(len(data.index)):
            if (i % 100 == 0):
                print(i, "of", len(data.index))
            for j in range(i + 1, len(data.index)):
                voteSim = self.votesSimilarity(int(data["votes"][i]), int(data["votes"][j]))
                ratingSimilarity = self.ratingsSimilarity(float(data["ratings"][i]), float(data["ratings"][j]))
                isAdult = 0.8
                if (int(data["is_adult"][i])  == int(data["is_adult"][j])):
                    isAdult = 1
                self.similarities[i, j] = voteSim * ratingSimilarity * isAdult
                self.similarities[j, i] = self.similarities[i, j]
        print("..done")
        return self.similarities

    def overallSimilarity(self, data):
        genres = self.getGenres(data)
        self.similarities = np.zeros((len(data.index), len(data.index)))

        for i in range(len(data.index)):
            if (i % 100 == 0):
                print(i, "of", len(data.index))
            for j in range(i + 1, len(data.index)):
                yearSim = self.yearSimilarity(int(data["yor"][i]), int(data["yor"][j]))
                genreSimilarity = self.genreSimilarity(data["id"][i], data["id"][j], genres)
                voteSim = self.votesSimilarity(int(data["votes"][i]), int(data["votes"][j]))
                ratingSimilarity = self.ratingsSimilarity(float(data["ratings"][i]), float(data["ratings"][j]))
                isAdult = 0.7
                if (int(data["is_adult"][i]) == int(data["is_adult"][j])):
                    isAdult = 1
                self.similarities[i, j] = yearSim * genreSimilarity * voteSim * ratingSimilarity * isAdult
                self.similarities[j, i] = self.similarities[i, j]
        print("..done")
        return self.similarities

    def yearSimilarity(self, startMovie, otherMovie):
        diff = abs(startMovie - otherMovie)
        sim = math.exp(-diff / 10.0)
        return sim

    def votesSimilarity(self, startMovie, otherMovie):
        diff = abs(startMovie - otherMovie)
        sim = math.exp(-diff / 10000.0)
        return sim

    def ratingsSimilarity(self, startMovie, otherMovie):
        diff = abs(startMovie - otherMovie)
        sim = math.exp(-diff / 3.0)
        return sim

    def genreSimilarity(self, movie1, movie2, genres):
        genres1 = genres[movie1]
        genres2 = genres[movie2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(genres1)):
            x = genres1[i]
            y = genres2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y

        return sumxy/math.sqrt(sumxx * sumyy)

    def getGenres(self, metaData):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        for i in range(len(metaData.index)):
            movieID = metaData["id"][i]
            genreList = metaData["genres"][i].split("|")
            genreIDList = []
            for genre in genreList:
                if genre in genreIDs:
                    genreID = genreIDs[genre]
                else:
                    genreID = maxGenreID
                    genreIDs[genre] = genreID
                    maxGenreID += 1
                genreIDList.append(genreID)
            genres[movieID] = genreIDList

        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (movieID, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[movieID] = bitfield

        return genres