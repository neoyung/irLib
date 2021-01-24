class portfolio:
    """
    1.  Shocking common parts of components like discount curve, model any dependence on any 
        object simply by referencing the object as an item of a instance of portfolio.
    2.  Features: show cashflow overtime by overseeing every components schedule, any kinds of 
        buy and sell at any time pt. Have to set behavior for received cash flow, like 
        reinvest or idle? (Proposed)
    3.  Sensitivity and scenario testing by using method like 1 mentioned
    """

    def __init__(self, **components):
        self.components = components

    def addComponent(self, component, alias):
        self.components[alias] = component

    def setDependedObjs(self, **objs):
        self.dependedObjs = objs

    # discount curve is just an example of objs one can shock
    def addDependedObj(self, obj, alias):
        self.dependedObjs[alias] = obj

    def calculateNPV(self, valuationDate):
        return sum([component.calculateNPV(valuationDate) for componentAlias, component in self.components.item()])
