import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from heart_data import *

data = import_heart_data(translate=True)
label = data.columns[-1]

def make_feature_plots(jitter=.02):
    '''Generate the logistic regression plot for every feature.'''
    for feature in data.columns[:-1]:
        plot = sns.regplot(x=feature, y=label, logistic=True, data=data, y_jitter=jitter)
        plot.get_figure().savefig(f"plots/{feature}.png")
        plt.clf() # clear everything

def make_bar_plot(names, values, filename):
    '''Generate a bar plot

    Parameters
    ----------
    names : list of string, names of the labels.
    values : values to plot.
    filename : the name of the file. Will be saved in plots/filename.png.'''
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    plt.xticks(rotation='vertical')
    plot = sns.barplot(x = names, y=values)
    plot.get_figure().savefig(f"plots/{filename}.png")
    plt.clf()


def make_rf_importance_plot(n_estimators=200):
    '''Generates the Random Forest importance plot'''
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=n_estimators)
    rf.fit(data.iloc[:, 0:-1], data.iloc[:, -1])
    make_bar_plot(names = data.columns[:-1],
                  values=rf.feature_importances_,
                  filename='rf_importance')

def make_correlation_plot(absolute_value=True):
    '''Generates the correlation plot'''
    corr = data.corr()[label][:-1]
    if absolute_value:
        corr = corr.abs()
    make_bar_plot(names=data.columns[:-1],
                  values=corr,
                  filename='corr')

def make_creatinine_vs_ejection_fraction_plot():
    '''Generates the creatinine vs ejection plot'''
    creatinine = data.columns[7]
    fraction = data.columns[4]
    death = data.columns[-1]
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    plot = sns.scatterplot(x=creatinine, y=fraction, hue=death, data=data)
    plot.get_figure().savefig("plots/creatinine_vs_ejection_fraction.png")
    plt.clf()


def make_all_plots():
    make_feature_plots()
    make_rf_importance_plot()
    make_correlation_plot()
    make_creatinine_vs_ejection_fraction_plot()
