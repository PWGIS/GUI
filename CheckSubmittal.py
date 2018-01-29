# This is my own work, with assistance from the wxGlade GUI wireframe composer
# ------------------------------------------------------------------------------
# Updates 1/26/2018: Created a method that populates a txtCtrl with the fileDialog file path and file name
# ------------------------------------------------------------------------------

import wx


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
        self.bxOutput = wx.Panel(self, wx.ID_ANY)
        self.cbxDraw = wx.CheckBox(self, wx.ID_ANY, "Draw")
        self.btnClear = wx.Button(self, wx.ID_ANY, "Clear")
        self.btnZoom = wx.Button(self, wx.ID_ANY, "Zoom")
        self.btnRun = wx.Button(self, wx.ID_ANY, "Run", style=wx.BU_EXACTFIT)

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


if __name__ == '__main__':
    app=wx.App()
    frame = frmCheckSubmital(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
