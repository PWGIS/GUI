# This is my own work, with assistance from the wxGlade GUI wireframe composer
# ------------------------------------------------------------------------------
# Updates 1/26/2018: Created a method that populates a txtCtrl with the fileDialog file path and file name
# ------------------------------------------------------------------------------

import wx, arcpy, os

parentSDE = r"C:\Users\MiguelTo\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\publiworks_TAX_SQL_Miguelto.sde"


class FrmCheckSubmitall(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.rbxUtilitySelect = wx.RadioBox(self, wx.ID_ANY, "Utility", choices=["Stormwater", "Sewer", "Water"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.txtFeaturesPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.btnSelectFeatures = wx.Button(self, wx.ID_ANY, "Select")
        self.btnSelectFeatures.Bind(wx.EVT_BUTTON, self.dialog_select_features)
        self.txtPipesPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.btnSelectPipes = wx.Button(self, wx.ID_ANY, "Select")
        self.btnSelectPipes.Bind(wx.EVT_BUTTON, self.dialog_select_pipes)
        self.bxOutput = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.cbxDraw = wx.CheckBox(self, wx.ID_ANY, "Draw")
        self.btnClear = wx.Button(self, wx.ID_ANY, "Clear")
        self.btnZoom = wx.Button(self, wx.ID_ANY, "Zoom")
        self.btnRun = wx.Button(self, wx.ID_ANY, "Run", style=wx.BU_EXACTFIT)
        self.btnRun.Bind(wx.EVT_BUTTON, self.main)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        # begin wxGlade: FrmCheckSubmitall.__set_properties
        self.SetTitle("Check Submittal")
        self.rbxUtilitySelect.SetSelection(0)
        self.btnSelectFeatures.SetMinSize((80, 20))
        self.btnSelectPipes.SetMinSize((80, 20))
        self.cbxDraw.SetValue(1)
        self.btnClear.SetMinSize((50, 20))
        self.btnZoom.SetMinSize((50, 20))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FrmCheckSubmitall.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.rbxUtilitySelect, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        lblFeatures = wx.StaticText(self, wx.ID_ANY, "Features: ")
        sizer_6.Add(lblFeatures, 0, wx.ALIGN_CENTER | wx.LEFT, 16)
        sizer_6.Add(self.txtFeaturesPath, 1, 0, 0)
        sizer_6.Add(self.btnSelectFeatures, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        lblPipes = wx.StaticText(self, wx.ID_ANY, "Pipes: ")
        sizer_7.Add(lblPipes, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 16)
        sizer_7.Add(self.txtPipesPath, 1, 0, 0)
        sizer_7.Add(self.btnSelectPipes, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        sizer_5.Add(sizer_7, 0, wx.ALL | wx.EXPAND, 0)
        sizer_5.Add(self.bxOutput, 1, wx.ALL | wx.EXPAND, 10)
        sizer_8.Add(self.cbxDraw, 0, wx.LEFT | wx.RIGHT, 10)
        sizer_8.Add(self.btnClear, 0, wx.RIGHT, 10)
        sizer_8.Add(self.btnZoom, 0, 0, 0)
        sizer_8.Add((20, 20), 1, 0, 0)
        sizer_8.Add(self.btnRun, 0, wx.BOTTOM | wx.RIGHT, 10)
        sizer_5.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.SetSize((400, 300))
        # end wxGlade

    def dialog_select_features(self, event):
        # Begin Dialog Features Method.
        fileDialog = wx.FileDialog(self, "Select the Features File", wildcard="Text files (*.txt)|*.txt",
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        value = fileDialog.Directory + "\\" + fileDialog.Filename
        self.txtFeaturesPath.SetValue(value)

    def dialog_select_pipes(self, event):
        # Begin Dialog Pipes Method.
        fileDialog = wx.FileDialog(self, "Select the Features File", wildcard="Text files (*.txt)|*.txt",
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        value = fileDialog.Directory + "\\" + fileDialog.Filename
        self.txtPipesPath.SetValue(value)

    def verify_input(self):
        """ Returns a tuple that shows the existence of the two paths provided.
        The first value represents the Features path, while the second represents the Pipes.
        """
        InputTup = (os.path.exists(self.txtFeaturesPath.GetValue()), os.path.exists(self.txtPipesPath.GetValue()))

        return InputTup

    def order_key(self):
        """ Returns a dictionary where the key is the valid column name
        the value is the key's position within the input."""
        # prepare the header of the file for processing
        feat_key = {}
        pipe_key = {}
        if self.rbxUtilitySelect.GetSelection() == 0 or self.rbxUtilitySelect.GetSelection() == 1:
            if self.verify_input()[0]:
                f = open(self.txtFeaturesPath.GetValue())
                fheader = f.readlines()
                fheader.reverse()
                fheader = fheader.pop()
                fheader = fheader.upper()
                fheader = fheader.replace("NORTHING", "Y")
                fheader = fheader.replace("EASTING", "X")
                fheader = fheader.replace('\n', '')
                fheader = fheader.split(",")

                if "ID" in fheader:
                    feat_key["ID"] = fheader.index("ID")
                if "TYPE" in fheader:
                    feat_key["TYPE"] = fheader.index("TYPE")
                if "Y" in fheader:
                    feat_key["Y"] = fheader.index("Y")
                if "X" in fheader:
                    feat_key["X"] = fheader.index("X")
                if "INVERT" in fheader:
                    feat_key["INVERT"] = fheader.index("INVERT")
                if "MATERIAL" in fheader:
                    feat_key["MATERIAL"] = fheader.index("MATERIAL")
                if "ELEVATION" in fheader:
                    feat_key["ELEVATION"] = fheader.index("ELEVATION")

                if "ID" not in fheader:
                    self.bxOutput.AppendText("Missing ID field in Header\n")
                if "TYPE" not in fheader:
                    self.bxOutput.AppendText("Missing TYPE field in Header\n")
                if "Y" not in fheader:
                    self.bxOutput.AppendText("Missing NORTHING field in Header\n")
                if "X" not in fheader:
                    self.bxOutput.AppendText("Missing EASTING field in Header\n")
                if "INVERT" not in fheader:
                    self.bxOutput.AppendText("Missing INVERT field in Header\n")
                if "MATERIAL" not in fheader:
                    self.bxOutput.AppendText("Missing MATERIAL field in Header\n")
            if self.verify_input()[1]:
                p = open(self.txtPipesPath.GetValue())
                pheader = p.readlines()
                pheader.reverse()
                pheader = pheader.pop()
                pheader = pheader.upper()
                pheader = pheader.replace('\n', '')
                pheader = pheader.split(",")

                if "ID" in pheader:
                    pipe_key["ID"] = pheader.index("ID")
                if "SIZE" in pheader:
                    pipe_key["SIZE"] = pheader.index("SIZE")
                if "MATERIAL" in pheader:
                    pipe_key["MATERIAL"] = pheader.index("MATERIAL")
                if "USID" in pheader:
                    pipe_key["USID"] = pheader.index("USID")
                if "DSID" in pheader:
                    pipe_key["DSID"] = pheader.index("DSID")

                count = 0
                for val in pheader:
                    if val in ['DSINVERT', 'DOWNSTREAM INVERT', 'DSI']:
                        pheader[val] = "USINV"
                        break
                    count = count + 1
                if "DSINV" in pheader:
                    pipe_key["DSINV"] = pheader.index("DSINV")

                count = 0
                for val in pheader:
                    if val in ['USINVERT', 'UPSTREAM INVERT', 'USI']:
                        pheader[val] = "USINV"
                        break
                    count = count + 1
                if "USINV" in pheader:
                    pipe_key["USINV"] = pheader.index("USINV")

                if "SLOPE" in pheader:
                    pipe_key["SLOPE"] = pheader.index("SLOPE")
                if "LENGTH" in pheader or "LEN" in pheader:
                    pipe_key["LENGTH"] = pheader.index("LENGTH")

                if "ID" not in pheader:
                    self.bxOutput.AppendText("Missing ID field in Header\n")
                if "SIZE" not in pheader:
                    self.bxOutput.AppendText("Missing SIZE field in Header\n")
                if "MATERIAL" not in pheader:
                    self.bxOutput.AppendText("Missing MATERIAL field in Header\n")
                if "USID" not in pheader:
                    self.bxOutput.AppendText("Missing USID field in Header\n")
                if "DSID" not in pheader:
                    self.bxOutput.AppendText("Missing DSID field in Header\n")
                if "USINV" not in pheader:
                    self.bxOutput.AppendText("Missing USINV field in Header\n")
                if "DSINV" not in pheader:
                    self.bxOutput.AppendText("Missing DSINV field in Header\n")
                if "SLOPE" not in pheader:
                    self.bxOutput.AppendText("Missing SLOPE field in Header\n")
                if "LENGTH" not in pheader and "LEN" not in pheader:
                    self.bxOutput.AppendText("Missing LENGTH field in Header\n")
            else:
                self.bxOutput.AppendText("\nNo Valid Pipes file provided. Skipping Pipes import.")
        elif self.rbxUtilitySelect.GetSelection() == 2:
            if self.verify_input()[0]:
                f = open(self.txtFeaturesPath.GetValue())
                fheader = f.readlines()
                fheader.reverse()
                fheader = fheader.pop()
                fheader = fheader.upper()
                fheader = fheader.replace("NORTHING", "Y")
                fheader = fheader.replace("EASTING", "X")
                fheader = fheader.replace('\n', '')
                fheader = fheader.split(",")

                if "ID" in fheader:
                    feat_key["ID"] = fheader.index("ID")
                if "TYPE" in fheader:
                    feat_key["TYPE"] = fheader.index("TYPE")
                if "Y" in fheader:
                    feat_key["Y"] = fheader.index("Y")
                if "X" in fheader:
                    feat_key["X"] = fheader.index("X")
                if "ELEVATION" in fheader:
                    feat_key["ELEVATION"] = fheader.index("ELEVATION")
                if "DESCRIPTION" in fheader:
                    feat_key["DESCRIPTION"] = fheader.index("DESCRIPTION")

                if "ID" not in fheader:
                    self.bxOutput.AppendText("Missing ID field in Header\n")
                if "TYPE" not in fheader:
                    self.bxOutput.AppendText("Missing TYPE field in Header\n")
                if "Y" not in fheader:
                    self.bxOutput.AppendText("Missing NORTHING field in Header\n")
                if "X" not in fheader:
                    self.bxOutput.AppendText("Missing EASTING field in Header\n")
                if "DESCRIPTION" not in fheader:
                    self.bxOutput.AppendText("Missing DESCRIPTION field in Header\n")
            else:
                self.bxOutput.AppendText("\nNo Valid Features file provided. Skipping Feature import.")
            if self.verify_input()[1]:
                p = open(self.txtPipesPath.GetValue())
                pheader = p.readlines()
                pheader.reverse()
                pheader = pheader.pop()
                pheader = pheader.upper()
                pheader = pheader.replace('\n', '')
                pheader = pheader.split(",")

                if "ID" in pheader:
                    pipe_key["ID"] = pheader.index("ID")
                if "SIZE" in pheader:
                    pipe_key["SIZE"] = pheader.index("SIZE")
                if "MATERIAL" in pheader:
                    pipe_key["MATERIAL"] = pheader.index("MATERIAL")
                if "FEATUREID1" in pheader:
                    pipe_key["FEATUREID1"] = pheader.index("FEATUREID1")
                if "FEATUREID2" in pheader:
                    pipe_key["FEATUREID2"] = pheader.index("FEATUREID2")

                if "ID" not in pheader:
                    self.bxOutput.AppendText("Missing ID field in Header\n")
                if "SIZE" not in pheader:
                    self.bxOutput.AppendText("Missing SIZE field in Header\n")
                if "MATERIAL" not in pheader:
                    self.bxOutput.AppendText("Missing MATERIAL field in Header\n")
                if "FEATUREID1" not in pheader:
                    self.bxOutput.AppendText("Missing FEATUREID1 field in Header\n")
                if "FEATUREID2" not in pheader:
                    self.bxOutput.AppendText("Missing FEATUREID2 field in Header\n")
            else:
                self.bxOutput.AppendText("\nNo Valid Pipes file provided. Skipping Pipes import.")
        key = (feat_key,pipe_key)
        return key

    def main(self, event):
        # Import features currently only works  on a premade file that has no header and
        # only has an X, and Y value delimited with a comma
        self.bxOutput.SetValue("")
        Key = self.order_key()
        #
        if os.path.exists(self.txtFeaturesPath.GetValue()):
            f = open(self.txtFeaturesPath.GetValue())
            lstNodes = f.readlines()
            lstNodes.reverse()
            lstNodes.pop()
        env = arcpy.da.Editor("in_memory")

    # def import_features(self):
    # def import_pipes(self):
    # def create_version():
    # def push_updates():

if __name__ == '__main__':
    app=wx.App()
    frame = FrmCheckSubmitall(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
