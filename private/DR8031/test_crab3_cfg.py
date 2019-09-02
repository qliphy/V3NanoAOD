from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName   = 'VVV_DR2_v1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
#config.JobType.generator = 'lhe'
#config.JobType.inputFiles = ['LOWVA.lhe']
# Name of the CMSSW configuration file
config.JobType.psetName    = 'B2G-RunIISummer16DR80Premix-02574_2_cfg.py'
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 2500

config.section_("Data")
# This string determines the primary dataset of the newly-produced outputs.
# For instance, this dataset will be named /CrabTestSingleMu/something/USER
config.Data.inputDataset = '/VVV-3000-R008/qili-crab_VVV_DR_v5-b1c0e8cfd394092a8ffef7662900ef17/USER'
#config.Data.primaryDataset = 'Bulk'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.publication = True

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_CH_CERN'
