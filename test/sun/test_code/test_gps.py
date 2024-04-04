import asyncio
from mavsdk import System


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Start the task
    await print_position(drone)


async def print_position(drone):
    position = drone.telemetry.position()
    print(f"Latitude: {position.latitude_deg}, Longitude: {position.longitude_deg}, Altitude: {position.absolute_altitude_m}")


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())
