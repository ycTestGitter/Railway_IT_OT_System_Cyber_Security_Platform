#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import wx
import metroEmuGobal as gv
import railwayAgent as agent

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapMgr(object):
    """ Map manager to init/control differet elements state on the map."""
    def __init__(self, parent):
        """ Init all the elements on the map. All the parameters are public to 
            other module.
        """
        self.tracks = {}
        self.trains = {}
        self.sensors = {}
        self.signals = {}
        self.stations = {}
        self.envItems = [] # Currently we only have building item so use list instead of dict()

        self._initTandT()
        self._initSensors()
        self._initSignal()
        self._initStation()
        self._initEnv()

        gv.gDebugPrint('Map display management controller inited', logType=gv.LOG_INFO)

#-----------------------------------------------------------------------------
    def _initTandT(self):
        """ This is a private Train&Tracks data init function, currently the data 
            is hardcoded. It will be replaced by loading a config file before the 
            whole program init.(load to a gv.gxx parameter)
        """
        # Init WE-Line and the trains on it.
        key = 'weline'
        self.tracks[key] = {
            'name': key,
            'color': gv.gTrackConfig[key]['color'],
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(50, 200), (100, 200), (100, 600), (600, 600), (600, 800),
                       (900, 800), (900, 400), (1550, 400), (1550, 450), (950, 450),
                       (950, 850), (550, 850), (550, 650), (50, 650)]
        }
        trackTrainCfg_we = [{'id': 'we01', 'head': (50, 200), 'nextPtIdx': 1, 'len': 5}, 
                            {'id': 'we02', 'head': (1500, 400),'nextPtIdx': 7, 'len': 5},
                            {'id': 'we03', 'head': (460, 600), 'nextPtIdx': 3, 'len': 5},
                            {'id': 'we03', 'head': (800, 850), 'nextPtIdx': 11, 'len': 5}]
        self.trains[key] = self._getTrainsList(trackTrainCfg_we, self.tracks[key]['points'])
        # Init NS-Line and the trains on it.
        key = 'nsline'
        self.tracks[key] = {
            'name' : key,
            'color': gv.gTrackConfig[key]['color'],
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(300, 50), (1200, 50), (1200, 300), (800, 300), (800, 600), (700, 600), 
                       (700, 100), (400, 100), (400, 450), (300, 450)]
        }
        trackTrainCfg_ns = [{'id': 'ns01', 'head': (400, 50), 'nextPtIdx': 1, 'len': 4},
                            {'id': 'ns02', 'head': (1100, 300), 'nextPtIdx': 3, 'len': 4},
                            {'id': 'ns03', 'head': (600, 100), 'nextPtIdx': 7, 'len': 4}]

        self.trains[key] = self._getTrainsList(trackTrainCfg_ns, self.tracks[key]['points'])
        # Init CC-Line and the trains on it.
        key = 'ccline'
        self.tracks[key] = {
            'name' : key,
            'color': gv.gTrackConfig[key]['color'],
            'type': gv.RAILWAY_TYPE_CYCLE,
            'points': [(200, 200), (1400, 200), (1400, 700), (200, 700)]
        }
        trackTrainCfg_cc = [  {'id': 'cc01', 'head': (800, 200), 'nextPtIdx': 1, 'len': 6},
                            {'id': 'cc02', 'head': (300, 700), 'nextPtIdx': 3, 'len': 6},
                            {'id': 'cc03', 'head': (1300, 700), 'nextPtIdx': 3, 'len': 6}]
        self.trains['ccline'] = self._getTrainsList(trackTrainCfg_cc, self.tracks[key]['points'])

#-----------------------------------------------------------------------------
    def _initSensors(self):
        """ Init all the train detection sensors on the map. """
        # Init all the WE-Line sensors
        sensorPos_we= [
            (50, 200), (170, 600), (270, 600), (600, 670), (600, 770), (900, 730),
            (900, 630), (1370, 400), (1470, 400), (1430, 450), (1330, 450), 
            (950, 670), (950, 770), (550, 730), (550, 650), (230, 650), (130, 650)
            ]
        self.sensors['weline'] = agent.AgentSensors(self, 'we', sensorPos_we)
        # Init all the NS-line sensors
        sensorPos_ns = [
            (300, 230), (300, 130), (1200, 170), (1200, 270), (700, 230), (700, 130),
            (400, 170), (400, 270)
            ]
        self.sensors['nsline'] = agent.AgentSensors(self, 'ns', sensorPos_ns)
        # Init all the CC-Line sensors.
        sensorPos_cc = [
            (270, 200), (480, 200), (670, 200), (770, 200), 
            (1170, 200), (1270, 200), (1400, 370), (1400, 500), 
            (980, 700), (830, 700), (630, 700), (460, 700),
            (200, 700), (200, 530)
            ]
        self.sensors['ccline'] = agent.AgentSensors(self, 'cc', sensorPos_cc)

