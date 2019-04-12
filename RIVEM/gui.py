"""
Last edited: 2019-04-09
"""

from __future__ import print_function
import os
import os.path
import Tkinter as tk
import Pmw
import time
import chimera
from chimera.baseDialog import ModelessDialog
from chimera.widgets import MoleculeScrolledListBox
from chimera.widgets import MoleculeOptionMenu
from chimera import Molecule
from chimera import dialogs
from RIVEM import rivem, RIVEM_version


class RIVEM_GUI(ModelessDialog):
    name = "RIVEM"
    title = "RIVEM v" + RIVEM_version
    buttons = ('Plot', 'Close')
    help = "file://" + os.path.join(os.path.dirname(__file__), "manual.html")

    def fillInUI(self, parent):
        # Frame to contain widgets
        f = tk.Frame(parent)
        # Input PDB selection dropdown
        self.inputPDBMenu = MoleculeOptionMenu(parent, label_text="Input PDB:",
                                               labelpos='w')
        self.inputPDBMenu.grid(row=2, column=1)
        # Add a model selection list
        #self.inputModelList = MoleculeScrolledListBox(
        #        parent, autoselect='single', labelpos='w',
        #        label_text="Input PDB:")
        #self.inputModelList.grid(row=1, column=1)


    def Plot(self):
        wrapper = rivem()
        # Get parameters from GUI
        if self.inputPDBMenu.getvalue() is not None:
            input_pdb_path = self.inputPDBMenu.getvalue().openedAs[0]
            wrapper.set_input_PDB(input_pdb_path)
        # Run command
        wrapper.run()

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
