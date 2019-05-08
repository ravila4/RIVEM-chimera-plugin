"""
Last edited: 2019-04-09
"""

from __future__ import print_function
import os
from os import path
import platform
import subprocess
import Tkinter as tk
import Pmw
from chimera import replyobj, UserError
from chimera.baseDialog import ModelessDialog
from chimera.widgets import MoleculeScrolledListBox
from chimera.widgets import MoleculeOptionMenu
from chimera.widgets import DisclosureFrame
from chimera import dialogs
from chimera.fetch import FETCH_PREFERENCES, FETCH_DIRECTORY
from chimera import preferences
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
        # Tooltips
        self.balloon = Pmw.Balloon(parent)
        # Widgets
        self._makeInputOpts(parent)
        self._makePlotRegionOpts(parent)
        self._makeColorOpts(parent)
        self._makePrintCmd(parent)
        # Add a model selection list
        # self.inputModelList = MoleculeScrolledListBox(
        #         parent, autoselect='single', labelpos='w',
        #         label_text="Input PDB:")
        # self.inputModelList.grid(row=1, column=1)

    def _makeInputOpts(self, parent):
        """Draw collapsible frame for input options."""
        df = DisclosureFrame(parent, text=" Input", collapsed=False)
        df.pack(fill="x")
        f = df.frame
        # Input PDB selection dropdown
        self.inputPDBMenu = MoleculeOptionMenu(f, label_text="Input PDB:",
                                               labelpos='w')
        self.inputPDBMenu.grid(row=0, column=0, sticky='w')
        self.balloon.bind(self.inputPDBMenu, "Give the name for the PDB " +
                          "file for the Roadmap.")
        # Input matrix selection dropdown
        self.matrixMenu = Pmw.OptionMenu(f, initialitem="None",
                                         label_text="Matrix file:",
                                         labelpos='w',
                                         items=["None", "ncs1", "ncs2"])
        self.matrixMenu.grid(row=1, column=0, sticky='w')
        self.balloon.bind(self.matrixMenu,
                          "Read in the matrix for the PDB and the maps. " +
                          "The matrix should be in CNS ncs.def format.")

    def _makePlotRegionOpts(self, parent):
        """Draw collapsible frame for plot region options."""
        df = DisclosureFrame(parent, text=" Plot Region")
        df.pack(fill="x")
        f = df.frame
        # Radio Button for polar system
        self.psradio_var = tk.StringVar(value="1")
        psradio_opts = [(1, "Polar 1: Theta rotates from X, " +
                         "Phi rotates from Y towards Z"),
                        (2, "Polar 2: Theta rotates from Y, " +
                            "Phi rotates from X away from Z")]
        for i in range(2):
            val, text = psradio_opts[i]
            polarSystemRadio = tk.Radiobutton(f, text=text,
                                              justify='left', value=val,
                                              variable=self.psradio_var)
            polarSystemRadio.grid(row=i, column=0, columnspan=2, sticky='w')
        # Open entry fields for polar angle ranges
        self.angleGroup = Pmw.Group(f, tag_text="Angle Ranges")
        self.angleGroup.grid(row=3, column=0, sticky='w')
        # Phi
        self.phiStartEntry = Pmw.EntryField(self.angleGroup.interior(),
                                            label_text="Phi start: ",
                                            labelpos='w', validate='real',
                                            entry_width=6,
                                            entry_justify='right', value=0.0)
        self.phiStartEntry.grid(row=3, column=0, sticky='e')
        self.phiEndEntry = Pmw.EntryField(self.angleGroup.interior(),
                                          label_text=" Phi end: ",
                                          labelpos='w', validate='real',
                                          entry_width=6,
                                          entry_justify='right', value=180.0)
        self.phiEndEntry.grid(row=3, column=1, sticky='e')
        # Theta
        self.thetaStartEntry = Pmw.EntryField(self.angleGroup.interior(),
                                              label_text="Theta start: ",
                                              labelpos='w', validate='real',
                                              entry_width=6,
                                              entry_justify='right', value=0.0)
        self.thetaStartEntry.grid(row=4, column=0, sticky='e')
        self.thetaEndEntry = Pmw.EntryField(self.angleGroup.interior(),
                                            label_text=" Theta end: ",
                                            labelpos='w', validate='real',
                                            entry_width=6,
                                            entry_justify='right', value=180.0)
        self.thetaEndEntry.grid(row=4, column=1, sticky='e')
        # Angle increments
        self.angleDeltaEntry = Pmw.EntryField(
                self.angleGroup.interior(),
                label_text="Increment angle in steps of: ", labelpos='w',
                validate='real', entry_width=4, entry_justify='right',
                value=1.0)
        self.angleDeltaEntry.grid(row=5, column=0, columnspan=2)
        # Open entry fields for XYZ ranges
        self.XYZGroup = Pmw.Group(f, tag_text="XYZ Ranges")
        self.XYZGroup.grid(row=3, column=1, sticky='w')
        # X
        self.xStartEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                          label_text="X start: ",
                                          labelpos='w', validate='real',
                                          entry_width=14,
                                          entry_justify='right',
                                          value=-3.402823e+38)
        self.xStartEntry.grid(row=3, column=0, sticky='e')
        self.xEndEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                        label_text=" X end: ",
                                        labelpos='w', validate='real',
                                        entry_width=14,
                                        entry_justify='right',
                                        value=3.402823e+38)
        self.xEndEntry.grid(row=3, column=1, sticky='e')
        # Y
        self.yStartEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                          label_text="Y start: ",
                                          labelpos='w', validate='real',
                                          entry_width=14,
                                          entry_justify='right',
                                          value=-3.402823e+38)
        self.yStartEntry.grid(row=4, column=0, sticky='e')
        self.yEndEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                        label_text=" Y end: ",
                                        labelpos='w', validate='real',
                                        entry_width=14,
                                        entry_justify='right',
                                        value=3.402823e+38)
        self.yEndEntry.grid(row=4, column=1, sticky='e')
        # Z
        self.zStartEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                          label_text="Z start: ",
                                          labelpos='w', validate='real',
                                          entry_width=14,
                                          entry_justify='right',
                                          value=-3.402823e+38)
        self.zStartEntry.grid(row=5, column=0, sticky='e')
        self.zEndEntry = Pmw.EntryField(self.XYZGroup.interior(),
                                        label_text=" Z end: ",
                                        labelpos='w', validate='real',
                                        entry_width=14,
                                        entry_justify='right',
                                        value=3.402823e+38)
        self.zEndEntry.grid(row=5, column=1, sticky='e')

    def _makeColorOpts(self, parent):
        """Draw collapsible frame for color options."""
        df = DisclosureFrame(parent, text=" Color Settings")
        df.pack(fill="x")
        f = df.frame
        # Color selection dropdown
        self.color_methods = ["None",
                              "Residue type",
                              "Radius, small (Red) to large (Blue)",
                              "Radius, small (Blue) to large (Red)",
                              "Density, negative (Red) to positive (Blue)",
                              "Density, negative (Blue) to positive (Red)",
                              "From PDB"]
        self.colorMenu = Pmw.OptionMenu(f, initialitem="None",
                                        label_text="Color method:",
                                        labelpos='w', items=self.color_methods)
        self.colorMenu.grid(row=0, column=0, sticky='w')
        # Color gradient settings entry fields
        self.gradSettingsGroup = Pmw.Group(
                f, tag_text="Color gradient settings: ")
        self.gradSettingsGroup.grid(row=1, column=0, sticky='w')
        self.dMinEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                        label_text="Low plot threshold: ",
                                        labelpos='w', validate='real',
                                        entry_width=6,
                                        entry_justify='right')
        self.dMinEntry.grid(row=0, column=0, sticky='e')
        self.dMaxEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                        label_text="High plot threshold: ",
                                        labelpos='w', validate='real',
                                        entry_width=6,
                                        entry_justify='right')
        self.dMaxEntry.grid(row=1, column=0, sticky='e')
        self.dColorMidEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                             label_text=" Gradient mid point: ",
                                             labelpos='w', validate='real',
                                             entry_width=6,
                                             entry_justify='right')
        self.dColorMidEntry.grid(row=0, column=1, sticky='e')
        self.dColorMinEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                             label_text=" Gamma: ",
                                             labelpos='w', validate='real',
                                             entry_width=6,
                                             entry_justify='right')
        self.dColorMinEntry.grid(row=1, column=1, sticky='e')

    def _makePrintCmd(self, parent):
        """Draw text box for printing command."""
        self.cmdTxtBox = Pmw.ScrolledText(parent, label_text="Command",
                                          labelpos="n", usehullsize=1,
                                          hull_width=400, hull_height=100,
                                          text_padx=4, text_pady=4)
        self.cmdTxtBox.configure(text_state="disabled")
        # Allow clicking to set focus, for copying text from text box
        self.cmdTxtBox.bind("<1>", lambda event: self.cmdTxtBox.focus_set())

    def updateParams(self):
        """Update wrapper attributes from GUI input."""
        # Get path to input model
        if self.inputPDBMenu.getvalue() is not None:
            input_pdb_path = self.inputPDBMenu.getvalue().openedAs[0]
            if not path.isfile(input_pdb_path) and len(input_pdb_path) == 4:
                # Input model is from a fetched file
                id_code = input_pdb_path.upper()
                input_pdb_path = self.getFetchedModelPath(id_code)
            # TODO: Handle conversion for mmCIF files.
        else:
            input_pdb_path = None
        self.wrapper.PDB = input_pdb_path

        # Set output path
        # TODO: Allow user to specify a custom output path.
        # Otherwise, default to cache_dir from the Chimera preferences
        if input_pdb_path is not None:
            filename = path.basename(input_pdb_path)
            if filename.endswith(".pdb"):
                filename = filename.replace(".pdb", ".ps")
            else:
                filename += ".ps"
        cache_dir = preferences.get(FETCH_PREFERENCES, FETCH_DIRECTORY)
        try:
            from OpenSave import tildeExpand
            cache_dir = tildeExpand(cache_dir)
            if not path.exists(path.join(cache_dir, "RIVEM")):
                os.makedirs(path.join(cache_dir, "RIVEM"))
            out_path = path.join(cache_dir, "RIVEM", filename)
            self.wrapper.out = out_path
        except UnboundLocalError:
            raise UserError("Error while setting output path.")

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
        # Set dmin and dmax
        dmin = self.dMinEntry.getvalue()
        dmax = self.dMaxEntry.getvalue()
        if dmin is not None:
            self.wrapper.dmin = dmin
        if dmax is not None:
            self.wrapper.dmax = dmax

    def getFetchedModelPath(self, id_code):
        """Find the path to a fetched model (one that wasn't opened from a
        file)."""
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
    """Return a list of currently loaded models.
    This method is here for reference, and not currently used."""
    from chimera import openModels as om, Molecule
    from VolumeViewer import Volume
    mlist = om.list(modelTypes=[Molecule, Volume])
    mlist = ['selected atoms'] + mlist
    return mlist


# Register dialogs
dialogs.register(RIVEM_GUI.name, RIVEM_GUI, replace=True)
