import numpy as np
from sklearn import datasets, neighbors
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
from random import randint
import time

def lets_knn(X_train, y_train, X_test, y_test, n_neighbors=3, weights='uniform', print_wrong_pred=False):
    t0 = time.time()
    # creating and training knn classifier
    knn = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
    knn.fit(X_train, y_train)
    t1 = time.time()

    # predicting classes and comparing them with actual labels
    pred = knn.predict(X_test)
    t2 = time.time()
    # calculating accuracy
    accuracy = round(np.mean(pred == y_test)*100, 1)

    print("Accuracy of", weights ,"KNN with", n_neighbors, "neighbors:", accuracy,"%. Fit in",
          round(t1 - t0, 1), "s. Prediction in", round(t2 - t1, 1), "s")

    # selecting wrong predictions with correct and wrong labels
    wrong_pred = X_test[(pred != y_test)]
    correct_labels = y_test[(pred != y_test)]
    wrong_labels = pred[(pred != y_test)]

    if print_wrong_pred:
        # the we print first 16 of them
        fig = plt.figure()
        fig.suptitle("Incorrect predictions", fontsize=18)
        pics_count = 0
        # in order to print different sized photos, we need to determine to what shape we want to reshape
        size = int(np.sqrt(X_train.shape[1]))
        for n, (digit, wrong_label, correct_label) in enumerate(zip(wrong_pred, wrong_labels, correct_labels)):
            a = fig.add_subplot(4, 4, n + 1)
            plt.imshow(digit.reshape(size,size))
            a.set_title("Correct: " + str(correct_label) + ". Predicted: " + str(wrong_label))
            a.axis('off')
            pics_count +=1
            if n == 15:
                break
        fig.set_size_inches(fig.get_size_inches() * pics_count / 7)
        plt.show()

X, y = datasets.load_digits(return_X_y=True)

# check data shapes - data is already flattened
print("X shape:", X.shape[0:])
print("y shape:", y.shape[0:])

# pics_count = 16
# digits = np.zeros((pics_count,8,8), dtype=int)
# labels = np.zeros((pics_count,1), dtype=int)
# for i in range(pics_count):
#   idx = randint(0, X.shape[0]-1)
#   # as data is flattened we need them to be reshaped to the original 2D shape
#   digits[i] = X[idx].reshape(8,8)
#   labels[i] = y[idx]
#
# # then we print them all
# fig = plt.figure()
# fig.suptitle("A sample from the original dataset", fontsize=18)
# for n, (digit, label) in enumerate(zip(digits, labels)):
#   a = fig.add_subplot(4, 4, n + 1)
#   plt.imshow(digit)
#   a.set_title(label[0])
#   a.axis('off')
# fig.set_size_inches(fig.get_size_inches() * pics_count / 7)
# plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print("X train shape:", X_train.shape)
print("y train shape:", y_train.shape)
print("X test shape:", X_test.shape)
print("y test shape:", y_test.shape)

# lets_knn(X_train, y_train, X_test, y_test)


# # проверим данный метод на датасете  mnist
#
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
#
# X_train = X_train.reshape((-1, 28*28))
# X_test = X_test.reshape((-1, 28*28))
#
# # checking shapes
# print("X train shape:", X_train.shape)
# print("y train shape:", y_train.shape)
# print("X test shape:", X_test.shape)
# print("y test shape:", y_test.shape)

for weights in ['uniform', 'distance']:
  for n in range(1,11):
     lets_knn(X_train, y_train, X_test, y_test, n_neighbors=n, weights=weights, print_wrong_pred=True)
