from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName   = 'VVV-3000-R008'
#config.General.saveLogs = True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'PrivateMC'
config.JobType.inputFiles = ['/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/Triboson/Triboson_M3000_R0.08_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz']
config.JobType.psetName    = 'B2G-RunIISummer15wmLHEGS-01617_1_cfg.py'


config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 400
config.Data.totalUnits = 40000
config.Data.publication = True
config.Data.outputPrimaryDataset = 'VVV-3000-R008'

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_CH_CERN'
