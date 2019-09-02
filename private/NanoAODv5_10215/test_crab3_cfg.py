from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName   = 'VVV_NanoAOD_v3'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
#config.JobType.generator = 'lhe'
#config.JobType.inputFiles = ['LOWVA.lhe']
# Name of the CMSSW configuration file
config.JobType.psetName    = 'B2G-RunIISummer16NanoAODv5-00001_1_cfg.py'
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 2500

config.section_("Data")
# This string determines the primary dataset of the newly-produced outputs.
# For instance, this dataset will be named /CrabTestSingleMu/something/USER
config.Data.inputDataset = '/VVV-3000-R008/qili-crab_VVV_MiniAOD_v1-bd3e7bcff6c9bcad356ea4ed7e4f08b4/USER'
#config.Data.primaryDataset = 'Bulk'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.publication = True

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_CH_CERN'
