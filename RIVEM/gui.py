"""
Last edited: 2019-03-31
"""

import chimera
import os
import os.path
import Tkinter as tk
import tkMessageBox
import tkFileDialog
import time
from chimera.baseDialog import ModelessDialog
from chimera import dialogs
from RIVEM import RIVEM_version


OML = chimera.openModels.list


class RIVEM_GUI(ModelessDialog):
    name = "RIVEM"
    title = "RIVEM v" + RIVEM_version
    buttons = ('Run')
    help = "https://bilbo.bio.purdue.edu/~viruswww/Rossmann_home/softwares/river_programs/rivem.php"

    def fillInUI(self, parent):
        # Make a label for the Path selection box
        pathLabel = tk.Label(parent, text='Path to RIVEM executable:')
        pathLabel.grid(column=0, row=0)


# Register dialogs
dialogs.register(RIVEM_GUI.name, RIVEM_GUI, replace=True)
