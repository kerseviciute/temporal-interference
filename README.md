# Simulate the effects of a planar electric field at different frequencies on a realistic neuron

## Snakemake run

```shell
snakemake --use-conda --rerun-triggers mtime --cores 4
```

## Notes

- Variable time step implementation is not possible with Gfluct2.

## Future problems

- [ ] mechanism of choice does not implement depression
- [ ] cell morphology (cell c62564) has been updated to include an axon: https://neuromorpho.org/neuron_info.jsp?neuron_name=c62564
- [ ]

## TODO

- [x] Make sure the synapses work correctly and their weights are not updated when they shouldn't be (or if they are - check if other conditions are met)

- [ ] How to create multiple separate neurons in a single python session?

- [x] Run LTP protocol + obtain weights with / without electric field
- [x] Use weights obtained during LTP and run with naturally occurring inputs with / without electric field
- [x] Use weights obtained during LTP and run with unsynchronised Poisson inputs with / without electric field

- [x] AP threshold electric field strength
- [ ] Test the effect of the orientation of the electric field on synaptic plasticity (esp. parallel vs perpendicular)
- [x] Insert NMDA

- [ ] Continue cleaning up the code (go through old notebooks to check what is worth saving)
- [ ] Regularly rerun all notebooks to ensure that they are up-to-date

## Commands

Start NEURON GUI:

```{shell}
nrngui
```

Run .hoc file:

```{shell}
nrniv model.hoc
```

Run .hoc interactively:

```{shell}
nrniv main.hoc -
```

## Compile NMODL files

```shell
nrnivmodl
```
