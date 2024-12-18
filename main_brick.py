from mod_construct_brick import *
from mod_sample import *
from mod_construct_supercell import *
from mod_write import *
from parameters import *
from mod_make_graphs import *
import time


# Check input parameters:
try: seed
except NameError: seed = 1123

try: width_Ca_Si
except NameError: width_Ca_Si = 0.1

try: width_SiOH
except NameError: width_SiOH = 0.08

try: width_CaOH
except NameError: width_CaOH = 0.04

try: offset_gaussian
except NameError: offset_gaussian = False

try: make_independent
except NameError: make_independent = False

try: create
except NameError: create = False

try: write_lammps
except NameError: write_lammps = True

try: write_lammps_erica
except NameError: write_lammps_erica = True

try: write_vasp
except NameError: write_vasp = False



try: prefix
except NameError: prefix = "input"



widths = [width_Ca_Si, width_SiOH, width_CaOH]

np.random.seed(seed)
random.seed(seed+10)


list_properties = []


if create:
	# Get all possible bricks
	bricks, sorted_bricks = get_all_bricks(pieces)
	if not os.path.isdir("./output"):
		os.makedirs('./output')


	unitcell = np.array([ [6.7352,    0.0 ,      0.0],
				 		   [-4.071295, 6.209521,  0.0],
						   [0.7037701, -6.2095578, 13.9936836] ])

	supercell = np.zeros((3,3))
	for i in range(3):
		supercell[i,:] = unitcell[i,:]*shape[i]



	N_brick = shape[0]*shape[1]*shape[2]

	offset = [0.0, 0.0, 0.0]
	if offset_gaussian:
		off_Si, off_Ca = get_offset(5000, sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, Al_Si_ratio, Al_Four, Al_Five, Al_Six)
		offset = [off_Si,off_Ca]


	list_crystals = []
	cont = 0


	t = time.time()
	jsample = 0
	for isample in range(N_samples):
		crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six, N_water, r_2H_Si = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, Al_Si_ratio, Al_Four, Al_Five, Al_Six,Al_Five_inter,Al_Six_inter,offset=offset )


		crystal_index = [ brick.ind for brick in crystal ] 

		new = False

		if make_independent and set(crystal_index) not in list_crystals:
			new = True
			list_crystals.append(set(crystal_index))
		elif not make_independent and crystal_index not in list_crystals:
			new = True
			list_crystals.append(crystal_index)

		if new:
			# if you want to get N_Al==0
			Al_Si_ratio_new = N_Al / N_Si if N_Si != 0 else 0
			Al_Four_ratio = N_Al_Four / N_Al if N_Al != 0 else 0
			Al_Five_ratio = N_Al_Five / N_Al if N_Al != 0 else 0
			Al_Six_ratio = N_Al_Six / N_Al if N_Al != 0 else 0

			list_properties.append([N_Ca / N_Si, r_SiOH, r_CaOH, MCL, jsample + 1,r_2H_Si, r_AlOH, Al_Si_ratio_new, Al_Four_ratio,Al_Five_ratio, Al_Six_ratio])
			#if you noly get some CASH and not get CSH,you can use it in below
			#list_properties.append( [N_Ca/N_Si, r_SiOH, r_CaOH, MCL, jsample+1, r_2H_Si, r_AlOH, N_Al/N_Ca, N_Al_Four/N_Al, N_Al_Five/N_Al, N_Al_Six/N_Al] )

			water_in_crystal = fill_water(crystal, N_water = N_water)

			crystal_rs, water_in_crystal_rs =  reshape_crystal(crystal, water_in_crystal, shape)
			entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal_rs, water_in_crystal_rs, shape, pieces )

			entries_angle = get_angles(crystal_dict, water_dict, shape)

			# Water molecule overlap
			entries_crystal, N_not_ok, itry = check_move_water_hydrogens(entries_crystal)
			
			if N_not_ok != 0:
				print("Warning: structure {: 5d} contains {: 5d} wrong water molecules".format(jsample, N_not_ok))
			else:
				print("Structure {: 5d} converged after {: 5d} iterations".format(jsample, itry))


			write_output( jsample, entries_crystal, entries_bonds, entries_angle, shape, crystal_rs, water_in_crystal_rs,
					 	  supercell, N_Ca, N_Si, r_SiOH, r_CaOH, MCL,N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six, write_lammps, write_lammps_erica, write_vasp,prefix)

			jsample += 1

	print("Generation completed in {: 12.6f} s".format(time.time()-t))

	list_properties = np.array(list_properties)	
	plot_XOH_X(list_properties)
	plot_MCL(list_properties,Al_Si_ratio)
	plot_distributions(list_properties)
	plot_water(list_properties)

	get_sorted_log(list_properties)




