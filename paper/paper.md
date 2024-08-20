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
materials [@wolf2023accelerated]. To further advance the portfolio, COHESIVM was created, 
which facilitates combinatorial analysis of material and device properties.

# Statement of need

COHESIVM is a Python package that aims to simplify the process of setting up and 
executing combinatorial voltaic measurements. It provides researchers with a flexible, 
modular framework that can be tailored to various experimental needs. Following the 
well-documented abstract base classes, application-specific components are easily 
implemented while COHESIVM takes care of the experimental workflow and data collection. 
Additionally, the package provides graphical user interfaces, allowing users with less 
programming experience to execute experiments and analyze the collected data.

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
(25&nbsp;mm × 25&nbsp;mm) [@wolf2024unpublished]. The main branch of the GitHub repository 
includes the implemented components and hardware documentation related to this work.

# References