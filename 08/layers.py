import sys
import re
import collections
import math
import heapq
import itertools


class LoadValues:
    file = './input'
    raw_values = None
    processed_values = None

    def __init__(self, data=None, file=True):
        if file:
            if data is not None:
                file_name = data
            else:
                file_name = self.file
            with open(file_name) as f:
                self.raw_values = list(f)
        else:
            self.raw_values = list(data)

    def list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = [int(val) for val in raw]
        return self.processed_values

    def comma_list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = raw[0].split(",")
        return self.processed_values

    def value_to_digit_list(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = list(raw[0])
        return self.processed_values

class Layer:
    pixel_list = None
    sizeX = None
    sizeY = None

    def __init__(self, pixel_list, size):
        self.pixel_list = pixel_list
        (self.sizeX, self.sizeY) = size

    def get_zeros(self):
        return self.pixel_list.count('0')

    def get_ones(self):
        return self.pixel_list.count('1')

    def get_twos(self):
        return self.pixel_list.count('2')

    def get_score(self):
        return self.get_ones()*self.get_twos()

    def merge_with_inferior_layer(self, other):
        new_pixel = list(self.pixel_list)
        for i in range(len(self.pixel_list)):
            if new_pixel[i] == '2':
                new_pixel[i] = other.pixel_list[i]
        return Layer(''.join(new_pixel), (self.sizeX, self.sizeY))

    def __str__(self):
        tmp = []
        for i in range(self.sizeY):
            tmp.append(self.pixel_list[self.sizeX*i:self.sizeX*(i+1)])
        return "\n".join(tmp)

    def pretty(self):
        tmp = []
        for i in range(self.sizeY):
            buf= (self.pixel_list[self.sizeX*i:self.sizeX*(i+1)])

            tmp.append(buf.replace("0", " ").replace("1","X"))
        return "\n".join(tmp)

    def __repr__(self):
        return self.pixel_list

class Layers:
    layers = None
    sizeX = None
    sizeY = None

    def __init__(self, image, sizeX, sizeY):
        (self.sizeX, self.sizeY) = (sizeX, sizeY)
        self.layers = []
        pix_per_layer = sizeX*sizeY
        (nb_layers, rem) = divmod(len(image), pix_per_layer)
        for id_layer in range(nb_layers):
            new_layer = Layer(image[(id_layer*pix_per_layer):(id_layer+1)*pix_per_layer],(sizeX, sizeY))
            self.layers.append(new_layer)

    def get_best_layer(self):
        scores = []
        for idx,l in enumerate(self.layers):
            scores.append((l.get_zeros(), idx))
            print(l.pixel_list)
            print("Layer : ", idx, len(l.pixel_list), l.get_zeros(), l.get_ones(), l.get_twos(), l.get_score())
        (sc, best_layer) = min(scores)
        return (best_layer, self.layers[best_layer].get_score())

    def flatten_layers(self):
        tmp = self.layers[0]
        for i in self.layers[1:]:
            tmp = tmp.merge_with_inferior_layer(i)
        return tmp

if __name__ == '__main__':
    value_loader = LoadValues("input")
    values = value_loader.raw_values[0]
    print(values)
    ml = Layers(values,25,6)
    (lay, val) = ml.get_best_layer()
    print(lay, val)
    ll = ml.layers[3]

    print(ll.pixel_list)
    print(ml.layers[3].get_zeros())
    #print(ml.layers[3])

    flat =(ml.flatten_layers())
    print(flat.pretty())