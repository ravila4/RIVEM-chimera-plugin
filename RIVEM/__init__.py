"""
Last edited: 2019-03-31
"""

from __future__ import print_function
import subprocess
import tempfile
import os


RIVEM_version = '4.5'


class rivem():
    """RIVEM wrapper class to store arguments and run the executable."""
    def __init__(self):
        # Output file is generated in a temp dir
        self.temp_dir = tempfile.mkdtemp()
        self.out = os.path.join(self.temp_dir, "map.ps")
        self.PDB = None
        self.matrix = None

    def generate_cmd(self):
        cmd = ["rivem"]
        if self.PDB is not None:
            cmd += ["-p", self.PDB]
        if self.matrix is not None:
            cmd += ["-m", self.matrix]
        # Add output file
        cmd += ["-O", self.out]
        return cmd

    def run(self):
        cmd = self.generate_cmd()
        print("Command:", cmd)
        subprocess.call(cmd)
        print("Wrote output file to:", self.out)
