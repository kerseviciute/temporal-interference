from neuron import h
import os

class Neuron:
    def __init__(self, morphology):
        self.is_created = False
        self.morphology = morphology

        self.hoc_dir = os.getcwd()

        self.create_cell()

    def create_cell(self):
        # Only create the cell if it is not yet created
        if self.is_created: return

        # Load standard run tools
        h.load_file("stdrun.hoc")

        # Load cell anatomical and biophysical properties
        self.load_hoc("cellspec_c62564.hoc")
        self.load_hoc("biophys.hoc")
        self.load_hoc("fluct.hoc")

        self.insert_mechanism("extracellular")
        self.insert_mechanism("xtrau")

        # Only interpolates sections that have xtrau
        self.load_hoc("interpxyzu.hoc")

        self.load_hoc("setpointersu.hoc")

        # Computes scale factor used to calculate extracellular potential
        # produced by a uniform electrical field
        self.load_hoc("calcrxcu.hoc")

        # Extracellular stimulus
        self.load_hoc("zapstimu2.hoc")

        self.is_created = True

    def insert_mechanism(self, mechanism):
        for sec in h.allsec():
            sec.insert(mechanism)

    def load_hoc(self, hoc_file):
        hoc_path = os.path.join(self.hoc_dir, hoc_file)
        h.load_file(str(hoc_path).replace('\\', '/'))
