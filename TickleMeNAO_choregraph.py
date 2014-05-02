mtmd = None
mt = None

class MyClass(GeneratedClass):
	def __init__(self):
		GeneratedClass.__init__(self)
		global mtmd
		global mt
	
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
		self.log(dir(mtmd))
		self.log(dir(mt))

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
		pythonbridge.evalFull("import Markov_tickles_motion_data as mtmd")
		pythonbridge.evalFull("import Markov_tickles.MarkovTickleModule as mt")
		pythonbridge.evalFull("import jill as bob")
		self.log("imports completed")