import pandas as pd
from matplotlib import pyplot as plt

from app.Machine_Learning.Analysis import AnalyzerBase
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class LinearRegressionAnalyzer(AnalyzerBase):

    def __init__(self, overrideData=None):
        super().__init__()

        if overrideData is not None:
            self.mergedData = overrideData
    def plotLinearRegression(self, yColumn, allColumns, xPlot=None, xlabel='', ylabel='',
                             title=''):
        X_test, y_test, y_pred = self.getLinearRegressionData(yColumn, allColumns)

        if xPlot is None:
            X_test = X_test.iloc[:, 0]

        plt.scatter(X_test[xPlot], y_test, color='red', label='Linear Regression')
        plt.plot(X_test[xPlot], y_pred, color="blue", linewidth=3)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        plt.xticks(rotation=90)

        return plt

    def getLinearRegressionData(self, yColumn, xColumns):
        x = self.mergedData[xColumns]
        y = self.mergedData[yColumn]

        x = pd.get_dummies(x)

        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train)

        y_pred = linear_model.predict(X_test)

        print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

        y_test = y_test.astype(float)

        return X_test, y_test, y_pred