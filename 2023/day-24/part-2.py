import z3


def read_data(filename):
    """
    Reads the hailstone data from a file and returns a list of tuples.

    Each tuple contains position and velocity information in the format:
    (px, py, pz, vx, vy, vz)

    :param filename: str, name of the file containing the data
    :return: list of tuples
    """
    hailstones = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split('@')
            position = tuple(map(int, parts[0].split(',')))
            velocity = tuple(map(int, parts[1].split(',')))
            hailstones.append(position + velocity)
    return hailstones


def main():
    """
    The trick is to find out from where the stone has to be thrown and at what speed so that it hits
    hailstone 1 after t1, hailstone 2 after t2 and so on. Since the Advent of code puzzles are designed to be solvable,
    this must work for all hailstones. Since we have 6 unknowns (x,y,z,vx,vy,vz), a system of equations
    with 6 unknowns must be solved. Perhaps there is a symbolic solution. Since this is too complicated
    for me and there are numerical solvers for Python, I use them.
    """
    hailstones = read_data("input.txt")

    x, y, z, vx, vy, vz = z3.Reals("x y z vx vy vz")
    s = z3.Solver()

    # You can run the whole solving process but it is enough to run it for the first equations
    for i, h in enumerate(hailstones[0:7]):
        ax, ay, az, vax, vay, vaz = h
        t = z3.Real(f't_{i}')
        s.add(t >= 0)
        s.add(x + vx * t == ax + vax * t)
        s.add(y + vy * t == ay + vay * t)
        s.add(z + vz * t == az + vaz * t)

    assert s.check() == z3.sat

    m = s.model()
    x, y, z = m.eval(x), m.eval(y), m.eval(z)
    x, y, z = x.as_long(), y.as_long(), z.as_long()

    result = x + y + z

    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
