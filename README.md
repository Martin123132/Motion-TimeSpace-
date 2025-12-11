# Motion–TimeSpace Research Program  
### Empirical Patterns • Computational Models • Geometric Hypotheses

This repository is an open research program built around a simple guiding question:

**Do recurring geometric patterns appear across gravitational, cosmological, and dynamical systems — and if so, can a single motion–curvature mechanism help explain them?**

The emphasis throughout this project is **empirical first**,  
**computational second**,  
**theoretical last**.

No claims of finality.  
No “theory of everything.”  
Just systematic exploration.

---

## 🚀 What This Repository Contains

### **1. Empirical Analyses (Data-Driven)**
Studies examining patterns that repeatedly show up across scales:

- **Galaxy rotation curves** — universal mass–radius scaling \(M(r) \propto r^{1.878}\) across 80+ spirals  
- **Cluster dynamics** — intermediate scaling regime between galaxies and planetary systems  
- **CMB Cold Spot & Great Attractor** — statistical correlation tests with curvature predictions  
- **Cosmology** — SN/BAO/H(z) fits revealing redshift-dependent curvature gradients  
- **Outlier classification** — environmental shifts, morphology trends, ultra-dwarf deviations  

These are purely observational and reproducible using the scripts in the repo.

---

### **2. Computational Models**
Fully working numerical tools used throughout this program:

- **Curvature Trap** — generative solver reproducing galaxy mass profiles  
- **Gravitational lensing reconstructor** — RMSE < 0.002 accuracy on cluster maps  
- **Cosmology solvers (MBT-5)** — fits expansion and growth tensions  
- **Orbital-decay corrections** — binary pulsar fits giving a small curvature-persistence factor  
- **Kerr interior regularisation** — minimum-length curvature saturation model  
- **Navier–Stokes regularity tools** — energy-bounded flow evolution under geometric resistance  
- **Neutrino mixing solver** — diagonalises curvature-exchange tensor to recover PMNS angles  

All code is open, reproducible, and centred on numerical experimentation.

---

## 📐 Why Motion–Curvature Shows Up Everywhere (Working Hypothesis Only)

Across many independent analyses, a recurring structure appears:

- systems tend to obey **power-law geometric scaling**,  
- curvature grows but **never truly diverges**,  
- motion feeds back into geometry via **persistence or resistance**,  
- information-like terms behave as if they store **“memory”** of past motion.

This repo uses the term **Motion–TimeSpace (MTS)** as a *working framework* to organise and test these ideas.

Important:

> **MTS is not presented as a complete theory — it is a hypothesis-driven research direction.**  
> Its role is to unify repeated patterns and propose mechanisms worth testing, not to claim final answers.

---

## 🧩 Research Themes & Representative Files

### **1. Galactic & Cluster Physics**
- *Galaxy Rotation Curve Analysis Using MBT Framework*  
- *An Empirical Scaling Relation for Galaxy Rotation Curves*  
- *Composite Mass Profiles and the MTS Curvature Trap*  
- *Universal Gravitational Scaling (TNG vs observations)*

Focus: mass–radius exponent, curvature traps, environmental effects.

---

### **2. Cosmology & Large-Scale Structure**
- *A Thermodynamic Extension of General Relativity Resolving the Hubble Tension*  
- *MBT Cosmology: Three-Dataset Analysis & Replication Guide*  
- *Unified Geometric Framework for Cosmology and Thermodynamics*  
- *Pantheon+* (distance-redshift analysis)

Focus: redshift-dependent curvature gradient \( \Gamma_G(z) \), MBT-5 expansion law, growth-rate predictions.

---

### **3. General Relativity Extensions**
- *MTS Curvature Saturation as Minimum-Length Regularisation of the Kerr Interior*  
- *MTS Regularity Framework*  
- *The Motion–TimeSpace Action Principle*  
- *The Fundamental Action of MTS Field Theory*

Focus: emergent metric from ψ-field derivatives, minimum length, removal of singularities, modified Einstein equations.

---

### **4. Orbital & Local Dynamics**
- *MTS Orbital–Decay Derivation*  
- *The Universal Orbital Hierarchy in MTS*  
- *Why Orbital Dynamics Has an e Problem*

Focus: small corrections to GR energy loss, curvature persistence, hierarchy mapping.

---

