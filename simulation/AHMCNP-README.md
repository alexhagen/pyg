# AH MCNP Python Wrapper

This is an object oriented way of creating MCNP input decks for use in the MFARL lab, so the generality of MCNP is much reduced.  Writing using OOP allows for the entire thing to be modular and to move things around on the grid.  It has also been writting to allow for submitting to qsub in efficient ways

## Example

An input deck can be created with just a few line python file, such as:

```python

import ..simulation.ahmcnp

sim = mcnp();
sim.add_message("hi");
sim.add_surface();
sim.compileinp("filename.inp");
```