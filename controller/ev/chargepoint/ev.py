# Copyright 2020 program was created VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

import constants
import os
import time


def get_ENV_val(str):
    if (str in os.environ):
        return os.environ[str]
    else:
        errMsg = "Missing environment variable: " + str
        raise EVException(errMsg, constants.ERR_ENV_VAR_MISSING)


class EVException(Exception):
    err_code = None
    def __init__(self, message, code):

        # Call the base class constructor with the parameters it needs
        super(EVException, self).__init__(message)

        # Now for your custom code...
        self.err_code = code


# A Charge Session has a start time and only when complete an end time.
# Trickle is when the charging rate drops, vehicle specific
class ChargeSession():
    vehicleID = None
    start = None
    trickle = None
    end = None
    amount = None
    trickle_amount = None
    totalCharge = None
    fullChargeRate = None
    trickleChargeRate = None
    portID = None

    def __init__(self, vehicleID, portID, amount):
        self.vehicleID = vehicleID
        self.portID = portID
        self.start = time.time()
        self.amount = amount
        self.totalCharge = 0


class ChargePort():
    portID = None
    shedState = False
    shedTime = None
    amount = None
    percentage = None

    def __init__(self, portID):
        self.portID = portID

    def shed(self, amount=None, percent=None):
        if (amount is not None):
            self.amount = amount
        else:
            if (percent is not None):
                self.percent = percent
            else:
                raise EVException("Specify either amount or percent",
                                  constants.ERR_INVALID_VALUE)
        self.shedTime = time.time()
        self.shedState = True

    def clear(self):
        self.shedState = False
        self.amount = None
        self.percent = None


class ChargePoint():
    sgID = None
    stationID = None
    portID = None
    ID = None

    def __init__(self, sgID, stationID, portID):
        self.ID = ChargePoint.buildID(sgID, stationID, portID)
        self.sgID = sgID
        self.stationID = stationID
        self.portID = portID

    @staticmethod
    def fromID(IDstr):
        if ((IDstr is None) or (IDstr == "")):
            print("Invalid input provided to ChargePoint constructor")
            raise EVException("IDstr cannot be empty or None",
                              constants.ERR_INVALID_VALUE)
        IDlist = IDstr.split(constants.SEPARATOR)
        sgID = None
        stationID = None
        portID = None

        if constants.DEBUG:
            print(IDlist)
        if (len(IDlist) == 1):
            sgID = IDlist[0]
        else:  # len(IDlist) will be 3
            if (IDlist[0] != ""):
                sgID = IDlist[0]
            if (IDlist[1] != ""):
                stationID = IDlist[1]
            if (IDlist[2] != ""):
                portID = IDlist[2]
        if constants.DEBUG:
            print("id = " + IDstr + ", ")
            print("sgID = " + str(sgID) + ", ")
            print("stationID = " + str(stationID) + ", ")
            print("portID = " + str(portID) + "\n")
        return ChargePoint(sgID, stationID, portID)

    @staticmethod
    def buildID(sgID, stationID, portID):
        IDstr = ""
        sep = constants.SEPARATOR
        if ((sgID is None) and (stationID is None)):
            raise EVException("Specify at least Station Group or Station ID",
                              constants.ERR_INVALID_VALUE)
        if (sgID is not None):
            IDstr += str(sgID)
        if (stationID is not None):
            IDstr = IDstr + sep + stationID + sep
        if (portID is not None):
            IDstr += portID
        return IDstr


class ChargeSessions:
    sessions = None

    def __init__(self):
        self.sessions = {}

    def get_start(self, vehicleID, watt, now):
        start = now
        if (vehicleID in self.sessions.keys()):
            start = self.sessions[vehicleID]
            if (watt == 0):
                # charge session over
                del self.sessions[vehicleID]
        else:
            self.sessions[vehicleID] = start
        return start
