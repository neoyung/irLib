from pathlib import Path
import pandas as pd
from irLib.helpers.yieldCurve import yieldCurve


class reader:
    def __init__(self):
        self.content = dict()

    # alias is for user to define but it has to match a yieldCurve name later or throw error
    def readFile(self, filepath, alias):
        self.content[alias] = {'dataSource': Path(
            filepath), 'data': pd.read_csv(Path(filepath))}

    def loadYCData(self, object_, timeIndex, sim_no):
        assert isinstance(object_, yieldCurve), 'not a yield curve'
        
        try:
            object_.dataSource = self.content[object_.alias]['dataSource']
            object_.timeIndex = timeIndex
            object_.values = self.content[object_.alias]['data'].iloc[sim_no, :len(
                timeIndex)].tolist()
        except KeyError as ke:
            print(
                f'Object name {str(ke)} does not match any one of the aliases in reader')
