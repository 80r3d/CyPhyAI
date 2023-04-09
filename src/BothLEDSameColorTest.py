import asyncio

from random import randrange
from sphero_bolt import SpheroBolt
from bleak import BleakError

async def run(address):
    # mac address of sphero bolt
    global BOLTS, BOLTS_HSV_PREVIEW

    bolt_names = address

    BOLTS = []
    BOLTS_HSV_PREVIEW = {}
    for bolt_name in bolt_names:
        print(f"[!] Connecting with BOLT {bolt_name}")

        bolt = SpheroBolt(bolt_name)
        connect_tries = 0
        tries = 10
        while connect_tries < tries:
            connect_tries += 1
            try:
                error = await bolt.connect()
                break
            except (BleakError, TimeoutError) as e:
                if connect_tries == tries:
                    print(f"[ERROR] : {e}")

            except Exception as e:
                error = str(e)
                if 'HRESULT: 0x800710DF' in error:
                    print('Uw bluetooth staat niet aan', '\n')

                else:
                    raise e

        await bolt.resetYaw()
        await bolt.wake()

        BOLTS.append(bolt)


    for bolt in BOLTS:
        await bolt.roll(100, 0, 2)


if __name__ == "__main__":
    address = ["DC:03:B5:A0:3D:46", "FA:9D:4E:32:C5:4E"]
    add1 = "DC:03:B5:A0:3D:46"
    add2 = "FA:9D:4E:32:C5:4E"
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(address))
    while True:
        toy_number = int(input("Select the sphero to control: "))
        toy = BOLTS[toy_number]
        loop.run_until_complete(toy.roll(100, 0, 2))