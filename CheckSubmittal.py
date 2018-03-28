# This is my own work, with assistance from the wxGlade GUI wireframe composer
# ------------------------------------------------------------------------------
# Updates 1/26/2018: Created a method that populates a txtCtrl with the fileDialog file path and file name
# ------------------------------------------------------------------------------

import wx, arcpy, os


class FrmCheckSubmital(wx.Frame):
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
        self.btnRun.Bind(wx.EVT_BUTTON, self.import_features)

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
        if self.rbxUtilitySelect.GetSelection() == 0:
            headList = {}
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
                    headList["ID"] = fheader.index("ID")
                if "TYPE" in fheader:
                    headList["TYPE"] = fheader.index("TYPE")
                if "Y" in fheader:
                    headList["Y"] = fheader.index("Y")
                if "X" in fheader:
                    headList["X"] = fheader.index("X")
                if "INVERT" in fheader:
                    headList["INVERT"] = fheader.index("INVERT")
                if "MATERIAL" in fheader:
                    headList["MATERIAL"] = fheader.index("MATERIAL")
                if "ELEVATION" in fheader:
                    headList["ELEVATION"] = fheader.index("ELEVATION")

                if "ID" not in fheader:
                    print "Missing ID field in Header"
                if "TYPE" not in fheader:
                    print "Missing TYPE field in Header"
                if "Y" not in fheader:
                    print "Missing NORTHING field in Header"
                if "X" not in fheader:
                    print "Missing EASTING field in Header"
                if "INVERT" not in fheader:
                    print "Missing INVERT field in Header"
                if "MATERIAL" not in fheader:
                    print "Missing MATERIAL field in Header"
            else:
                print "No Valid Features file provided. Skipping Feature import."

            headList2 = {}
            if self.verify_input()[1]:
                p = open(self.txtPipesPath.GetValue())
                pheader = p.readlines()
                pheader.reverse()
                pheader = pheader.pop()
                print pheader
                pheader = pheader.upper()
                pheader = pheader.replace('\n', '')
                pheader = pheader.split(",")
                print pheader

                if "ID" in pheader:
                    headList2["ID"] = pheader.index("ID")
                if "SIZE" in pheader:
                    headList2["SIZE"] = pheader.index("SIZE")
                if "MATERIAL" in pheader:
                    headList2["MATERIAL"] = pheader.index("MATERIAL")
                if "USID" in pheader:
                    headList2["USID"] = pheader.index("USID")
                if "DSID" in pheader:
                    headList2["DSID"] = pheader.index("DSID")

                count = 0
                for val in pheader:
                    if val in ['DSINVERT', 'DOWNSTREAM INVERT', 'DSI']:
                        pheader[val] = "USINV"
                        break
                    count = count + 1
                if "DSINV" in pheader:
                    headList2["DSINV"] = pheader.index("DSINV")

                count = 0
                for val in pheader:
                    if val in ['USINVERT', 'UPSTREAM INVERT', 'USI']:
                        pheader[val] = "USINV"
                        break
                    count = count + 1
                if "USINV" in pheader:
                    headList2["USINV"] = pheader.index("USINV")

                if "SLOPE" in pheader:
                    headList2["SLOPE"] = pheader.index("SLOPE")
                if "LENGTH" in pheader or "LEN" in pheader:
                    headList2["LENGTH"] = pheader.index("LENGTH")

                if "ID" not in pheader:
                    print "Missing ID field in Header"
                if "SIZE" not in pheader:
                    print "Missing SIZE field in Header"
                if "MATERIAL" not in pheader:
                    print "Missing MATERIAL field in Header"
                if "USID" not in pheader:
                    print "Missing USID field in Header"
                if "DSID" not in pheader:
                    print "Missing DSID field in Header"
                if "USINV" not in pheader:
                    print "Missing USINV field in Header"
                if "DSINV" not in pheader:
                    print "Missing DSINV field in Header"
                if "SLOPE" not in pheader:
                    print "Missing SLOPE field in Header"
                if "LENGTH" not in pheader and "LEN" not in pheader:
                    print "Missing LENGTH field in Header"
            else:
                print "No Valid Pipes file provided. Skipping Pipes import."
            Key = (headList,headList2)
            return Key

    def import_features(self, event):
        # Import features currently only works  on a premade file that has no header and
        # only has an X, and Y value delimited with a comma
        Key = self.order_key()
        #
        print Key
        if os.path.exists(self.txtFeaturesPath.GetValue()):
            f = open(self.txtFeaturesPath.GetValue())
            lstNodes = f.readlines()
            lstNodes.reverse()
            lstNodes.pop()
            self.bxOutput.SetValue("")
        env = arcpy.da.Editor("in_memory")

if __name__ == '__main__':
    app=wx.App()
    frame = FrmCheckSubmital(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
