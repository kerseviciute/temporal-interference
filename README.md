# Simulate the effects of a planar electric field at different frequencies on a realistic neuron

## Snakemake run

```{shell}
conda env create -f env/neuron.yml
conda activate neuron
nrnivmodl nrnmod
```

```shell
conda activate snakemake
snakemake --use-conda --rerun-triggers mtime --cores 4
```

## Notes

- Variable time step implementation is not possible with Gfluct2.

## Future problems

- cell morphology (cell c62564) has been updated to include an axon: https://neuromorpho.org/neuron_info.jsp?neuron_name=c62564

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
