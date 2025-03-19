from neuron import h
import os
from abc import ABC, abstractmethod


class AbstractNeuron(ABC):
    """
    The abstract neuron class encapsulates all steps to initialize
    the model neuron. This includes loading the necessary files,
    inserting mechanisms, and defining init() for resetting the neuron.

    See the extensions of this class for models with different synapse
    types. Use only those models to run the simulations.

    NOTE: only one neuron per python session can be created.
    """

    # TODO: would it be possible to define the neuron in such a way
    # TODO: that it is separate from h? (now these are equivalent)
    # TODO: would be useful to run simulations in parallel
    def __init__(self):
        self.__is_created = False
        self.__hoc_dir = os.getcwd()

        self.create_cell()

    def create_cell(self):
        # Only create the cell if it is not yet created
        if self.__is_created:
            print("Cell already created")
            return

        print("Creating cell")

        # Load standard run tools
        h.load_file("stdrun.hoc")

        # Load cell anatomical and biophysical properties
        self.load_hoc("nrnhoc/cellspec_c62564.hoc")
        self.load_hoc("nrnhoc/biophys.hoc")
        self.load_hoc("nrnhoc/fluct.hoc")

        self.insert_mechanism("extracellular")
        self.insert_mechanism("xtrau")

        # Only interpolates sections that have xtrau
        self.load_hoc("nrnhoc/interpxyzu.hoc")

        self.load_hoc("nrnhoc/setpointersu.hoc")

        # Computes scale factor used to calculate extracellular potential
        # produced by a uniform electrical field
        self.load_hoc("nrnhoc/calcrxcu.hoc")

        # Extracellular stimulus
        self.load_hoc("nrnhoc/zapstimu2.hoc")

        h('proc init() { nrnpython("AbstractNeuron._AbstractNeuron__neuron_init()") }')

        self.initialize()

        self.__is_created = True

    # noinspection PyMethodMayBeStatic
    def insert_mechanism(self, mechanism):
        for sec in h.allsec():
            sec.insert(mechanism)

    def load_hoc(self, hoc_file):
        hoc_path = os.path.join(self.__hoc_dir, hoc_file)
        h.load_file(hoc_path)

    @staticmethod
    def __neuron_init():
        h.t = 0

        for section in h.allsec():
            # Reset the resting potential
            section.v = h.Vrest

            # Set reversal potential for sodium channels
            if h.ismembrane("nax", sec = section) or \
               h.ismembrane("na3", sec = section):
                for segment in section: segment.ena = 55

            # Set reversal potential for potassium channels
            if h.ismembrane("kdr", sec = section) or \
               h.ismembrane("kap", sec = section) or \
               h.ismembrane("kad", sec = section):
                for segment in section: segment.ek = -90

            # Set reversal potential for h-current
            if h.ismembrane("hd", sec = section):
                for segment in section: segment.ehd_hd = -30

        # Set membrane potential to resting values
        h.finitialize(h.Vrest)
        # Calculate the currents
        if h.cvode.active():
            h.cvode.re_init()
        else:
            h.fcurrent()

        for section in h.allsec():
            if h.ismembrane("na3", sec = section) or \
               h.ismembrane("nax", sec = section):
                for segment in section:
                    # Calculate passive current for sodium channels
                    segment.e_pas = segment.v + (segment.ina + segment.ik) / segment.g_pas

            if h.ismembrane("hd", sec = section):
                # Calculate passive current for h-current mechanisms
                for segment in section:
                    segment.e_pas = segment.e_pas + segment.i_hd / segment.g_pas

        print("Neuron initialized")

    """
        initialize() is called during create_cell(). Use this method to include
        synapses, set up stimulation parameters, etc.
    """
    @abstractmethod
    def initialize(self):
        pass

    """
        run() is a method used to run the simulation.
    """
    @abstractmethod
    def run(self):
        pass
