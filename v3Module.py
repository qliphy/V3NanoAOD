import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

jetsize=6
fatjetsize=3

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
        self.out.branch("njets","I");
        self.out.branch("jets_pt","F",lenVar="jetsize");   
        self.out.branch("jets_eta","F",lenVar="jetsize");   
        self.out.branch("jets_phi","F",lenVar="jetsize");
        self.out.branch("jets_mass","F",lenVar="jetsize");
        self.out.branch("nfatjets","I");
        self.out.branch("fatjets_pt","F",lenVar="fatjetsize");
        self.out.branch("fatjets_eta","F",lenVar="fatjetsize");
        self.out.branch("fatjets_phi","F",lenVar="fatjetsize");
        self.out.branch("fatjets_mass","F",lenVar="fatjetsize");
        self.out.branch("fatjets_deepw","F",lenVar="fatjetsize");
        self.out.branch("fatjets_deeph","F",lenVar="fatjetsize");
        self.out.branch("gen_weight",  "F");
        self.out.branch("gen_gra_eta",  "F");
        self.out.branch("gen_gra_m",  "F");
        self.out.branch("gen_gra_pt",  "F");
        self.out.branch("gen_gra_phi",  "F");

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
#MC------------------------------------------------------------
        gen_gra_eta=-10.
        gen_gra_m=-10.
        gen_gra_pt=-10.
        gen_gra_phi=-10.          
        if hasattr(event,'nGenPart'):
           for i in range(0,len(genparts)):
              if abs(genparts[i].pdgId) == 9000024:
                gen_gra_eta=genparts[i].eta
                gen_gra_m=genparts[i].mass
                gen_gra_pt=genparts[i].pt
                gen_gra_phi=genparts[i].phi

        self.out.fillBranch("gen_gra_eta",gen_gra_eta)
        self.out.fillBranch("gen_gra_m",gen_gra_m)
        self.out.fillBranch("gen_gra_pt",gen_gra_pt)
        self.out.fillBranch("gen_gra_phi",gen_gra_phi)


#MC------------------------------------------------------------


            
        debug = False
        lower_pt_muons = []
        tight_muons = []
        loose_but_not_tight_muons = []
        lower_pt_electrons = []
        tight_electrons = []
        loose_but_not_tight_electrons = []
        ak4_jets = []
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

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 1:
            return False



        njets = 0
        for i in range(0,len(jets)):
            if jets[i].pt < 40:
                continue
            if abs(jets[i].eta) > 4.7:
                continue
            if not jets[i].jetId & (1 << 0):
                continue
            pass_lepton_dr_cut = True
            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            ak4_jets.append(i)
            njets+=1

        jets_pt=[-10.0,-10.0,-10.0,-10.0,-10.0,-10.0]
        jets_eta=[-10.0,-10.0,-10.0,-10.0,-10.0,-10.0]
        jets_phi=[-10.0,-10.0,-10.0,-10.0,-10.0,-10.0]
        jets_mass=[-10.0,-10.0,-10.0,-10.0,-10.0,-10.0]
        for i in range(0,6):
           if(i<njets) :
              jets_pt[i]=jets[ak4_jets[i]].pt
              jets_eta[i]=jets[ak4_jets[i]].eta
              jets_phi[i]=jets[ak4_jets[i]].phi
              jets_mass[i]=jets[ak4_jets[i]].mass

        nfatjets = 0
        for i in range(0,len(fatjets)):
            if fatjets[i].pt < 200:
                continue
            if abs(fatjets[i].eta) > 4.7:
                continue
            if not fatjets[i].jetId & (1 << 0):
                continue
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

        fatjets_pt=[-10.0,-10.0,-10.0]
        fatjets_eta=[-10.0,-10.0,-10.0]
        fatjets_phi=[-10.0,-10.0,-10.0]
        fatjets_mass=[-10.0,-10.0,-10.0]
        fatjets_deepw=[-10.0,-10.0,-10.0]
        fatjets_deeph=[-10.0,-10.0,-10.0]
        for i in range(0,3):
           if(i<nfatjets) :
             fatjets_pt[i]=fatjets[fat_jets[i]].pt
             fatjets_eta[i]=fatjets[fat_jets[i]].eta
             fatjets_phi[i]=fatjets[fat_jets[i]].phi
             fatjets_mass[i]=fatjets[fat_jets[i]].mass
             fatjets_deepw[i]=fatjets[fat_jets[i]].deepTagMD_WvsQCD
             fatjets_deeph[i]=fatjets[fat_jets[i]].deepTagMD_H4qvsQCD           

        
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
        self.out.fillBranch("jets_pt",jets_pt)
        self.out.fillBranch("jets_eta",jets_eta)
        self.out.fillBranch("jets_phi",jets_phi)
        self.out.fillBranch("jets_mass",jets_mass)
        self.out.fillBranch("nfatjets",nfatjets)
        self.out.fillBranch("fatjets_pt",fatjets_pt)
        self.out.fillBranch("fatjets_eta",fatjets_eta)
        self.out.fillBranch("fatjets_phi",fatjets_phi)
        self.out.fillBranch("fatjets_mass",fatjets_mass)
        self.out.fillBranch("fatjets_deepw",fatjets_deepw)
        self.out.fillBranch("fatjets_deeph",fatjets_deeph)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
        self.out.fillBranch("met",event.MET_pt)

        return True

v3Module = lambda : v3Producer()
