---
title: 'COHESIVM: Combinatorial h+/e- Sample Investigation using Voltaic Measurements'
tags:
  - Python
  - materials science
  - combinatorial approach
  - high-throughput analysis
  - lab automation
authors:
  - name: Maximilian Wolf
    orcid: 0000-0003-4917-7547
    affiliation: '1, 2'
  - name: Selina Götz
    orcid: 0000-0003-4962-153X
    affiliation: '1'
  - name: Georg K.H. Madsen
    orcid: 0000-0001-9844-9145
    affiliation: '2'
  - name: Theodoros Dimopoulos
    orcid: 0000-0002-3620-9645
    affiliation: '1'
affiliations:
 - name: Center for Energy, AIT Austrian Institute of Technology GmbH, Austria
   index: 1
 - name: Institute of Materials Chemistry, TU Wien, Austria
   index: 2
date: 13 August 2024
bibliography: paper.bib
---

# Summary

Accelerating materials discovery and optimization is crucial for transitioning 
to sustainable energy conversion and storage. In this regard, materials acceleration 
platforms (MAPs) can significantly shorten the discovery process, cutting material and 
labor costs [@aspuru2018materials]. Combinatorial and high-throughput methods are 
instrumental in developing said MAPs, enabling autonomous operation and the generation 
of large datasets [@maier2007combinatorial]. Therefore, in a previous work, we developed 
combinatorial deposition and analysis techniques for the discovery of new semiconductor 
materials [@wolf2023accelerated]. To drive further innovation in the field, COHESIVM was 
created, which facilitates combinatorial analysis of material and device properties 
through the following key features:

- A **generalized workflow** reduces redundancy and ensures consistency across different 
  experimental setups.
- The **modular design** abstracts devices, contact interfaces, and measurement routines 
  into interchangeable units.
- **Efficient data handling** is achieved through robust metadata collection and 
  well-structured storage.

# Statement of need

COHESIVM is a Python package that aims to streamline the setup and execution of
combinatorial voltaic measurements. Typically, experimental workflows and data handling 
are implemented on a use-case basis, which can be time-consuming and error-prone. With 
COHESIVM however, these foundational features are pre-implemented and designed to be 
reusable across different scenarios. The package provides a generalized framework, following 
well-documented abstract base classes, which facilitates the implementation of 
application-specific components. Additionally, graphical user interfaces allow users with 
less programming experience to execute experiments and analyze the collected data.

COHESIVM stands out for its straightforward design and the ease with which it can be 
interfaced with existing APIs to implement new devices seamlessly. While there are a number 
of tools available in the public domain that provide control over measurement equipment 
[@pernstich2012instrument; @weber2021pymodaq; @fuchs2024nomad], many of these tools focus 
primarily on graphical user interfaces which can limit their flexibility. Python APIs, such 
as ``bluesky`` [@allan2019bluesky], do offer experiment control and data collection capabilities. 
However, COHESIVM's advantage lies in its simplicity and targeted application in combinatorial 
experiments.

So far, COHESIVM has been used for the investigation of oxide semiconductor heterojunctions where 
it enables to quickly screen a matrix of 8&nbsp;×&nbsp;8 pixels on a single substrate 
(25&nbsp;mm × 25&nbsp;mm). The package's documentation provides a 
[high-level description](https://cohesivm.readthedocs.io/en/latest/tutorials/real-world_example.html) of how COHESIVM was applied in this context. In brief, 
64 gold pads were sputtered onto the sample using a mask, which is [available in the repository](https://github.com/mxwalbert/cohesivm/tree/main/hardware/ma8x8). 
Schematics and board files for reproducing the utilized ``MA8X8`` interface are provided
as well. The sample was mounted on this interface, which was then placed under a solar simulator 
(Ossila, AAA classification) and connected to the electronic measurement equipment (Agilent 4156C). 
Employing COHESIVM, the current-voltage characteristics of all 64 pixels were recorded and the
resulting data was analysed to generate a map of open-circuit voltages.

# Author Contributions

**Maximilian Wolf:** Methodology, Software, Writing - Original Draft. **Selina Götz:** Software, Validation. 
**Georg K.H. Madsen:** Writing - Review & Editing, Supervision. **Theodoros Dimopoulos:** Conceptualization, 
Resources, Supervision.

# References
