#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from v3Module import *
from countHistogramsModule import *
#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

nevents = 40000
preselection="(nElectron + nMuon) > 1"

#---local------------------------
files=['1.root']
#files=['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/WW_TuneCUETP8M1_13TeV-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/40000/EA8C5F9E-A1F8-2245-AC4D-6CD8440DFB5B.root']
#p=PostProcessor(".",files,preselection,"v3_keep_and_drop.txt",[countHistogramsModule(),v3Module()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "v3_output_branch_selection.txt", maxEntries=nevents)

#---crab--------------------------
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
p=PostProcessor(".",inputFiles(),preselection,"v3_keep_and_drop.txt",[countHistogramsModule(),v3Module()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "v3_output_branch_selection.txt")


#p=PostProcessor(".",inputFiles(),"event == 200","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

p.run()

print "DONE"
os.system("ls -lR")



