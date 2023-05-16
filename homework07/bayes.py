import math
import re
from collections import defaultdict


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.classes = []
        self.word_counts = defaultdict(lambda: defaultdict(int))
        self.class_counts = defaultdict(int)
        self.total_counts = defaultdict(int)

    def fit(self, X_train, Y_train):
        self.classes = list(set(Y_train))
        for i in range(len(X_train)):
            words = (re.sub(r"\W+", " ", X_train[i].lower())).split(" ")
            c = Y_train[i]
            self.class_counts[c] += 1
            for w in words:
                self.word_counts[c][w] += 1
                self.total_counts[w] += 1

        for c in self.classes:
            total_words = sum(self.word_counts[c].values())
            for w in self.total_counts:
                count = self.word_counts[c][w]
                self.word_counts[c][w] = (count + self.alpha) / (total_words + self.alpha * len(self.total_counts))

    def predict(self, X_test):
        Y_output = []
        for x in X_test:
            words = (re.sub(r"\W+", " ", x.lower())).split(" ")
            scores = {c: 0 for c in self.classes}
            for c in self.classes:
                score = 0
                for w in words:
                    score += (lambda x: math.log(x) if x > 0 else 0)(self.word_counts[c][w])
                score += math.log(self.class_counts[c] / sum(self.class_counts.values()))
                scores[c] = score
            y_pred = max(scores, key=scores.get)
            Y_output.append(y_pred)
        return Y_output

    def score(self, X_test, Y_test):
        Y_pred = self.predict(X_test)
        correct = sum([1 for i in range(len(Y_test)) if Y_pred[i] == Y_test[i]])
        total = len(Y_test)
        return correct / total
