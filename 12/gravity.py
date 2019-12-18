from LoadValues import LoadValues
import cProfile, pstats

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

    def __deepcopy__(self, memodict={}):
        new_moon = Moon()
        new_moon.coords = self.coords
        new_moon.velocity = self.velocity
        return new_moon

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

    def __deepcopy__(self, memodict={}):
        new_galaxy = Galaxy([])
        new_galaxy.moon_list = []
        for moon in self.moon_list:
            new_galaxy.moon_list.append(moon.__deepcopy__())
        return new_galaxy

    def find_cycle_len(self):
        my_galaxy = self.__deepcopy__()
        init_galaxy = self.__deepcopy__()
        init_energy= init_galaxy.energy()
        i = 1
        my_galaxy.next_step()
        norepeat = True
        while norepeat:
            energy = my_galaxy.energy()
            if energy == init_energy:
                if my_galaxy == init_galaxy:
                    print(my_galaxy)
                    norepeat = False
                    break
            if not (i % 10000):
                print("Step : ", i, " energy:", energy)
            my_galaxy.next_step()
            i += 1
        return i

    def find_single_dim_cycle(self):
        my_galaxyx = self.__deepcopy__()
        my_galaxyy = self.__deepcopy__()
        my_galaxyz = self.__deepcopy__()

        for (i, moon) in enumerate(self.moon_list):
            (x, y, z) = moon.coords
            (dx, dy, dz) = moon.velocity
            my_galaxyx.moon_list[i].coords = (x, 0, 0)
            my_galaxyy.moon_list[i].coords = (0, y, 0)
            my_galaxyz.moon_list[i].coords = (0, 0, z)
            my_galaxyx.moon_list[i].velocity = (dx, 0, 0)
            my_galaxyx.moon_list[i].velocity = (dy, 0, 0)
            my_galaxyx.moon_list[i].velocity = (dz, 0, 0)

        cycle_x = my_galaxyx.find_cycle_len()
        cycle_y = my_galaxyy.find_cycle_len()
        cycle_z = my_galaxyz.find_cycle_len()
        print(cycle_x, cycle_y, cycle_z)
        return lcm(lcm(cycle_x, cycle_y), cycle_z)


def gcd(a, b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b // gcd(a, b)


if __name__ == '__main__':
    pr = cProfile.Profile()

    value_loader = LoadValues("input")
    coord_list = value_loader.get_3d_coords()
    print(coord_list)
    my_galaxy = Galaxy(coord_list)

    for i in range(101):
        print("After step #", i)
        print(my_galaxy)
        my_galaxy.next_step()

    my_galaxy = Galaxy(coord_list)
    print(my_galaxy)


    pr.enable()

    init_galaxy = Galaxy(coord_list)
    #print(init_galaxy.find_cycle_len())
    print(init_galaxy.find_single_dim_cycle())
    pr.disable()
    #pr.print_stats()


