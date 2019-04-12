"""
Last edited: 2019-04-09
"""

from __future__ import print_function
import os
import os.path
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
    help = "file://" + os.path.join(os.path.dirname(__file__), "manual.html")

    def fillInUI(self, parent):
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
        if self.inputPDBMenu.getvalue() is not None:
            input_pdb_path = self.inputPDBMenu.getvalue().openedAs[0]
            self.wrapper.PDB = input_pdb_path
        matrix = self.matrixMenu.getvalue()
        if matrix == "None":
            self.wrapper.matrix = None
        elif matrix == "ncs1":
            self.wrapper.matrix = os.path.join(os.path.dirname(__file__),
                                               "matrix_files", "ncs.def")
        elif matrix == "ncs2":
            self.wrapper.matrix = os.path.join(os.path.dirname(__file__),
                                               "matrix_files", "ncs2.def")

    def Run(self):
        """Set up command and run RIVEM executable."""
        # Initialize RIVEM wrapper object
        self.wrapper = rivem()
        self.updateParams()
        # Run command
        self.wrapper.run()

    def PrintCommand(self):
        """Prints the command for the current parameters."""
        self.wrapper = rivem()
        self.updateParams()
        cmd = " ".join(self.wrapper.generate_cmd())
        self.cmdTxtBox.settext(cmd)
        print(cmd)


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
