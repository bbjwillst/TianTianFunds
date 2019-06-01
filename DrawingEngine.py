from DbUtilities.MariaHelper import MariaHelper
from Enums.ChartTypes import ChartTypes

import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


class DrawingEngine(object):
    def __init__(self):
        pass

    def Draw(self, codeno, type=ChartTypes.ScatterLinearRegrPlot):
        mh = MariaHelper()
        data = mh.queryLsjzByCodeno(codeno)
        df = pd.DataFrame(data)
        df['fsrq'] = pd.to_datetime(df['fsrq'])
        df.set_index('fsrq')

        ax = plt.subplots(figsize=(10, 10))
        ax.bar(x=df['fsrq'].head(10), height=df['dwjz'].head(10), color='r')
        ax.set_label(xlabel='X Title', size=20)
        plt.show()
