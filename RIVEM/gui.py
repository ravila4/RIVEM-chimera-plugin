"""
Last edited: 2019-04-09
"""

from __future__ import print_function
import os
from os import path
import platform
import shutil
import subprocess
import Tkinter as tk
import Pmw
from chimera import replyobj
from chimera.baseDialog import ModelessDialog
from chimera.widgets import MoleculeScrolledListBox
from chimera.widgets import MoleculeOptionMenu
from chimera import dialogs
from RIVEM import rivem, RIVEM_version


class RIVEM_GUI(ModelessDialog):
    # Initialize RIVEM wrapper object
    wrapper = rivem()
    name = "RIVEM"
    title = "RIVEM v" + RIVEM_version
    buttons = ('Run', 'Print Command', 'Close')
    help = "file://" + path.join(path.dirname(__file__), "manual.html")

    def fillInUI(self, parent):
        """Generate GUI widgets"""
        # Frame to contain widgets
        self.inputFrame = tk.LabelFrame(parent, text="Input")
        self.inputFrame.pack(fill="both", expand="yes")
        # Input PDB selection dropdown
        self.inputPDBMenu = MoleculeOptionMenu(self.inputFrame,
                                               label_text="Input PDB:",
                                               labelpos='w')
        self.inputPDBMenu.grid(row=0, column=0, sticky='w')
        # Input matrix selection dropdown
        self.matrixMenu = Pmw.OptionMenu(self.inputFrame, initialitem="None",
                                         label_text="Matrix file:",
                                         labelpos='w',
                                         items=["None", "ncs1", "ncs2"])
        self.matrixMenu.grid(row=1, column=0, sticky='w')
        # Label Frame for color settings
        self.colorFrame = tk.LabelFrame(parent, text="Color settings")
        self.colorFrame.pack(fill="both", expand="yes")
        # Color selection dropdown
        self.color_methods = ["None",
                              "Residue type",
                              "Radius, small (Red) to large (Blue)",
                              "Radius, small (Blue) to large (Red)",
                              "Density, negative (Red) to positive (Blue)",
                              "Density, negative (Blue) to positive (Red)",
                              "From PDB"]
        self.colorMenu = Pmw.OptionMenu(self.colorFrame, initialitem="None",
                                        label_text="Color method:",
                                        labelpos='w',
                                        items=self.color_methods)
        self.colorMenu.grid(row=2, column=0, sticky='w')
        # Text box for printing commands
        self.cmdTxtBox = Pmw.ScrolledText(parent, label_text="Command",
                                          labelpos="n", usehullsize=1,
                                          hull_width=400, hull_height=100,
                                          text_padx=4, text_pady=4)
        self.cmdTxtBox.configure(text_state="disabled")
        self.cmdTxtBox.bind("<1>", lambda event: self.cmdTxtBox.focus_set())
        # Add a model selection list
        # self.inputModelList = MoleculeScrolledListBox(
        #         parent, autoselect='single', labelpos='w',
        #         label_text="Input PDB:")
        # self.inputModelList.grid(row=1, column=1)

    def updateParams(self):
        """Update wrapper attributes from GUI input."""
        # Get path to input model
        if self.inputPDBMenu.getvalue() is not None:
            input_pdb_path = self.inputPDBMenu.getvalue().openedAs[0]
            if not path.isfile(input_pdb_path) and len(input_pdb_path) == 4:
                # Input model is from a fetched file
                id_code = input_pdb_path.upper()
                input_pdb_path = self.getFetchedModelPath(id_code)
            self.wrapper.PDB = input_pdb_path
        # Set matrix file
        matrix = self.matrixMenu.getvalue()
        if matrix == "None":
            self.wrapper.matrix = None
        elif matrix == "ncs1":
            self.wrapper.matrix = path.join(path.dirname(__file__),
                                            "matrix_files", "ncs.def")
        elif matrix == "ncs2":
            self.wrapper.matrix = path.join(path.dirname(__file__),
                                            "matrix_files", "ncs2.def")
        # Set color method
        cm = self.colorMenu.getvalue()
        cm_index = self.color_methods.index(cm)
        color_codes = [None, "1", "2", "3", "4", "5", None]
        # TODO: If cm_index is 6, ask for input PDB
        self.wrapper.color_method = color_codes[cm_index]

    def getFetchedModelPath(self, id_code):
        """Find the path to a fetched model (one that wasn't opened from a
        file)."""
        from chimera.fetch import FETCH_PREFERENCES, FETCH_DIRECTORY
        from chimera import preferences
        cache_dir = preferences.get(FETCH_PREFERENCES, FETCH_DIRECTORY)
        if cache_dir:
            from OpenSave import tildeExpand
            cache_dir = tildeExpand(cache_dir)
            model_path = path.join(cache_dir, "PDB", id_code + ".pdb")
            if not path.isfile(model_path):
                # Check for mmCIF file
                model_path = path.join(cache_dir, "PDB", id_code + ".cif")
                if not path.isfile(model_path):
                    model_path = None
        else:
            model_path = None
        return model_path

    def Run(self):
        """Set up command and run RIVEM executable."""
        self.updateParams()
        # Print command in text box
        cmd = " ".join(self.wrapper.generate_cmd())
        self.cmdTxtBox.settext(cmd)
        # Run RIVEM
        replyobj.status("Running RIVEM")
        self.wrapper.run()
        replyobj.status("Done.")
        # Open generated postcrip with system viewer
        if platform.system() == "Darwin":
            subprocess.call(("open", self.wrapper.out))
        elif platform.system() == "Windows":
            os.startfile(self.wrapper.out)
        else:
            subprocess.call(("xdg-open", self.wrapper.out))
        # TODO: Find a nice way to remove temp file.
        # TODO: Make  generated ps file have a unique name.

    def PrintCommand(self):
        """Prints the command for the current parameters."""
        self.updateParams()
        cmd = " ".join(self.wrapper.generate_cmd())
        self.cmdTxtBox.settext(cmd)
        # Show text box
        self.cmdTxtBox.pack(fill="both", expand="yes", side="bottom")


#
# ----------------------------------------------------------------------------
#


def get_model_list():
    """Return a list of currently loaded models."""
    from chimera import openModels as om, Molecule
    from VolumeViewer import Volume
    mlist = om.list(modelTypes=[Molecule, Volume])
    mlist = ['selected atoms'] + mlist
    return mlist


# Register dialogs
dialogs.register(RIVEM_GUI.name, RIVEM_GUI, replace=True)
