import logging

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


# A more general function would allow better tuning, but sufficient for this project
def model(X, y, te_s=0.3):

    # region private helper functions
    def get_optimized_lasso(Xtr, Ytr):
        """
        Perform a GridSearch with cross-validation to determine optimal alpha value for the Lasso modifier
        :param Xtr: pandas DataFrame of the X training set
        :param Ytr: pandas DataFrame or Series of the response
        :return: Lasso estimator object fitted to the best parameters
        """
        logging.debug('Entering get_optimized_lasso()')
        # Best practice future implementation should have programmatically defined parameters instead
        # The values chosen here are a result from trial in a jupyter notebook
        tune = [{'normalize': [True], 'alpha': [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]},
                {'normalize': [False], 'alpha': [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]}]

        lasso_grid = GridSearchCV(Lasso(), tune, cv=5, scoring='explained_variance')
        lasso_grid.fit(Xtr, Ytr)

        return lasso_grid.best_estimator_

    def feature_selection(lm, x):
        """
        Removes columns with a zero coefficient as determined by the Lasso estimator
        :param lm: Lasso model
        :param x: pandas DataFrame fitted to lm
        :return: pandas DataFrame x, with non-correlated coefficients removed
        """
        logging.debug('Entering feature_selection()')
        mask = []
        for i in range(len(x.columns)):
            logging.debug(lm.coef_[i])
            if lm.coef_[i] == 0:
                mask.append(False)
                logging.debug(False)
            else:
                mask.append(True)
                logging.debug(True)
        return x.loc[:, mask]

    # endregion

    Xtr, Xte, Ytr, Yte = train_test_split(X, y, test_size=te_s)

    lm = get_optimized_lasso(Xtr, Ytr)
    # Use optimized lasso to remove coef_ 0 columns
    selected_x = feature_selection(lm, X)

    Xtr, Xte, Ytr, Yte = train_test_split(selected_x, y, test_size=te_s)
    lm = get_optimized_lasso(Xtr, Ytr)

    return lm, selected_x


def return_coefficients(lm, selected_x):
    """
    Returns the coefficient of regression with the corresponding feature name
    :param lm: Fitted linear model
    :param selected_x: pandas DataFrame of features
    :return: zip object containing each coefficient and feature
    """
    zipped = zip(lm.coef_, selected_x)
    return list(zipped)



def plot_analyze(lm, X, y, te_s=0.3):
    """
    Generates various plots that evaluate the efficacy of the model
    :param lm: Lasso model, fitted
    :param X: pandas DataFrame of features
    :param y: pandas DataFrame or Series of response
    :param te_s: Float of test size to perform train_test_split upon
    :return: None
    """
    # region private helper functions
    # Returns residuals
    def residuals(lm, x, y):
        """Calculate residuals of model"""
        logging.debug('Entering residuals()')

        y_pred = lm.predict(x)

        return y - y_pred

    def residual_plot(resid):
        """Plot residuals of model"""
        fig, ax = plt.subplots()
        ax.plot(resid, 'o')
        ax.set_xlabel('Listing')
        ax.set_ylabel('Residual in Rental Price')
        ax.set_title('Model Residual Plot')

    def forty_five(y, y_pred):
        """Plot estimated response vs actual response"""
        fig, ax = plt.subplots()
        ax.plot(y.reset_index()['price'], y_pred, 'o')
        ax.plot(np.linspace(0, 12000), np.linspace(0, 12000), 'b-')
        ax.set_xlabel('Actual Price')
        ax.set_ylabel('Predicted Price')
        ax.set_title('Errors of Model')
        plt.show()

    def error_plot(y, y_pred):
        """Plot response over predicted response"""
        fig, ax = plt.subplots()
        ax.plot(y.reset_index()['price'], 'o', label='Actual Price')
        ax.plot(y_pred, 'o', label='Model-Predicted Price')
        ax.legend(loc='upper right')
        ax.set_xlabel('Listing')
        ax.set_ylabel('Error')
        ax.set_title('Errors of Model')

    def qq_plot(resid):
        """QQ Plot of residuals"""
        plt.subplots()
        scipy.stats.probplot(resid, dist="norm", plot=plt)
        plt.show()

    def learning_curve(lm, Xtr, Xte, Ytr, Yte):
        """Generate learning curve"""
        te_error = []
        tr_error = []
        for i in range(1, len(Xtr)+1):
            model = Lasso(alpha=lm.alpha)
            model.fit(Xtr.iloc[0:i, :], Ytr[0:i])
            yp_tr = model.predict(Xtr.iloc[0:i, :])
            yp_te = model.predict(Xte)
            tr_error.append(mean_squared_error(Ytr[0:i], yp_tr))
            te_error.append(mean_squared_error(Yte, yp_te))

        x = np.linspace(1, Xtr.shape[0], Xtr.shape[0])
        fig, ax = plt.subplots()
        plt.plot(x, tr_error, label='Training Error')
        plt.plot(x, te_error, label='Testing Error')
        ax.legend(loc='upper right')
        ax.set_xlabel('Size of Training Set')
        ax.set_ylabel('Error')
        ax.set_title('Learning Curve of Model')
        plt.show()

    # endregion

    Xtr, Xte, Ytr, Yte = train_test_split(X, y, test_size=te_s)
    test_resid = residuals(lm, Xte, Yte)
    residual_plot(test_resid)
    error_plot(Yte, lm.predict(Xte))
    qq_plot(test_resid)
    learning_curve(lm, Xtr, Xte, Ytr, Yte)
    forty_five(Yte, lm.predict(Xte))
