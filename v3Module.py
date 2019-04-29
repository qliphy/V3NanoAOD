import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class v3Producer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i");
        self.out.branch("lumi",  "i");
        self.out.branch("event",  "l");
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
        self.out.branch("npvs","I")
        self.out.branch("lepton_pdg_id",  "I");
        self.out.branch("lepton_pt",  "F");
        self.out.branch("lepton_phi",  "F");
        self.out.branch("lepton_eta",  "F");
        self.out.branch("met",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("njets","I")
        self.out.branch("nfatjets","I")
        self.out.branch("fatjet0_pt",  "F");
        self.out.branch("fatjet0_deepw",  "F");
        self.out.branch("fatjet0_deeph",  "F");
        self.out.branch("gen_weight",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #do this first for processing speed-up
        if not (event.HLT_Ele27_WPTight_Gsf or event.HLT_IsoMu24):
            return False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        photons = Collection(event, "Photon")
        if hasattr(event,'nGenPart'):
            genparts = Collection(event, "GenPart")
        if hasattr(event,'nLHEPart'):    
            lheparts = Collection(event, "LHEPart")
            
        debug = False
        lower_pt_muons = []
        tight_muons = []
        loose_but_not_tight_muons = []
        lower_pt_electrons = []
        tight_electrons = []
        loose_but_not_tight_electrons = []
        fat_jets = []

        for i in range(0,len(muons)):
            if muons[i].pt > 20 and abs(muons[i].eta) < 2.4:
                if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                    tight_muons.append(i)
                elif muons[i].pfRelIso04_all < 0.25:
                    loose_but_not_tight_muons.append(i)
            elif muons[i].pt > 10 and abs(muons[i].eta) < 2.4:
                if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                    lower_pt_muons.append(i)
                elif muons[i].pfRelIso04_all < 0.25:
                    lower_pt_muons.append(i)

        #for processing speed-up
        if len(tight_muons) + len(loose_but_not_tight_muons) > 1:
            return False

        for i in range (0,len(electrons)):
            if electrons[i].pt > 20 and abs(electrons[i].eta + electrons[i].deltaEtaSC) < 2.5:
                if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                    if electrons[i].cutBased >= 3:
                        tight_electrons.append(i)
                    elif electrons[i].cutBased >= 1:
                        loose_but_not_tight_electrons.append(i)
            elif electrons[i].pt > 10 and abs(electrons[i].eta + electrons[i].deltaEtaSC) < 2.5:
                if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                    if electrons[i].cutBased >= 3:
                        lower_pt_electrons.append(i)
                    elif electrons[i].cutBased >= 1:
                        lower_pt_electrons.append(i)

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False



        njets = 0
        for i in range(0,len(jets)):
            if jets[i].pt < 40:
                continue
            if abs(jets[i].eta) > 4.7:
                continue
#            if not jets[i].jetId & (1 << 0):
#                continue
            pass_lepton_dr_cut = True
            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            njets+=1


        nfatjets = 0
        for i in range(0,len(fatjets)):
            if fatjets[i].pt < 200:
                continue
            if abs(fatjets[i].eta) > 4.7:
                continue
#            if not fatjets[i].jetId & (1 << 0):
#                continue
            pass_lepton_dr_cut = True
            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,fatjets[i].eta,fatjets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,fatjets[i].eta,fatjets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            fat_jets.append(i)
            nfatjets+=1

        fatjet0_pt=-1.
        fatjet0_deepw=-1.
        fatjet0_deeph=-1.
        if nfatjets > 0 :
            fatjet0_pt=fatjets[fat_jets[0]].pt
            fatjet0_deepw=fatjets[fat_jets[0]].deepTagMD_WvsQCD
            fatjet0_deeph=fatjets[fat_jets[0]].deepTagMD_H4qvsQCD           

        
        if len(tight_muons) == 1:
            if not (event.HLT_IsoMu24):
                return False
            if muons[tight_muons[0]].pt < 25:
                return False
            if abs(muons[tight_muons[0]].eta) > 2.4:
                return False
            if muons[tight_muons[0]].pfRelIso04_all > 0.15:
                return False
            if not muons[tight_muons[0]].tightId:
                return False
            if debug:
                print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("lepton_pdg_id",13)
            self.out.fillBranch("lepton_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton_phi",muons[tight_muons[0]].phi)
        elif len(tight_electrons) == 1:
            if not event.HLT_Ele27_WPTight_Gsf:
                return False
            if electrons[tight_electrons[0]].cutBased == 0 or electrons[tight_electrons[0]].cutBased == 1:
                return False
            if electrons[tight_electrons[0]].pt < 30:
                return False
            if abs(electrons[tight_electrons[0]].eta) > 2.5:
                return False
            if debug:
                print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)
            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("lepton_pdg_id",11)
            self.out.fillBranch("lepton_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton_phi",electrons[tight_electrons[0]].phi)
        else:
            return False

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:    
            self.out.fillBranch("gen_weight",0)
        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        self.out.fillBranch("njets",njets)
        self.out.fillBranch("nfatjets",nfatjets)
        self.out.fillBranch("fatjet0_pt",fatjet0_pt)
        self.out.fillBranch("fatjet0_deepw",fatjet0_deepw)
        self.out.fillBranch("fatjet0_deeph",fatjet0_deeph)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
        self.out.fillBranch("met",event.MET_pt)

        return True

v3Module = lambda : v3Producer()