#-----------------------------------------------------------------------------
    def _initSignal(self):
        # Set all the signal on track weline
        trackSignalConfig_we = [
            {'id': 'we-0', 'pos':(160, 600), 'dir': gv.LAY_U, 'tiggerS': self.sensors['ccline'], 'onIdx':(13,), 'offIdx':(12,) }, 
            {'id': 'we-1', 'pos':(240, 650), 'dir': gv.LAY_U, 'tiggerS': self.sensors['ccline'], 'onIdx':(13,), 'offIdx':(12,) },
            {'id': 'we-3', 'pos':(600, 660), 'dir': gv.LAY_R, 'tiggerS': self.sensors['ccline'], 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-4', 'pos':(550, 740), 'dir': gv.LAY_L, 'tiggerS': self.sensors['ccline'], 'onIdx':(11,), 'offIdx':(10,) },
            {'id': 'we-5', 'pos':(900, 740), 'dir': gv.LAY_L, 'tiggerS': self.sensors['ccline'], 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-6', 'pos':(950, 660), 'dir': gv.LAY_R, 'tiggerS': self.sensors['ccline'], 'onIdx':(9,), 'offIdx':(8,) },
            {'id': 'we-7', 'pos':(1360, 400), 'dir': gv.LAY_U, 'tiggerS': self.sensors['ccline'], 'onIdx':(7,), 'offIdx':(6,) },
            {'id': 'we-8', 'pos':(1440, 450), 'dir': gv.LAY_U, 'tiggerS': self.sensors['ccline'], 'onIdx':(7,), 'offIdx':(6,) },
        ]
        self.signals['weline'] = []
        for info in trackSignalConfig_we:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.signals['weline'].append(signal)
        
        # Set all the signal on track nsline
        trackSignalConfig_ns = [
            {'id': 'ns-0', 'pos':(300, 240), 'dir': gv.LAY_L, 'tiggerS': self.sensors['ccline'], 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-2', 'pos':(400, 160), 'dir': gv.LAY_R, 'tiggerS': self.sensors['ccline'], 'onIdx':(1,), 'offIdx':(0,) },
            {'id': 'ns-3', 'pos':(700, 240), 'dir': gv.LAY_R, 'tiggerS': self.sensors['ccline'], 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'ns-4', 'pos':(1200, 160), 'dir': gv.LAY_R, 'tiggerS': self.sensors['ccline'], 'onIdx':(5,), 'offIdx':(4,) },
        ]
        self.signals['nsline'] = []
        for info in trackSignalConfig_ns:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.signals['nsline'] .append(signal)

        # set all the signal on track cline
        trackSignalConfig_cc = [
            {'id': 'cc-0', 'pos':(260, 200), 'dir': gv.LAY_U, 'tiggerS': self.sensors['nsline'], 'onIdx':(1, 7), 'offIdx':(0, 2) },
            {'id': 'cc-1', 'pos':(660, 200), 'dir': gv.LAY_U, 'tiggerS': self.sensors['nsline'], 'onIdx':(5,), 'offIdx':(4,) },
            {'id': 'cc-2', 'pos':(1160, 200), 'dir': gv.LAY_U, 'tiggerS': self.sensors['nsline'], 'onIdx':(3,), 'offIdx':(2,) },
            {'id': 'cc-3', 'pos':(1400, 360), 'dir': gv.LAY_R, 'tiggerS': self.sensors['weline'], 'onIdx':(8,10), 'offIdx':(7,9) },
            {'id': 'cc-4', 'pos':(990, 700), 'dir': gv.LAY_U, 'tiggerS': self.sensors['weline'], 'onIdx':(6,12), 'offIdx':(5,11) },
            {'id': 'cc-5', 'pos':(640, 700), 'dir': gv.LAY_U, 'tiggerS': self.sensors['weline'], 'onIdx':(4,14), 'offIdx':(3,13) },
            {'id': 'cc-6', 'pos':(210, 700), 'dir': gv.LAY_U, 'tiggerS': self.sensors['weline'], 'onIdx':(2, 16), 'offIdx':(1,15) },
        ]
        self.signals['ccline'] = []
        for info in trackSignalConfig_cc:
            signal = agent.AgentSignal(self, info['id'], info['pos'], dir=info['dir'])
            signal.setTriggerOnSensors(info['tiggerS'], info['onIdx'])
            signal.setTriggerOffSensors(info['tiggerS'], info['offIdx'])
            self.signals['ccline'].append(signal)

#-----------------------------------------------------------------------------
    def _initStation(self):
        """ Init all the train stations. """
        # Init all stations on weline.
        trackStation_we = [{'id': 'Tuas_Link', 'pos': (80, 200)},
                           {'id': 'Junrong_East', 'pos': (360, 600)},
                           {'id': 'Outram_Park', 'pos': (750, 800)},
                           {'id': 'City_Hall', 'pos': (900, 500)},
                           {'id': 'Paya_Leba', 'pos': (1250, 400)},
                           {'id': 'Changgi_Airport', 'pos': (1550, 450)},
                           {'id': 'Lavender', 'pos': (1100, 450)},
                           {'id': 'Raffles_Place', 'pos': (850, 850)},
                           {'id': 'Cliementi', 'pos': (430, 650)},
                           {'id': 'Boon_Lay', 'pos': (50, 450)}]
        self.stations['weline'] = []
        for info in trackStation_we:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trains['weline'])
            self.stations['weline'].append(station)
        
        # Init all stations on nsline
        trackStation_ns = [{'id': 'Junrong_East', 'pos': (360, 450)},
                           {'id': 'Wood_Land', 'pos': (430, 50)},
                           {'id': 'Yishun', 'pos': (1040, 50)},
                           {'id': 'Orchard', 'pos': (980, 300)},
                           {'id': 'City_Hall', 'pos': (750, 600)},
                           {'id': 'BiShan', 'pos': (550, 100)}]
        self.stations['nsline'] = []
        for info in trackStation_ns:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trains['nsline'])
            self.stations['nsline'].append(station)

        # Init all stations on ccline
        trackStation_cc = [{'id': 'Buona_Vsta', 'pos': (320, 700)},
                           {'id': 'Farrer_Road', 'pos': (200, 300)},
                           {'id': 'Serangoon', 'pos': (930, 200)},
                           {'id': 'Nicoll _ighway', 'pos': (1400, 600)},
                           {'id': 'Bayfront', 'pos': (1160, 700)},
                           {'id': 'HarbourFront', 'pos': (710, 700)}]
        self.stations['ccline'] = []
        for info in trackStation_cc:
            station = agent.AgentStation(self, info['id'], info['pos'])
            station.bindTrains(self.trains['ccline'])
            self.stations['ccline'].append(station)


#-----------------------------------------------------------------------------
    def _initEnv(self):
        """ Init all the enviroment Items on the map such as IOT device or camera."""
        envCfg = [ {'id':'Tuas Industry Area', 'img':'factory_0.png', 'pos':(80, 80) ,  'size':(120, 120)},
                   {'id':'Changgi Airport', 'img':'airport.jpg', 'pos':(1500, 240) ,  'size':(160, 100)},
                   {'id':'JurongEast-Jem', 'img':'city_0.png', 'pos':(360, 520) ,  'size':(80, 80)},
                   {'id':'CityHall-01', 'img':'city_2.png', 'pos':(750, 520) ,  'size':(90, 80)},
                   {'id':'CityHall-02', 'img':'city_1.png', 'pos':(850, 500) ,  'size':(80, 60)}]
        for info in envCfg:
            imgPath = os.path.join(gv.IMG_FD, info['img'])
            if os.path.exists(imgPath):
                bitmap = wx.Bitmap(imgPath)
                building = agent.agentEnv(self, info['id'], info['pos'], bitmap, info['size'] )
                self.envItems.append(building)

#-----------------------------------------------------------------------------
    def _getTrainsList(self, trainCfg, trackPts):
        """ Build the railwayAgent.TainAgent obj list based on inmput train config information.
        Args:
            trainCfg (_type_): _description_
            trackPts (_type_): _description_
        Returns:
            _type_: _description_
        """
        trainList = []
        for trainInfo in trainCfg:
            trainObj = agent.AgentTrain(self, trainInfo['id'], trainInfo['head'], trackPts, trainLen=trainInfo['len'])
            trainList.append(trainObj)
        return trainList

#-----------------------------------------------------------------------------
# Define all the get() functions here:

    def getEnvItems(self):
        return self.envItems

    def getTracks(self, trackID=None):
        if trackID and trackID in self.tracks.keys(): return self.tracks[trackID]
        return self.tracks

    def getTrains(self, trackID=None):
        if trackID and trackID in self.trains.keys(): return self.trains[trackID]
        return self.trains

    def getSignals(self, trackID=None):
        if trackID and trackID in self.signals.keys(): return self.signals[trackID]
        return self.signals

    def getSensors(self, trackID=None):
        if trackID and trackID in self.sensors.keys(): return self.sensors[trackID]
        return self.sensors
    
    def selfStations(self, trackID=None):
        if trackID and trackID in self.stations.keys(): return self.stations[trackID]
        return self.stations

#-----------------------------------------------------------------------------
    def periodic(self , now):
        """ Periodicly call back function. This function need to be called before the 
            railwayPanelMap's periodic().
        """
        # update the trains position.
        for key, val in self.trains.items():
            frontTrain = val[-1]
            for train in val:
                # Check the signal 1st 
                train.checkSignal(self.signals[key])
                train.checkCollFt(frontTrain)
                train.updateTrainPos()
                frontTrain = train                
            # update all the track's sensors state afte all the trains have moved.
            self.sensors[key].updateActive(val)
        
        # update the station train's docking state
        for key, val in self.stations.items():
            for station in val:
                station.updateTrainSDock()

        # Update the signal state
        for key, val in self.signals.items():
            for signal in val:
                signal.updateSingalState()