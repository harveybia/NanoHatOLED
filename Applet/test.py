class SHPageView:
    pageUDID = 0
    def __init__(self):
        self.udid = SHPageView.pageUDID
        SHPageView.pageUDID += 1

    def getImage(self):
        return pageUDID

    def getUDID(self):
        # UDID used as page number, ranging from [0, n)
        return self.udid
