from loadValues import LoadValues
import math

class FuelCalculator:
    reactions = {}
    ore_cost = {}

    def __init__(self, reactions):
        self.reactions = reactions
        self.ore_cost["ORE"] = (1, 1)

    def calculate_elem_cost(self, elem):
        if elem in self.ore_cost:
            return self.ore_cost[elem]
        else:
            ((res, qty), compounds) = self.reactions[elem]
            tmp_cost = 0
            for (compound, q) in compounds:
                (cost, units) = self.calculate_elem_cost(compound)
                tmp_cost += cost * math.ceil(q / units)
            self.ore_cost[elem] = (tmp_cost, qty)
            return self.ore_cost[elem]


    def calculate_ORE_cost(self):
        elem_list = self.reactions.keys()
        for elem in elem_list:
            self.calculate_elem_cost(elem)


if __name__ == '__main__':
    lv = LoadValues("input1")

    reactions = lv.get_reactions()
    print(reactions)
    my_fc = FuelCalculator(reactions)
    my_fc.calculate_ORE_cost()
    print(my_fc.ore_cost)
    print(my_fc.ore_cost["FUEL"])