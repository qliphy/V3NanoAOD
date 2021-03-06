from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName   = 'VVV_MiniAOD_v1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
#config.JobType.generator = 'lhe'
#config.JobType.inputFiles = ['LOWVA.lhe']
# Name of the CMSSW configuration file
config.JobType.psetName    = 'B2G-RunIISummer16MiniAODv3-00005_1_cfg.py'
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 2500

config.section_("Data")
# This string determines the primary dataset of the newly-produced outputs.
# For instance, this dataset will be named /CrabTestSingleMu/something/USER
config.Data.inputDataset = '/VVV-3000-R008/qili-crab_VVV_DR2_v1-f7b11725a86c799f51ca60747917325e/USER'
#config.Data.primaryDataset = 'Bulk'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.publication = True

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_CH_CERN'
