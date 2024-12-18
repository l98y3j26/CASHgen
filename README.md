# CASHgen

**CASHgen** is  an improved Python code for the automated generation of CASH structures, based on the pyCSH code proposed by Z. Casar et al. [1]. 
It is built upon the brick model introduced by Kunhi Mohamed et al. [2] and further expanded by X. Zhu et al. [3].

[1] Z. Casar, J. López-Zorrilla, H. Manzano, E. Duque-Redondo, A.K. Mohamed, K. Scrivener, P. Bowen, pyCSH: Automated atomic-level structure generation of bulk C-S-H and investigation of their intrinsic properties, Cement and Concrete Research, 183 (2024) 107593.
[2] A. Kunhi Mohamed, S.C. Parker, P. Bowen, S. Galmarini, An atomistic building block description of C-S-H Towards a realistic C-S-H model, Cement and Concrete Research, 107 (2018) 221-235.
[3] X. Zhu, M. Vandamme, L. Brochard, Z. Zhang, Q. Ren, C. Li, B. He, H. Zhang, Y. Zhang, Q. Chen, Z. Jiang, Nature of aluminates in C-A-S-H: A cryogenic stability insight, an extension of DNA-code rule, and a general structural-chemical formula, Cement and Concrete Research, 167 (2023) 107131.


# License
 
Copyright (C) 2024 Jon López-Zorrilla (jon.lopezz@ehu.eus), Ziga Casar
Copyright (C) 2025 Yunjian Li (liyunjian@must.edu.mo), Cheng Chen

CASHgen is free software based on pyCSH; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, you can obtain one at https://www.gnu.org/licenses/old-licenses/gpl-2.0.html.

# Installation and usage

The requirements for using CASHgen are having a Python 3 environment and installing the Numpy package. If plotting is involved, matplotlib and scikit-learn are also needed. The executable file for the code is main_brick.py:

On Linux systems, you can run it by entering:

python3 main_brick.py

On Windows systems, using debugging software may make the process more convenient.

The parameters that control the generated CSH models are defined in `parameters.py`, and are the following:

 - `seed`: **Optional**. Default : 1123
   Seed for the random number generator.
   
- `shape`: **Required**
  Shape of the supercell of defective tobermorite 14 A. Tuple of the shape (Nx, Ny, Nz).
  
- `Ca_Si_ratio`: **Required**
Target Ca/Si ratio of the CASH model.

- `W_Si_ratio`: **Required**
Target water/Si ratio of the CASH model.

- `Al_Si_ratio`: **Required**
Target Al/Si ratio of the CASH model.

- `Al_Four`: **Required**
The proportion of four-coordinated aluminum to total aluminum.

- `Al_Five`: **Required**
The proportion of five-coordinated aluminum to total aluminum.

- `Al_Six`: **Required**
The proportion of six-coordinated aluminum to total aluminum.

- `Al_Five_inter`: **Required**
The proportion of five-coordinated aluminum incorporated into the interlayer.

- `Al_Five_inter`: **Required**
The proportion of six-coordinated aluminum incorporated into the interlayer.

- `prefix`: **Optional**. Default: 'input'
  Name of the output files.
 
- `N_samples`: **Required**
Number of structures to be generated.

- `make_independent`: **Optional**. Default: False
  Whether to ensure that none of the structures are different spatial arrangement of the same unit cells or not.

- `offset_gaussian`: **Optional**. Default: False
  If True, some preliminary calculations will be done in order to impose more strictly that the amount of Ca-OH and Si-OH are closer to the experimental values.

- `width_Ca_Si`: **Optional**. Default: 0.1
Width of the gaussian used for sampling the Ca/Si ratio of each of the unit cells that compose the total supercell.  Smaller values (e.g. 0.01) will  lead to ratios closer to the target, but might cause the code to fail.

- `width_SiOH`: **Optional**. Default: 0.08
Width of the gaussian used for sampling the Si-OH/Si ratio.

- `width_CaOH`: **Optional**. Default: 0.04
Width of the gaussian used for sampling the Ca-OH/Ca ratio.

- `create`: **Required**.
True if you want to generate new structures, False, if other modes are required. See `check` and `read_structure`.

- `write_lammps`: **Optional**. Default: True
Write a `.data` LAMMPS data file for each of the structures. 

- `write_lammps_erica`: **Optional**. Default: True
Write a `.data` LAMMPS data file for each of the structures, with core-shell, bonds and angle information to use with EricaFF.

- `write_vasp`: **Optional**. Default: True
Write a `.vasp` VASP data file for each of the structures. 
