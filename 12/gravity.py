from LoadValues import LoadValues

class Moon:
    coords = None
    velocity = None

    def __init__(self, coords=(0,0,0)):
        self.coords = coords
        self.velocity = (0,0,0)

    def _coord_str(self, coord):
        (x, y, z) = coord
        str = "<x={}, y={}, z={}>".format(x, y, z)
        return str

    def __str__(self):
        str = "pos= " + self._coord_str(self.coords) + "\tvel=" + self._coord_str(self.velocity)
        str += "\tpot ={}\tkin ={}\ttot ={}".format(self.potential_energy(), self.kinetic_energy(), self.energy())
        return str

    def __eq__(self, other):
        return self.coords == other.coords and self.velocity == other.velocity

    def _delta_axis_velocity(self, a, b):
        if b > a:
            return 1
        elif b < a:
            return -1
        else:
            return 0

    def update_velocity(self, other):
        (x, y, z) = self.coords
        (xp, yp, zp) = other.coords
        (vx, vy, vz) = self.velocity
        vx += self._delta_axis_velocity(x, xp)
        vy += self._delta_axis_velocity(y, yp)
        vz += self._delta_axis_velocity(z, zp)
        self.velocity = (vx, vy, vz)

    def move_moon(self):
        (x, y, z) = self.coords
        (vx, vy, vz) = self.velocity
        x += vx
        y += vy
        z += vz
        self.coords = (x, y, z)

    def potential_energy(self):
        (x, y, z) = self.coords
        return (abs(x)+abs(y)+abs(z))

    def kinetic_energy(self):
        (x, y, z) = self.velocity
        return (abs(x)+abs(y)+abs(z))

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()

class Galaxy:
    moon_list = None

    def __init__(self, coord_list):
        self.moon_list = []
        for coord in coord_list:
            moon = Moon(coord)
            self.moon_list.append(moon)

    def __str__(self):
        res = []
        for moon in self.moon_list:
            res.append(str(moon))
        str_res = "\n".join(res)
        str_res += "\n"+"energy :" + str(self.energy())
        return str_res

    def next_step(self):
        for moon in self.moon_list:
            for other in self.moon_list:
                moon.update_velocity(other)
        for moon in self.moon_list:
            moon.move_moon()

    def energy(self):
        tot = sum([moon.energy() for moon in self.moon_list])
        return tot

    def __eq__(self, other):
        for (i, moon) in enumerate(self.moon_list):
            if moon != other.moon_list[i]:
                return False
        return True



if __name__ == '__main__':
    value_loader = LoadValues("input2")
    coord_list = value_loader.get_3d_coords()
    print(coord_list)
    my_galaxy = Galaxy(coord_list)

    for i in range(1001):
        print("After step #", i)
        print(my_galaxy)
        my_galaxy.next_step()

    my_galaxy = Galaxy(coord_list)
    print(my_galaxy)
    state_list = {}
    i = 0
    #state_list[my_galaxy.energy()] = [my_galaxy]
    norepeat = True
    while norepeat:
        energy = my_galaxy.energy()
        if energy in state_list:
            for galaxy in state_list[energy]:
                if my_galaxy == galaxy:
                    print(my_galaxy)
                    print(galaxy)
                    norepeat = False
                    print("Finished, repeat at :", i)
                    break
                state_list[energy].append(my_galaxy)
        else:
            state_list[energy] = [my_galaxy]
        print("Step : ", i, " energy:", energy)
        my_galaxy.next_step()
        i += 1



