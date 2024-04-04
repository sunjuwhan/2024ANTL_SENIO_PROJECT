class GpsModel:
    def __init__(self) -> None:
        self.__latitude_deg=None #위도
        self.__longitude_deg=None #경도
        self.__absolute_altitude=None  
        self.__relative_altitude=None  #실제 높이 
    def set_gps(self,latitude,longitude,absolute,relative):
        self.__latitude_deg=latitude
        self.__longitude_deg=longitude
        self.__absolute_altitude=absolute
        self.__relative_altitude=relative
        
    def get_gps(self):
        return(self.__latitude_deg,self.__longitude_deg,self.__absolute_altitude,self.__relative_altitude)
    
    