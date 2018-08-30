#! pbe/sto-3g H2O DFT energy  
import os
import sys
import utils
import addons
import qcdb

print('        <<< Literal nwchem.nw to NWChem >>>')


nwchem {
memory 300 mb
geometry units Angstrom
O     0.000000000000    0.000000000000   -0.068516219310
H     0.000000000000   -0.790689573744    0.543701060724
H     0.000000000000    0.790689573744    0.543701060724
end
basis spherical
 * library sto-3g
end
charge 0

dft
direct
xc xpbe96 cpbe96
grid lebedev 99 14
convergence energy 1e-7 density 1e-7
end

task dft energy
}

energy ('nwchem')

assert compare_values(-75.234018772562, qcdb.get_variable('dft total energy'), 5, 'DFT')  #TEST
assert compare_values(-75.234018772562, qcdb.get_variable('current energy'), 5, 'DFT')  #TEST

nwchem {}
clean ()
clean_variables()

print('        <<< Through Psi4 format >>>')

memory 300 mb

molecule h2o {
0 1
O
H 1 1.0
H 1 1.0 2 104.5
}

set {
print(2)
basis sto-3g

df_scf_guess false #Doing nothing 
scf_type direct
e_convergence 7
d_convergence 7
dft_spherical_points 590
dft_radial_points 99
reference rks
}

set dft_functional pbe

nwchem {}

energy ('nwchem-dft')

assert compare_values(-75.234018772562, get_variable('dft total energy'), 5, 'DFT')  #TEST
assert compare_values(-75.234018772562, get_variable('current energy'), 5, 'DFT')  #TEST
 
clean()
clean_variables()
nwchem {}

# these make a clean slate for the next job
revoke_global_option_changed('NWCHEM_DFT_DIRECT')
revoke_global_option_changed('NWCHEM_DFT')
revoke_global_option_changed('NWCHEM_DFT_XC')
revoke_global_option_changed('NWCHEM_DFT_GRID')
revoke_global_option_changed('NWCHEM_DFT_CONVERGENCE')

print('        <<< Translation of nwchem.nw to Psi4 format to NWChem >>>')

memory 300 mb

molecule h2o {
0 1
O
H 1 1.0
H 1 1.0 2 104.5
}

set {
print 2
basis sto-3g

df_scf_guess false
nwchem_dft_direct true
nwchem_dft_grid [lebedev, 99, 14]
nwchem_dft_convergence [energy, 1.e-7, density, 1.e-7]
}

set nwchem_dft_xc [xpbe96, cpbe96]

nwchem {}

energy ('nwchem-dft')

assert compare_values(-75.234018772562, get_variable('dft total energy'), 5, 'DFT')  #TEST
assert compare_values(-75.234018772562, get_variable('current energy'), 5, 'DFT')  #TEST
