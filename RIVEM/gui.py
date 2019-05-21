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
        self.matrixMenu.grid(row=2, column=0, sticky='w')
        self.balloon.bind(self.matrixMenu,
                          "Read in the matrix for the PDB and the maps.\n" +
                          "The matrix should be in CNS ncs.def format.")
        # Resudue label options for PDB
        self._labelVar = tk.IntVar()
        self.residueLabelCheckBox = tk.Checkbutton(
                f, text="Add residue labels", variable=self._labelVar)
        self.residueLabelCheckBox.grid(row=0, column=1, sticky='w')
        self._colorContourOpts = {"Blue": 0, "Red": 1, "Gray": 2,
                                  "Orange": 3, "Yellow": 4, "Tan": 5,
                                  "Silver": 6, "Green": 7, "White": 8,
                                  "Pink": 9, "Cyan": 10, "Purple": 11,
                                  "Lime": 12, "Mauve": 13, "Ochre": 14,
                                  "Iceblue": 15, "Black": 16}
        self.residueLabelColor = Pmw.OptionMenu(
                f, initialitem="Black", label_text="Label color:",
                labelpos='w', items=self._colorContourOpts)
        self.residueLabelColor.grid(row=1, column=1, sticky='w')
        self.residueLabelSize = Pmw.EntryField(f, label_text=" Label size:",
                                               labelpos='w', validate='real',
                                               entry_width=3,
                                               entry_justify='right', value=0)
        self.residueLabelSize.grid(row=1, column=2, sticky='w')

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
        self._color_methods = ["None",
                               "Residue type",
                               "Radius, small (Red) to large (Blue)",
                               "Radius, small (Blue) to large (Red)",
                               "Density, negative (Red) to positive (Blue)",
                               "Density, negative (Blue) to positive (Red)",
                               "From PDB"]
        self.colorMenu = Pmw.OptionMenu(
                f, initialitem="None", label_text="Color method:",
                labelpos='w', items=self._color_methods)
        self.colorMenu.grid(row=0, column=0, sticky='w')
        # Color gradient settings
        self.gradSettingsGroup = Pmw.Group(
                f, tag_text="Color Gradient Settings")
        self.gradSettingsGroup.grid(row=1, column=0, sticky='w')
        # dMin
        self.dMinEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                        label_text="Low threshold: ",
                                        labelpos='w', validate='real',
                                        entry_width=8,
                                        entry_justify='right')
        self.dMinEntry.grid(row=0, column=0, sticky='e')
        # dMax
        self.dMaxEntry = Pmw.EntryField(self.gradSettingsGroup.interior(),
                                        label_text="High threshold: ",
                                        labelpos='w', validate='real',
                                        entry_width=8,
                                        entry_justify='right')
        self.dMaxEntry.grid(row=1, column=0, sticky='e')
        # color_mid_point
        self.gradMidLbl = tk.Label(self.gradSettingsGroup.interior(),
                                   text=" Gradient midpoint: ")
        self._gradMidVar = tk.StringVar(self.gradSettingsGroup.interior())
        self.gradMidScale = tk.Scale(self.gradSettingsGroup.interior(),
                                     from_=0.1, to_=1, orient="horizontal",
                                     resolution=0.1, length=150,
                                     command=lambda x: self._gradMidVar.set(
                                         "%.1f " % float(x)), showvalue=False)
        self.gradMidScale.set(0.5)
        self._gradMidVar.set("0.5 ")
        self.gradMidStatusLbl = tk.Label(self.gradSettingsGroup.interior(),
                                         textvariable=self._gradMidVar)
        self.gradMidLbl.grid(row=0, column=1, sticky='e')
        self.gradMidScale.grid(row=0, column=2, sticky='w')
        self.gradMidStatusLbl.grid(row=0, column=3, sticky='w')
        # color_min
        self.gammaLbl = tk.Label(self.gradSettingsGroup.interior(),
                                 text=" Gradient gamma: ")
        self._gammaVar = tk.StringVar(self.gradSettingsGroup.interior())
        self.gammaScale = tk.Scale(self.gradSettingsGroup.interior(),
                                   from_=-1, to_=1, orient="horizontal",
                                   resolution=0.1, length=150,
                                   command=lambda x: self._gammaVar.set(
                                       "%.1f " % float(x)), showvalue=False)
        self.gammaScale.set(0.0)
        self._gammaVar.set("0.0 ")
        self.gammaStatusLbl = tk.Label(self.gradSettingsGroup.interior(),
                                       textvariable=self._gammaVar)
        self.gammaLbl.grid(row=1, column=1, sticky='e')
        self.gammaScale.grid(row=1, column=2, sticky='w')
        self.gammaStatusLbl.grid(row=1, column=3, sticky='w')

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
        # Residue labels
        self.wrapper.label = self._labelVar.get()
        if self._labelVar.get() == 1:
            # Show label size and color options
            size = self.residueLabelSize.getvalue()
            if size != "":
                self.wrapper.label_size = int(size)
            else:
                self.wrapper.label_size = 0
            color = self.residueLabelColor.getvalue()
            self.wrapper.label_color = self._colorContourOpts[color]
        # Set plot region
        begPhi = self.phiStartEntry.getvalue()
        endPhi = self.phiEndEntry.getvalue()
        begTheta = self.thetaStartEntry.getvalue()
        endTheta = self.thetaEndEntry.getvalue()
        deltaAngle = self.angleDeltaEntry.getvalue()
        begX = self.xStartEntry.getvalue()
        endX = self.xEndEntry.getvalue()
        begY = self.yStartEntry.getvalue()
        endY = self.yEndEntry.getvalue()
        begZ = self.zStartEntry.getvalue()
        endZ = self.zEndEntry.getvalue()
        if begPhi != "":
            self.wrapper.begPhi = float(begPhi)
        else:
            self.wrapper.begPhi = 0.0
        if endPhi != "":
            self.wrapper.endPhi = float(endPhi)
        else:
            self.wrapper.endPhi = 180.0
        if begTheta != "":
            self.wrapper.begTheta = float(begTheta)
        else:
            self.wrapper.begTheta = 0.0
        if endTheta != "":
            self.wrapper.endTheta = float(endTheta)
        else:
            self.wrapper.endTheta = 180.0
        if deltaAngle != "":
            self.wrapper.deltaAngle = float(deltaAngle)
        else:
            self.wrapper.deltaAngle = 1.0
        if begX != "":
            self.wrapper.begX = float(begX)
        else:
            self.wrapper.begX = -3.402823e+38
        if endX != "":
            self.wrapper.endX = float(endX)
        else:
            self.wrapper.endX = 3.402823e+38
        if begY != "":
            self.wrapper.begY = float(begY)
        else:
            self.wrapper.begY = -3.402823e+38
        if endY != "":
            self.wrapper.endY = float(endY)
        else:
            self.wrapper.endY = 3.402823e+38
        if begZ != "":
            self.wrapper.begZ = float(begZ)
        else:
            self.wrapper.begZ = -3.402823e+38
        if endZ != "":
            self.wrapper.endZ = float(endZ)
        else:
            self.wrapper.endZ = 3.402823e+38
        # Set color method
        cm = self.colorMenu.getvalue()
        cm_index = self._color_methods.index(cm)
        color_codes = [None, 1, 2, 3, 4, 5, 6]
        # TODO: If cm_index is 6, take input PDB
        self.wrapper.color_method = color_codes[cm_index]
        self.wrapper.dmin = None
        self.wrapper.dmax = None
        self.wrapper.color_mid_point = None
        self.wrapper.color_min = None
        if color_codes[cm_index] is not None:
            # Set dmin and dmax
            dmin = self.dMinEntry.getvalue()
            dmax = self.dMaxEntry.getvalue()
            if dmin != "":
                self.wrapper.dmin = dmin
            if dmax != "":
                self.wrapper.dmax = dmax
            # Set color_mid_point and color_min
            self.wrapper.color_mid_point = self.gradMidScale.get()
            self.wrapper.color_min = self.gammaScale.get()

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
        # TODO: This part goes away after replacing with a messagebox.
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
