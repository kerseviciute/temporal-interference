# Simulate the effects of a planar electric field at different frequencies on a realistic neuron

## TODO

- [ ] Go through all the files and make sure the simulations and the figures are up-to-date
- [ ] Run with theta-gamma coupled inputs
- [ ] Run with natural inputs (setup)
- [ ] Remove old unnecessary code
- [ ] Rerun all?
- [ ] Is there a difference between carriers?
- [ ] How to test whether distributions are different?
- [ ] Prepare a presentation for myself and future generations, including detailed description of what has been done
- [ ] Remake notebook for subthreshold carrier strength
- [ ] Firing rates during LTP (and other protocols)
- [ ] Use jupyter notebooks to create images but also run it in Snakemake
- [ ] Clean up the code used to generate the figures, now it's very messy
- [ ] Remove outdated outputs

## Snakemake run

```shell
snakemake --use-conda --rerun-triggers mtime --cores 4
```

## Notes

- Variable time step implementation is not possible with Gfluct2.

## Future problems

- [ ] cell morphology (cell c62564) has been updated to include an axon: https://neuromorpho.org/neuron_info.jsp?neuron_name=c62564

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
