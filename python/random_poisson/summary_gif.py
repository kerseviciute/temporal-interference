import imageio.v2 as imageio

# Create GIF
with imageio.get_writer(snakemake.output["gif"], mode = "I", fps = 2) as writer:
    for file in snakemake.input["summaries"]:
        image = imageio.imread(file)
        writer.append_data(image)
