import matplotlib.pyplot as plt
from math import pi, sin, cos, isnan

DEGREES_TO_RADIANS = pi / 180


def print_coords(coords):
    for (x, y) in coords:
        if isnan(x):
            print("<gap>")
        else:
            print("({:.2f}, {:.2f})".format(x, y))


def turtle_to_coords(turtle_program, turn_amount=45):
    # The state variable tracks the current location and angle of the turtle.
    # The turtle starts at (0, 0) facing up (90 degrees).
    state = (0.0, 0.0, 90.0)

    # Throughout the turtle's journey, we "yield" its location. These coordinate
    # pairs become the path that plot_coords draws.
    yield (0.0, 0.0)

    # Loop over the program, one character at a time.
    for command in turtle_program:
        x, y, angle = state

        if command in "Ff":  # Move turtle forward
            state = (
                x - cos(angle * DEGREES_TO_RADIANS),
                y + sin(angle * DEGREES_TO_RADIANS),
                angle,
            )

            if command == "f":
                # Insert a break in the path so that
                # this line segment isn't drawn.
                yield (float("nan"), float("nan"))

            yield (state[0], state[1])

        elif command == "+":  # Turn turtle clockwise without moving
            state = (x, y, angle + turn_amount)

        elif command == "-":  # Turn turtle counter-clockwise without moving
            state = (x, y, angle - turn_amount)

        # Note: We silently ignore unknown commands


def plot_coords(coords, bare_plot=False):
    if bare_plot:
        # Turns off the axis markers.
        plt.axis("off")
    # Ensures equal aspect ratio.
    plt.axes().set_aspect("equal", "datalim")
    # Converts a list of coordinates into
    # lists of X and Y values, respectively.
    X, Y = zip(*coords)
    # Draws the plot.
    plt.plot(X, Y)


def transform_sequence(sequence, transformations):
    return "".join(transformations.get(c, c) for c in sequence)


def transform_multiple(sequence, transformations, iterations):
    for _ in range(iterations):
        sequence = transform_sequence(sequence, transformations)
    return sequence


def hilbert():
    return turtle_to_coords(
        transform_multiple("L", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}, 5), 90
    )


if __name__ == "__main__":
    plt.style.use("bmh")  # Use some nicer default colors
    plt.xlabel("x")
    plt.ylabel("y")

    plot_coords(
        turtle_to_coords(
            transform_multiple("L", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}, 5), 90
        )
    )

    plt.show()
