import time

MarkovTickle = None

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

        # Autonomous Life needs to be
        self.autonomousLife = ALProxy('ALAutonomousLife')

        self.log(self.autonomousLife.getState())

    def onLoad(self):
        #~ puts code for box initialization here
        pass

    def onUnload(self):
        #~ puts code for box cleanup here
        self.log(" ----------------- unload ------------- ")
        global MarkovTickle
        MarkovTickle.exit()
        MarkovTickle = None


    def onInput_onStart(self, p):
        global MarkovTickle

        self.do_imports()

        id = self.autonomousLife.post.setState("disabled")
        self.autonomousLife.wait(id, 0)

        if not MarkovTickle in globals():
            MarkovTickle = None


        MarkovTickle = mt.MarkovTickleModule("MarkovTickle")

        MarkovTickle.mainTask()

        while True:
            self.log("alive!")
            time.sleep(1)



        self.onStopped()

    def onInput_onStop(self):
        self.log(" ----------------- stop ------------- ")
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box



    def do_imports(self):
        """ Import external Python.

        """
        ext_path = ALFrameManager.getBehaviorPath(self.behaviorId)
        self.log("Importing external python at "+ext_path)
        pythonbridge = ALProxy("ALPythonBridge")
        pythonbridge.evalFull("import sys; sys.path.append('" + ext_path + "')")
        pythonbridge.evalFull("import Markov_tickles_motion_data as mtmd")
        pythonbridge.evalFull("import Markov_tickles as mt")
        self.log("imports completed")