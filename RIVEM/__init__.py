"""
Last edited: 2019-03-31
"""

import subprocess
import tempfile
from os import path


RIVEM_version = '4.5'


class rivem():
    """RIVEM wrapper class to store arguments and run the executable."""
    def __init__(self):
        # Output file is generated in a temp dir
        self.temp_dir = tempfile.mkdtemp()
        self.out = path.join(self.temp_dir, "map.ps")
        self.PDB = None
        self.matrix = None
        # Path to rivem executable
        self.rivem_path = path.join(path.dirname(__file__), "rivem")

    def generate_cmd(self):
        """Generate the argument list from the class attributes."""
        cmd = [self.rivem_path]
        if self.PDB is not None:
            cmd += ["-p", self.PDB]
        if self.matrix is not None:
            cmd += ["-m", self.matrix]
        # Add output file
        cmd += ["-O", self.out]
        return cmd

    def run(self):
        """Run the rivem executable."""
        cmd = self.generate_cmd()
        subprocess.call(cmd)
