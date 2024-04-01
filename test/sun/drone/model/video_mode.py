class VideoModel():
    def __init__(self) -> None:
        self.frame=None
        
    def set_frame(self,data):
        self.frame=data
    def get_frame(self):
        if(self.frame==None):
            self.frame="no"
        return self.frame   