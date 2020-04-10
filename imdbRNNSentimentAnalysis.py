from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.datasets import imdb
from tensorflow.python.keras.layers import LSTM

print("Loading the data...")
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words = 2000)

x_train = sequence.pad_sequences(x_train, maxlen = 80)
x_test = sequence.pad_sequences(x_test, maxlen = 80)

model = Sequential()
model.add(Embedding(20000, 128))
model.add(LSTM(128, dropout = 0.2, recurrent_dropout = 0.2))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(loss ="binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])
model.fit(x_train, y_train, batch_size = 32, epochs = 10, validation_data = (x_test, y_test), verbose = 2)


score, acc = model.evaluate(x_test, y_test, batch_size = 32, verbose = 2)
