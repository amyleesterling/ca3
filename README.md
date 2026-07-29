# CA3 renderings

3D renderings from a connectomic reconstruction of mouse hippocampal CA3.

**Renderings:** https://amyleesterling.github.io/ca3/

**Preprint:** [Connectomic reconstruction from hippocampal CA3 reveals spatially graded mossy fiber inputs and selective feedforward inhibition to pyramidal cells](https://www.biorxiv.org/content/10.1101/2025.07.09.663979v1)

Zheng, Park, Hammerschmith, Lu, Yu, Sorek, Silverman, Jordan, Sterling, Silversmith, Collman, Seung, Tank. bioRxiv, 15 July 2025.
doi:[10.1101/2025.07.09.663979](https://doi.org/10.1101/2025.07.09.663979) · [PubMed 40791329](https://pubmed.ncbi.nlm.nih.gov/40791329/)

---

## What the study found, in plain language

The hippocampus is where experience becomes memory, and CA3 is the part of it
that binds the pieces of an event together. To understand how, you need to know
not just which cells are present but exactly which ones talk to each other.

This study took a block of mouse CA3, imaged it with an electron microscope, and
traced every neuron and every connection inside it. The result is a complete
wiring diagram of a small piece of real brain: **1,815 pyramidal cells**, the
main excitatory neurons, **229 inhibitory cells**, and more than **55,000 mossy
fibers**, the axons carrying signals in from the neighbouring dentate gyrus.

Three things came out of it.

**Not all pyramidal cells are alike.** Some are covered in elaborate spiny
structures called thorny excrescences, and these cells receive many mossy fiber
inputs. Others, the sparsely thorny cells, receive almost none. The split is
sharp rather than gradual, so these are genuinely two kinds of cell rather than
two ends of one continuum.

**Input is unevenly spread across space.** Cells further along the region receive
substantially more mossy fiber contacts than cells nearer the beginning. Cells
that share the same incoming fibers also sit closer together than chance would
predict, which suggests the wiring is organised rather than arbitrary. Curiously,
the cells receiving the most inputs get them through *smaller* terminals holding
fewer vesicles, so more connections does not simply mean more of everything.

**Inhibition is targeted, not general.** Mossy fibers also drive inhibitory
neurons, which act as brakes on the circuit. But they drive only the inhibitory
neurons that go on to target thorny cells. The inhibitory neurons serving
sparsely thorny cells receive no mossy fiber input at all. So the same signal
that excites one type of cell also recruits the brake belonging specifically to
that type, leaving the other type untouched.

---

## What is in these renderings

| population | count | what it is |
|---|---|---|
| Thorny pyramidal | 182 | excitatory cells with heavy mossy fiber input |
| Sparsely thorny pyramidal | 68 | excitatory cells with almost none |
| Inhibitory interneuron | 28 | local cells that inhibit the pyramidal cells |
| Mossy fiber axons | 688 | incoming axons from the dentate gyrus |
| Presynaptic CA3 cells | 16 | cells whose synaptic output was traced |

982 cells and roughly 124 million triangles in the full scene. Meshes were pulled
from the segmentation through [CAVE](https://caveclient.readthedocs.io/) and
rendered in Blender.

The study's classification reproduces in this subset: thorny cells receive a
median of **22** mossy fiber inputs and 71% clear the threshold of more than 10,
while sparsely thorny cells receive a median of **1** and not one of them
reaches it.
