from queue import Queue

from loadValues import LoadValues
import math

class FuelCalculator:
    reactions = None
    orders = None
    ore_needed = 0
    leftovers = None

    def __init__(self, reactions):
        self.reactions = reactions
        self.orders = Queue()
        self.leftovers = {}

    def consume_order(self):
        (order, qty) = self.orders.get()
        if order == "ORE":
            self.ore_needed += qty
        else:
            if order in self.leftovers:
                left = self.leftovers[order]
            else:
                left = 0
            if left > qty:
                self.leftovers[order] = left - qty
            else:
                needed = qty - left
                ((compound, q_recipe), ingredients) = self.reactions[order]
                mult = math.ceil(needed / q_recipe)
                for (ingredient, ing_qty) in ingredients:
                    self.orders.put((ingredient, ing_qty * mult))
                left = mult * q_recipe - needed
                self.leftovers[compound] = left

    def make_fuel(self, qty=1):
        self.orders = Queue()
        self.leftovers = {}
        self.ore_needed = 0
        self.orders.put(("FUEL", qty))
        while not self.orders.empty():
            self.consume_order()
        return self.ore_needed

    def how_many_for_ore(self, qty, max):
        min = 0
        while (max-min) > 1:
            tmp = math.floor((max+min)/2)
            print(min, max, tmp)

            tmp_qty = self.make_fuel(tmp)
            if tmp_qty <= qty:
                min = tmp
            else:
                max = tmp
        return min

if __name__ == '__main__':
    lv = LoadValues("input")

    reactions = lv.get_reactions()
    print(reactions)
    my_fc = FuelCalculator(reactions)
    qty = my_fc.make_fuel(1)
    print(qty)
    qty = my_fc.make_fuel(10)
    print(qty)
    qty = my_fc.make_fuel(1)
    print(qty)


    max = 1000000000000

    val = my_fc.how_many_for_ore(1000000000000, max)
    print(val, my_fc.make_fuel(val))
    print(val, my_fc.make_fuel(val+1))

