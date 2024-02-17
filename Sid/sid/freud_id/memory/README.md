## Sid Memory

This module handles all interfaces with the subjects of our agent's [Freudian _Id_](https://en.wikipedia.org/wiki/Id,_ego_and_superego),
across the memory tiers.

These subjects are:

* Persona
* Human(s)
* Knowledge(s)

These tiers are:

* Core Memory
  Think of this as CPU memory in computing

* Recall Memory
  Think of this as RAM in computing. Still fast, still limited in size, but not as directly accessable as CPU memory

* Archival Memory
  Think of this as disk. Infinately large, but the slowest recall - and because of the largeness, slowest to search


Sid Memory needs to handle
- the model for each of the memory types
- a standard API interface for each memory tier that is backend-agnostic