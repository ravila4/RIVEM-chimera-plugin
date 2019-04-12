"""
Last edited: 2019-03-31
"""

from __future__ import print_function
import subprocess
import tempfile
import os


RIVEM_version = '4.5'


class rivem():
    """Class to interact with RIVEM executable."""
    def __init__(self):
        # Output file is generated in a temp dir
        self.temp_dir = tempfile.mkdtemp()
        self.out = os.path.join(self.temp_dir, "map.ps")
        self.PDB = None     # Input PDB
        self.matrix = None  # Input matrix

    def set_input_PDB(self, path):
        """Takes as agument a file path to a currently loaded model."""
        self.PDB = path
        print("setting self.PDB", self.PDB)

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
        print("command:", cmd)
        subprocess.call(cmd)
        print("Wrote output file to:", self.out)

