from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'Nano_v2'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../PhysicsTools/NanoAODTools/scripts/haddnano.py', '../v3_postproc.py', '../v3Module.py', '../v3_keep_and_drop.txt', '../v3_output_branch_selection.txt', '../countHistogramsModule.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
#config.Data.inputDataset = '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/NANOAODSIM'
#config.Data.inputDBS = 'global'
config.Data.inputDataset = '/VVV-3000-R008/qili-crab_VVV_NanoAOD_v3-f9255f5ef092ed4261a677d1b3d4c5e7/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
#config.Data.outLFNDirBase = '/store/user/%s/NanoPost' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTest_v2'
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

#config.section_("User")
#config.User.voGroup = 'dcms'

