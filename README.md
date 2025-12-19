# About This Software

## Overview

This software is a collaborative development between **AI4Tech** and the **University of Brasília (UnB)** , designed to support **therapeutic planning in magnetic hyperthermia** for the treatment of small tumors using **biocompatible magnetic nanofluids** and **high‑frequency oscillating magnetic fields**.

It integrates **scientific simulation**, **machine learning**, and an intuitive **web‑based interface** to provide clinicians and researchers with instant predictions of key therapeutic quantities relevant to magnetic hyperthermia.

---

## Scientific Background

Magnetic hyperthermia is a promising technique for localized cancer therapy, where magnetic nanoparticles dispersed in biological tissue are heated by an applied oscillatory magnetic field. The temperature rise depends on several interacting physical mechanisms, including nanoparticle dynamics, magnetic losses, and thermal diffusion within tissue.

The numerical foundation of this software is based on **2,000 high‑fidelity simulations** performed with a custom FORTRAN solver developed by **Prof. Rafael Gabler Gontijo (University of Brasília – UnB)**.  

These simulations solve the transient and steady‑state **temperature field** in tumors of **circular or elliptical geometries** using:

- **Finite Difference Method (FDM)** in space  
- **Explicit Euler time integration**  
- A **magnetic heat source term** based on the **imaginary part of the ferrofluid’s complex susceptibility**, computed using the asymptotic model of **Berkov (2009)**

This methodology was validated in previous research by **Gontijo (2025)**, grounded on experimental temperature measurements performed in vivo by **Salloum et al. (2008)**.

---

## Reduced‑Order Model (ROM)

To deliver real‑time predictions, the 2,000 numerical simulations were used to train a **neural network‑based reduced‑order model (ROM)**, implemented by **Nicolas Spogis (CEO, AI4Tech)**.

The ROM takes six input variables:

1. Applied magnetic field intensity  
2. Magnetic field frequency  
3. Tumor radius  
4. Tumor eccentricity (0 = circular, 1 = elongated elliptical)  
5. Nanoparticle volume fraction  
6. Nominal nanoparticle radius  

In **milliseconds**, the ROM predicts the following therapeutic quantities:

- **Steady‑state center temperature**
- **Time to reach steady state**
- **Minimum tumor temperature**
- **Average tumor temperature**
- **Temperature standard deviation** (spatial variation)
- **Equivalent affected‑region radius** (mm)
- **Specific Absorption Rate (SAR)** (W/kg)

These outputs allow clinicians to rapidly evaluate treatment feasibility and expected thermal performance under different physical configurations.

---

## Optimization Features

The software also includes a specialized tool for **treatment optimization**.

Physicians can prescribe:

- Tumor geometry (radius and eccentricity)  
- Ferrofluid properties (particle volume fraction, nanoparticle radius)  
- Target **minimum** and **maximum** tumor temperatures  

The program then searches for feasible combinations of:

- **Magnetic field intensity**, and  
- **Magnetic field frequency**

that satisfy the user‑defined thermal constraints.

Multiple valid solutions are presented, enabling clinicians to choose strategies based on:

- Shortest required treatment time  
- Highest SAR  
- Specific clinical goals  

This transforms magnetic hyperthermia planning into a fast, interactive, data‑driven process.

---

## Scientific References

- **Gontijo, R. G.; Ossege, F. E. L.; Pereira, J. L. J. (2025).**  
  *Evaluation of machine learning algorithms in the prediction of key therapeutic quantities in magnetic hyperthermia.*  
  **Computers & Mathematics with Applications**, **194**, 362–378.  
  https://www.sciencedirect.com/science/article/pii/S089812212500272X

- **Berkov, D. V.; Iskakova, L. Y.; Zubarev, A. Y. (2009).**  
  *Theoretical study of the magnetization dynamics of nondilute ferrofluids.*  
  **Physical Review E**, **79**, 021407.  
  https://journals.aps.org/pre/abstract/10.1103/PhysRevE.79.021407

- **Salloum, M.; Ma, R.; Zhu, L. (2008).**  
  *An in vivo experimental study of temperature elevations in animal tissue during magnetic nanoparticle hyperthermia.*  
  **International Journal of Hyperthermia**, **24**, 589–601.  
  https://pubmed.ncbi.nlm.nih.gov/18979310/

---

## Acknowledgments

This software represents a joint effort combining **computational physics**, **machine learning**, and **therapeutic innovation**.  
We thank all contributors involved in its scientific and technological development.

---

If you use or cite this tool in research or clinical studies, please reference the works listed above and acknowledge the **UnB–AI4Tech Collaboration**.

## Development Team
* [Prof. Dr. Rafael Gabler Gontijo](mailto:rafael.gabler@unb.br) || UNB || <a href="https://rafaelgabler.com.br/" target="_blank">WebSite</a>
* [Prof. Dr. Nicolas Spogis](mailto:nicolas.spogis@gmail.com) || UNICAMP || <a href="https://ai4tech.ai/" target="_blank">WebSite</a>

## Installation

To install the necessary dependencies, you need to have Python installed on your system. If you don't have Python, you can download it [here](https://www.python.org/downloads/). After installing Python, follow the steps below:

1. **Clone the Repository**

   First, clone the NEOThermIA App repository to your local machine.

2. **Install Dependencies**

   Within the project directory, locate the `requirements.txt` file containing all necessary libraries. Install them by running: `pip install -r requirements.txt` 
This will install all dependencies required to run NEOThermIA.

## Execution

To run the application, follow these steps:

* Navigate to the project directory where `main.py` is located.

* Execute the `main.py` file using Python: `python main.py`

* After running the command, Dash will start the local server and you can access the application through your browser. Normally, the URL will be something like `http://127.0.0.1:8051/`.

## Support

If you encounter any problems or have any questions, do not hesitate to open an issue in the GitHub repository or contact us directly.

##  License
This project is licensed under the Apache License - see the LICENSE.md file for details.