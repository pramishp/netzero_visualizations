import matplotlib.pyplot as plt

from BasePlot import BasePlot


class StackedArea(BasePlot):
    def __init__(self):
        super(StackedArea, self).__init__()

    def plot(self, df):
        '''

        :param df: df with columns 'Year' and other columns will be plotted
        :return:
        '''

