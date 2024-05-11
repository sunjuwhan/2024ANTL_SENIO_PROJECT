
import asyncio
from mavsdk import System

class Drone:
    def __init__(self) -> None:
        self.antl_drone = None
        self.flying_alt=None
    async def make_drone(self):
        self.antl_drone=System()
        print("wating connect drone")
        await self.antl_drone.connect(system_address="serial:///dev/ttyAMA0")
        print("Start connect") 
        #await self.antl_drone.connect(system_address="udp://:14540")
        print("Wating for drone to connect...")  #drone connect 
        async for state in self.antl_drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break
            
        async for health in self.antl_drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position state is good enough for flying.")
                break
        try:
            await self.antl_drone.manual_control.set_manual_control_input
            (float(0), float(0), float(0.5), float(0))
            
            print("good")
            
        except Exception as e:
            print(e)
        print("Fetching amsl altitude at home location....")
        async for terrain_info in self.antl_drone.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            break
        self.flying_alt=absolute_altitude+1.0
        #print("-- Arming")
        #await self.antl_drone.action.arm()
        #await asyncio.sleep(1)
        
        #print("--take off")
        #await self.antl_drone.action.takeoff()
        #await asyncio.sleep(5)

    def get_drone(self):
        return self.antl_drone
class Key:#

    def __init__(self):
        self.__yaw = 0
        self.__throttle = 0
        self.__pitch = 0
        self.__roll = 0
    ##set

    def set_key(self,yaw,throttle,pitch,roll):
        self.__yaw=yaw
        self.__throttle=throttle
        self.__pitch=pitch
        self.__roll=roll

    ##get
    def get_key(self):
        return (self.__yaw,self.__throttle,self.__roll,self.__pitch)


class PilotModel:
    def __init__(self):
        self.__key = Key()
        self.__mode = 0
        self.__drone_state="off"
    def set_mode(self, mode):  
        self.__mode = mode
        return

    def set_data(self, key,mode):
        try:
            self.__key.set_key(
                yaw=float(key[0]), throttle=float(key[1]), 
                pitch=float(key[2]), roll=float(key[3])
                )
            self.__mode=mode
        except:
            print("ERROR :: Bad key request")
            self.__key.set_key(
                yaw=float(0), throttle=float(0.5), 
                pitch=float(0), roll=float(0)
                )
        return 
    def set_drone_state(self,state):
        self.__drone_state=state
    def get_drone_state(self):
        return self.__drone_state
        
    def get_key(self):
        return self.__key.get_key()
    
    def get_mode(self):
        return self.__mode

    def get_data(self):
        return (self.__key,self.__mode)

