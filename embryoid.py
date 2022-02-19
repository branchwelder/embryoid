from rich import print
from pyembroidery import *
from svgpathtools import svg2paths, wsvg
import numpy as np


OUTPUT_PES = "pes_tests/"
OUTPUT_SVG = "svg_tests/"
INPUT_SVG = "tests_input/"


class Embryoid:
    def __init__(self):
        self.pattern = EmbPattern()

    def save_svg(self, fname=OUTPUT_SVG + "design.svg"):
        write_svg(self.pattern, fname)

    def save_pes(self, fname=OUTPUT_PES + "design.pes"):
        write_pes(self.pattern, fname)

    def add_stitch_block(self, block):
        self.pattern.add_block(block)

    def parse_svg(self, fname):
        paths, attributes = svg2paths(fname)
        print(attributes)
        for path in paths:
            block = []
            for segment in path._segments:
                block.append((segment.start.real, segment.start.imag))
            block.append((path._segments[0].start.real, path._segments[0].start.imag))
            self.pattern.add_block(block, "teal")


def solid_block(x_len=100, y_len=100, num_stitches=20):
    stitches = []
    stitches_y_coords = np.linspace(0, y_len, num_stitches)
    for stitch_y in stitches_y_coords:
        stitches.append((0, stitch_y))
        stitches.append((x_len, stitch_y))

    return stitches


def parse(fname):
    e = Embryoid()
    e.parse_svg(INPUT_SVG + fname)
    e.save_svg("linger_longer.svg")
    e.save_pes("linger_longer.pes")


if __name__ == "__main__":
    parse("linger_longer_audioplot.svg")
    # e = Embryoid()
    # e.add_stitch_block(solid_block())
    # e.save_svg("block_test.svg")
    # e.save_pes("block_test.pes")
