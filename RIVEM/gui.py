"""
Last edited: 2019-04-09
"""

from __future__ import print_function
from os import path
import Tkinter as tk
import Pmw
import chimera
from chimera.baseDialog import ModelessDialog
from chimera.widgets import MoleculeScrolledListBox
from chimera.widgets import MoleculeOptionMenu
from chimera import dialogs
from RIVEM import rivem, RIVEM_version


class RIVEM_GUI(ModelessDialog):
    name = "RIVEM"
    title = "RIVEM v" + RIVEM_version
    buttons = ('Run', 'Print Command', 'Close')
    help = "file://" + path.join(path.dirname(__file__), "manual.html")
    # Initialize RIVEM wrapper object
    wrapper = rivem()

    def fillInUI(self, parent):
        """Generate GUI widgets"""
        # Frame to contain widgets
        f = tk.Frame(parent)
        # Input PDB selection dropdown
        self.inputPDBMenu = MoleculeOptionMenu(parent, label_text="Input PDB:",
                                               labelpos='w')
        self.inputPDBMenu.grid(row=0, column=0, sticky='w')
        # Input matrix selection dropdown
        self.matrixMenu = Pmw.OptionMenu(parent, initialitem="None",
                                         label_text="Matrix file:",
                                         labelpos='w',
                                         items=["None", "ncs1", "ncs2"])
        self.matrixMenu.grid(row=1, column=0, sticky='w')
        # Text box for printing commands
        self.cmdTxtBox = Pmw.ScrolledText(parent, label_text="Command",
                                          labelpos="n", usehullsize=1,
                                          hull_width=400, hull_height=80,
                                          text_padx=4, text_pady=4)
        self.cmdTxtBox.configure(text_state="disabled")
        self.cmdTxtBox.bind("<1>", lambda event: self.cmdTxtBox.focus_set())
        self.cmdTxtBox.grid(sticky='s')
        # Add a model selection list
        #self.inputModelList = MoleculeScrolledListBox(
        #        parent, autoselect='single', labelpos='w',
        #        label_text="Input PDB:")
        #self.inputModelList.grid(row=1, column=1)

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
                if not isfile(model_path):
                    model_path = None
        else:
            model_path = None
        return model_path

    def Run(self):
        """Set up command and run RIVEM executable."""
        self.updateParams()
        self.wrapper.run()

    def PrintCommand(self):
        """Prints the command for the current parameters."""
        self.updateParams()
        cmd = " ".join(self.wrapper.generate_cmd())
        self.cmdTxtBox.settext(cmd)


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
