"""
Last edited: 2019-03-31
"""

import subprocess
from os import path


RIVEM_version = '4.5'


class rivem():
    """RIVEM wrapper class to store arguments and run the executable."""
    def __init__(self):
        self.out = None
        self.PDB = None
        self.matrix = None
        self.label = 0
        self.label_size = 0
        self.label_color = 16
        self.plot_axis = 0
        self.polar = 1
        self.begPhi = 0.0
        self.endPhi = 180.0
        self.begTheta = 0.0
        self.endTheta = 180.0
        self.deltaAngle = 1.0
        self.begX = -3.402823e+38
        self.endX = 3.402823e+38
        self.begY = -3.402823e+38
        self.endY = 3.402823e+38
        self.begZ = -3.402823e+38
        self.endZ = 3.402823e+38
        self.color_method = None
        self.dmin = None
        self.dmax = None
        self.color_mid_point = None
        self.color_min = None
        # Path to rivem executable
        self.rivem_path = path.join(path.dirname(__file__), "rivem")

    def generate_cmd(self):
        """Generate the argument list from the class attributes."""
        cmd = [self.rivem_path]
        cmd += ["-S", self.polar]
        if self.PDB is not None:
            cmd += ["-p", self.PDB]
        if self.matrix is not None:
            cmd += ["-m", self.matrix]
        if self.label == 1:
            cmd += ["-l"]
            cmd += [self.label_size]
            cmd += [self.label_color]
        if self.plot_axis != 0:
            cmd += ["-s", self.plot_axis]
        if self.begPhi != 0.0:
            cmd += ["-Pbeg", self.begPhi]
        if self.endPhi != 180.0:
            cmd += ["-Pend", self.endPhi]
        if self.begTheta != 0.0:
            cmd += ["-Tbeg", self.begTheta]
        if self.endTheta != 180.0:
            cmd += ["-Tend", self.endTheta]
        if self.deltaAngle != 1.0:
            cmd += ["-D", self.deltaAngle]
        if self.begX != -3.402823e+38:
            cmd += ["-Xbeg", self.begX]
        if self.endX != 3.402823e+38:
            cmd += ["-Xend", self.endX]
        if self.begY != -3.402823e+38:
            cmd += ["-Ybeg", self.begY]
        if self.endY != 3.402823e+38:
            cmd += ["-Yend", self.endY]
        if self.begZ != -3.402823e+38:
            cmd += ["-Zbeg", self.begZ]
        if self.endZ != 3.402823e+38:
            cmd += ["-Zend", self.endZ]
        if self.color_method is not None:
            cmd += ["-c", self.color_method]
            if self.dmin is not None:
                cmd += ["-dmin", self.dmin]
            if self.dmax is not None:
                cmd += ["-dmax", self.dmax]
            if self.color_mid_point is not None:
                cmd += ["-G", self.color_mid_point]
            if self.color_min is not None:
                cmd += ["-g", self.color_min]
        # Add output file
        cmd += ["-O", self.out]
        return [str(k) for k in cmd]

    def run(self):
        """Run the rivem executable."""
        cmd = self.generate_cmd()
        subprocess.call(cmd)