### **5. Quantum & Field-Level Explorations**
- *The Proton as a Fundamental MTS Soliton*  
- *Numerical Curvature-Driven Fusion (10⁷-particle)*  
- *Yang–Mills Mass Gap via Motion Theory*  
- *The Riemann Hypothesis as a Geometric Invariance Principle*

Focus: ψ-field nonlinearities, geometric stability, curvature-frequency relations, number-theory analogues.

---

### **6. Tools, Utilities & Infrastructure**
- *The Geometric Motion Wrapper (GMW)* — high-throughput compression format  
- *MTS GRB Prediction Kit*  
- *MTS-Universe Mapper*

Focus: analysis automation, data compression, and geometric visualisation.

---

## 🔬 What the Evidence Currently Supports

### **Empirical**
- Scaling exponent \(m \approx 1.878\) is robust across large samples.  
- Clusters form a clear intermediate regime (not binaries).  
- Outlier behaviour is structured and predictable.  
- CMB Cold Spot correlations are statistically nontrivial.  
- Redshift-dependent curvature gradient improves cosmological fits.

### **Computational**
- Curvature Trap reproduces galaxy mass distributions.  
- MTS Kerr regularisation removes singularity while preserving GR outside core.  
- Orbital-decay correction factor \( \Gamma_\kappa \approx 3\times10^{-3} \) fits pulsar data.  
- Lens reconstruction achieves extremely low RMSE.

### **Theoretical (Exploratory)**
- ψ-field + curvature-exchange term produces modified Einstein equations.  
- Minimum-length + resistance guarantees fluid regularity and finite curvature in strong gravity.  
- Coarse-graining ψ leads to emergent metric behaviour resembling GR.

Again — **these are hypotheses, not conclusions**.

---

---

## 🤝 How to Engage With This Repository

### For Skeptics
- Start with `universal-scaling/` — it’s pure data.  
- Check the outlier maps.  
- Read the empirical papers before the theoretical ones.

### For Collaborators
- Open issues with data, alternative models, or contradictions.
- Suggest better ways to test curvature-persistence hypotheses.
- Contribute numerical experiments or replication notebooks.

### For Students
- Learn the difference between *observation*, *model*, and *interpretation*.  
- Explore how a single idea evolves across multiple physical domains.  
- Use this repo as an example of exploratory scientific method.

---

## 📎 Citation

```bibtex
@misc{mts_framework,
  author = {Martin Ollett},
  title = {Motion–TimeSpace Research Program: Empirical Patterns, Computational Models, and Geometric Hypotheses},
  year = {2025},
 
```

---

## ✉️ Contact
- GitHub Issues — questions, bugs, discussion  
- Email — ollett123123@outlook.com  
- Twitter — @nodicephysics  

---

## 🌱 Final Note

This repository is not about asserting a final theory.  
It is about **following patterns, building tools, testing ideas, and letting the evidence shape the direction**.

The journey continues.

## Why This Project Is Hosted on GitHub (and Not Exclusively on arXiv)

A common assumption in modern physics culture is that scientific work must appear on arXiv to be considered valid.  
This repository takes a different approach for three reasons:

### **1. Science is defined by reproducibility, not by platform**
Peer review is a process, not a location.

GitHub provides:

- full code  
- data  
- analysis pipelines  
- version history  
- open discussion  
- public, timestamped work  

This level of transparency often exceeds what is possible in a traditional PDF upload.

### **2. The research here is iterative and computational**
Many results in this program rely on:

- evolving numerical experiments  
- parameter sweeps  
- simulation revisions  
- updated datasets  
- notebooks and pipelines  
- live benchmarks  
- executable code  

arXiv is a static-paper archive.  
GitHub is the correct environment for work that grows, updates, and improves over time.

### **3. Open scrutiny is stronger here than in preprint culture**
Everything in this repository is:

- public  
- testable  
- falsifiable  
- reproducible by anyone  
- open to critique  
- version-controlled  

This enables true *community peer review*, not just publication into a silent preprint void.

### **4. arXiv is optional, not mandatory**
Nothing in scientific practice requires arXiv for legitimacy.  
If a result is:

- reproducible,  
- transparent,  
- mathematically coherent,  
- backed by data,  

then the platform it lives on does not determine its scientific value.

This project remains open to future formal publications,  
but its natural home — where the code, data, and methods live — is here.


