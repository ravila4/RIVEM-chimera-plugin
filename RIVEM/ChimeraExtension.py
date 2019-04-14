"""
UCSF Chimera plugin for RIVEM
Last edited: 2019-04-01
"""


import chimera.extension


class RIVEM_EMO(chimera.extension.EMO):
    """Create an Extension Mananagement Object (EMO)."""

    def name(self):
        return "RIVEM"

    def description(self):
        return "Project density onto a sterographic sphere."

    def categories(self):
        return ["Surface/Binding Analysis"]

    def icon(self):
        return self.path("logo.png")

    def activate(self):
        from chimera.dialogs import display
        display(self.module("gui").RIVEM_GUI.name)
        return None


# Register dialogs and menu entries
chimera.extension.manager.registerExtension(RIVEM_EMO(__file__))

# Register commands


def runRIVEM(cmd, args):
    from RIVEM import rivem


import Midas.midas_text
Midas.midas_text.addCommand('rivem', runRIVEM, None, help=True)
