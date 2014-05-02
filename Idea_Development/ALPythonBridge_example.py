class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
    def onLoad(self):
        #~ puts code for box initialization here
        pass

    def onUnload(self):
        #~ puts code for box cleanup here 
        pass

    def onInput_onStart(self, p):
        # here I do my imports
        self.do_imports()
        # now I can make use of the imported code here and in other boxes
        env = wanderer.make_wanderer_environment(self)
        pos = env.motion.getPosition("Head", 1, True)
        wanderer.init_state(env, pos)
        self.onStopped()

   def onInput_onStop(self):
        self.onUnload() #~ it is recommanded to call onUnload of this box in a onStop method, as the code written in onUnload is used to stop the box as well
    '''
    Import the external python now so we don't have to separately import it in
    every choreographe box that uses one of the external modules. Doing it this
    way also ensures that if paths change only this box needs to be updated.
    '''
    def do_imports(self):
        ext_path = ALFrameManager.getBehaviorPath(self.behaviorId)+"/src/main/python"
        self.log("Importing external python at "+ext_path)
        pythonbridge = ALProxy("ALPythonBridge")
        pythonbridge.evalFull("import sys; sys.path.append('" + ext_path + "')")
        pythonbridge.evalFull("import naoutil.naoenv as naoenv")
        pythonbridge.evalFull("import naoutil.i18n as i18n")
        pythonbridge.evalFull("import naoutil.jprops as jprops")
        pythonbridge.evalFull("import naoutil.general as general")
        pythonbridge.evalFull("from naoutil.jsonobj import to_json_string, from_json_string")
        pythonbridge.evalFull("import wanderer.action as action")
        pythonbridge.evalFull("import wanderer.event as event")
        pythonbridge.evalFull("import wanderer.robotstate as robotstate")
        pythonbridge.evalFull("import wanderer.http as http")
        pythonbridge.evalFull("import wanderer.wanderer as wanderer")
        pythonbridge.evalFull("from wanderer.randomwalk import RandomWalk")
        self.log("imports completed")