#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from  v3Module import *

from countHistogramsModule import *

#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/1EA786F7-D312-E811-9ED3-001E67460991.root"],"event == 2303072","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",inputFiles(),None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/WW_TuneCUETP8M1_13TeV-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/40000/83C07235-3B39-F149-91A7-3729E29794A9.root"],None,"v3_keep_and_drop.txt",[countHistogramsModule(),v3Module()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "v3_output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")



