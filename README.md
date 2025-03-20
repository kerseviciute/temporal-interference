# Simulate the effects of a planar electric field at different frequencies on a realistic neuron

## Future problems

- [ ] mechanism of choice does not implement depression

## TODO

- [ ] Make sure the synapses work correctly and their weights are not updated when they shouldn't be (or if they are - check if other conditions are met)

- [x] Run LTP protocol + obtain weights with / without electric field
- [ ] Use weights obtained during LTP and run with naturally occurring inputs with / without electric field
- [ ] Use weights obtained during LTP and run with unsynchronised Poisson inputs with / without electric field

- [ ] AP threshold electric field strength
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
