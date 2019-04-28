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

p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/WkkToWRadionToWWW_M3000-R0-08_TuneCP5_13TeV-madgraph/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/10000/3D80B581-DCBF-E94B-AF09-AA58C00AC90B.root"],None,"v3_keep_and_drop.txt",[countHistogramsModule(),v3Module()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "v3_output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")



