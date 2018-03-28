# This is my own work, with assistance from the wxGlade GUI wireframe composer
# ------------------------------------------------------------------------------
# Updates 1/26/2018: Created a method that populates a txtCtrl with the fileDialog file path and file name
# ------------------------------------------------------------------------------

import wx, arcpy, os


class frmCheckSubmital(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.rbxUtilitySelect = wx.RadioBox(self, wx.ID_ANY, "Utility", choices=["Stormwater", "Sewer", "Water"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.txtFeaturesPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.btnSelectFeatures = wx.Button(self, wx.ID_ANY, "Select")
        self.btnSelectFeatures.Bind(wx.EVT_BUTTON, self.dialogSelectFeatures)
        self.txtPipesPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.btnSelectPipes = wx.Button(self, wx.ID_ANY, "Select")
        self.btnSelectPipes.Bind(wx.EVT_BUTTON, self.dialogSelectPipes)
        self.bxOutput = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.cbxDraw = wx.CheckBox(self, wx.ID_ANY, "Draw")
        self.btnClear = wx.Button(self, wx.ID_ANY, "Clear")
        self.btnZoom = wx.Button(self, wx.ID_ANY, "Zoom")
        self.btnRun = wx.Button(self, wx.ID_ANY, "Run", style=wx.BU_EXACTFIT)
        self.btnRun.Bind(wx.EVT_BUTTON, self.importFeatures)

        self.__set_properties()
        self.__do_layout()


    def __set_properties(self):
        # begin wxGlade: frmCheckSubmitall.__set_properties
        self.SetTitle("Check Submittal")
        self.rbxUtilitySelect.SetSelection(0)
        self.btnSelectFeatures.SetMinSize((80, 20))
        self.btnSelectPipes.SetMinSize((80, 20))
        self.cbxDraw.SetValue(1)
        self.btnClear.SetMinSize((50, 20))
        self.btnZoom.SetMinSize((50, 20))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: frmCheckSubmitall.__do_layout
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
# Begin Dialog Method. These two methods are somewhat redundant and may be combined with an argument that parses the
    # textCtrl outputs depending on the button pressed
    def dialogSelectFeatures(self, event):

        fileDialog = wx.FileDialog(self, "Select the Features File", wildcard="Text files (*.txt)|*.txt",
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        value = fileDialog.Directory + "\\" + fileDialog.Filename
        self.txtFeaturesPath.SetValue(value)

    def dialogSelectPipes(self, event):

        fileDialog = wx.FileDialog(self, "Select the Features File", wildcard="Text files (*.txt)|*.txt",
                                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        value = fileDialog.Directory + "\\" + fileDialog.Filename
        self.txtPipesPath.SetValue(value)
    # Import features currently only works  on a premade file that has no header and
    # only has an X, and Y value delimited with a comma

    # Determines the order of the input header and returns a dictionary of indexed locations
    def orderkey(self, header):

        # prepare the header of the file for processing
        f = open(self.txtFeaturesPath.GetValue())
        header = f.readlines()
        header.reverse()
        header = header.pop()
        header = header.upper()
        header = header.replace("NORTHING", "Y")
        header = header.replace("EASTING", "X")
        header = header.replace('\n', '')
        header = header.split(",")


        headList = {}

        if "ID" in header:
            headList["ID"] = header.index("ID")
        if "TYPE" in header:
            headList["TYPE"] = header.index("TYPE")
        if "Y" in header:
            headList["Y"] = header.index("Y")
        if "X" in header:
            headList["X"] = header.index("X")
        if "INVERT" in header:
            headList["INVERT"] = header.index("INVERT")
        if "MATERIAL" in header:
            headList["MATERIAL"] = header.index("MATERIAL")
        if "ELEVATION" in header:
            headList["ELEVATION"] = header.index("ELEVATION")
        return headList

    def importFeatures(self, event):
        arcpy.env.workspace = "D:/Test.gdb"
        f = open(self.txtFeaturesPath.GetValue())
        lstNodes = f.readlines()
        lstNodes.reverse()
        lstNodes.pop()
        self.bxOutput.SetValue("")
        header = lstNodes.pop()
        print header
        okey = self.orderkey(header)
        print "OKey Value: "
        print okey

        try:
            edit = arcpy.da.Editor(r"D:/Test.gdb")
            edit.startEditing(True)
            cntr = 0
            with arcpy.da.InsertCursor("D:/Test.gdb/swNodesTest", ("SHAPE@XY", "ASBUILTID", "PROJECTID")) as cur:
                for node in lstNodes:
                    node = node.replace('\n','')
                    print node
                    cntr += 1
                    vals = node.split(",")
                    latitude = float(vals[0])
                    longitude = float(vals[1])
                    ABID = "FTR-" + str(cntr)
                    PID = float(1354.07)
                    print("Latitude: " + str(latitude) + " x Longitude: " + str(longitude))
                    self.bxOutput.AppendText("Latitude: " + str(latitude) + " x Longitude: " + str(longitude))
                    rowValue = [(latitude, longitude), ABID, PID]
                    self.bxOutput.AppendText("\nABID: " + ABID + " Project: " + str(PID)+"\n")
                    print(rowValue)
                    cur.insertRow(rowValue)
                    self.bxOutput.AppendText("Inserted Node\n")
                    print("Inserted Node")
            edit.stopEditing(True)
        except Exception as e:
            print(e.message)
        finally:
            f.close()


if __name__ == '__main__':
    app=wx.App()
    frame = frmCheckSubmital(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
