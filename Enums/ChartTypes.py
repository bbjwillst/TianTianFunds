from enum import Enum, unique

@unique
class ChartTypes(Enum):
    ScatterLinearRegrPlot= 0
    ZheXianTu = 1
    ZhiFangTu = 2
    BingTu = 3
    ScatterPlot = 4
