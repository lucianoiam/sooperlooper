#! /usr/bin/env python2
import test_engine
import unittest
import time

class TwoWayDict(dict):
    def __len__(self):
        return dict.__len__(self) / 2

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

class Engine (test_engine.TestEngine):
    def __init__(self, name):
        self.commands = (
                 "UNDO"
                ,"REDO" 
                ,"REPLACE" 
                ,"REVERSE" 
                ,"SCRATCH" 
                ,"RECORD" 
                ,"OVERDUB" 
                ,"MULTIPLY" 
                ,"INSERT" 
                ,"MUTE"
                ,"DELAY"
                ,"REDO_TOG"
                ,"QUANT_TOG"
                ,"ROUND_TOG"
                ,"ONESHOT"
                ,"TRIGGER"
                ,"SUBSTITUTE"
                ,"UNDO_ALL"
                ,"REDO_ALL"
                ,"MUTE_ON"
                ,"MUTE_OFF"
                ,"PAUSE"
                ,"PAUSE_ON"
                ,"PAUSE_OFF"
                )

        self.states = TwoWayDict() 
        for member in test_engine.__dict__.iteritems():
            if "LooperState" in member[0]:
                self.states[member[1]] = member[0][11:]

        self.auto_states = [ self.states["Unknown"]
                           , self.states["WaitStart"] 
                           , self.states["WaitStop"] 
                           , self.states["TriggerPlay"]
                           , self.states["OneShot"]
                           , self.states["Undo"]
                           , self.states["UndoAll"]
                           , self.states["Redo"]
                           , self.states["RedoAll"]
                           ]

        #self.commands_per_state = {}
        #for key in self.states:
        #    if type(key) == int:
        #        self.commands_per_state[key] = [x for x in range(len(self.commands))]

        test_engine.TestEngine.__init__(self, name)

    def request(self, command):
          #print "   requesting: ", self.commands[command]
          command_no = self.commands.index(command)
          self.looper.request_cmd(command_no)
          while (self.looper.request_pending):
              pass
    def getState(self):
        return self.looper.get_control_value(test_engine.State)
        

class stateTests(unittest.TestCase):
    def setUp(self):
        self.engine = Engine("SL_test")

    def tearDown(self):
        del self.engine

    def assertState(self, state):
        self.assertEqual(self.engine.getState(), self.engine.states[state])


    def testOff(self):
        self.assertState("Off")

    def testRecord(self):
        self.engine.request("RECORD")
        self.assertState("Recording")

    def testRecord2(self):
        self.engine.request("RECORD")
        self.engine.request("RECORD")
        self.assertState("Playing")

    def testOverdub(self):
        self.engine.request("RECORD")
        self.engine.request("RECORD")
        self.engine.request("OVERDUB")
        self.assertState("Overdubbing")


def main():
    unittest.main()

if __name__ == '__main__':
    main()
