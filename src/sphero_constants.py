DeviceID = {"apiProcessor": 16,
            "systemInfo": 17,
            "powerInfo": 19,
            "driving": 22,
            "sensor": 24,
            "userIO": 26,
            }

SendPacketConstants = {"StartOfPacket": 141,
                       "EndOfPacket": 216,
                       "ESC": 171}

UserIOCommandIDs = {"allLEDs": 28,
                    "matrixColor": 47,
                    "matrixPix": 45,
                    "printChar": 66}

SensorCommandIds = {"calibrateToNorth": 37,
                    "startIRBroadcast": 0x27,
                    "startIRFollow": 0x28,
                    "stopIRBroadcast": 0x29,
                    "stopIRFollow": 0x32,
                    "startStreamingService": 0x3A,
                    "stopStreamingService": 0x3B,
                    "clearStreamingService": 0x3C,
                    "streamingServiceDataNotify": 0x3D,
                    }

PowerCommandIDs = {"wake": 13}

DrivingCommands = {"driveWithHeading": 7,
                   "resetYaw": 6}

Flags = {
    "isResponse": 1,
    "requestsResponse": 2,
    "requestsOnlyErrorResponse": 4,
    "resetsInactivityTimeout": 8,
    "commandHasTargetId": 16,
    "commandHasSourceId": 32
}
