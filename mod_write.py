import numpy as np
import os



def get_lammps_input(input_file, entries_crystal, entries_bonds, entries_angle, supercell, write_lammps_erica):

	N_atom = len(entries_crystal)
	N_bond = len(entries_bonds)
	N_angle = len(entries_angle)

	with open(input_file, "w") as f:
		f.write( "Generated with Brickcode \n\n" )
		f.write( "{: 8d} atoms \n".format(N_atom) )
		f.write( "{: 8d} bonds \n".format(N_bond) )
		f.write( "{: 8d} angles \n".format(N_angle) )
		f.write( "{: 8d} atom types \n".format(9) )
		f.write( "{: 8d} bond types \n".format(3) )
		f.write( "{: 8d} angle types \n".format(3) )
		f.write( " \n" )
		f.write( "{: 12.6f} {: 12.6f} xlo xhi \n".format(0.0, supercell[0,0]) )
		f.write( "{: 12.6f} {: 12.6f} ylo yhi \n".format(0.0, supercell[1,1]) )
		f.write( "{: 12.6f} {: 12.6f} zlo zhi \n".format(0.0, supercell[2,2]) )
		f.write( "{: 12.6f} {: 12.6f} {: 12.6f} xy xz yz \n".format( supercell[1,0], supercell[2,0], supercell[2,1] ) )
		f.write( " \n" )
		f.write( "Masses \n" )
		f.write( " \n" )
		f.write( "1 40.08  #Ca  \n" )
		f.write( "2 28.10  #Si \n" )
		f.write( "3 15.59  #O \n" )
		f.write( "4 0.40   #O(S) \n" )
		f.write( "5 16.00  #Ow \n" )
		f.write( "6 16.00  #Oh \n" )
		f.write( "7 1.00   #Hw \n" )
		f.write( "8 1.00   #H \n" )
		f.write( "9 27.00  #Al \n")
		f.write( " \n" )
		f.write( "Atoms \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8.3f} {: 12.6f} {: 12.6f} {: 12.6f}\n"
		molID = 2
		CS_info = []
		for i in entries_crystal:
			if i[1] == 3:
				f.write( fmt.format(i[0], molID, *i[1:]) )
				CS_info.append( [i[0], molID] )
			elif i[1] == 4:
				f.write( fmt.format(i[0], molID, *i[1:]) )
				CS_info.append( [i[0], molID] )
				molID += 1
			else:
				f.write( fmt.format(i[0], 1, *i[1:]) )
				CS_info.append( [i[0], 1] )
		f.write( " \n" )

		f.write( "Bonds \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8d} \n"
		for i in entries_bonds:
			f.write( fmt.format(*i) )
		f.write( " \n" )

		f.write( "Angles \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8d} {: 8d} \n"
		for i in entries_angle:
			f.write( fmt.format(*i) )
		f.write( " \n" )

		f.write( " \n" )
		fmt = "{: 8d} {: 8d} \n"
		if write_lammps_erica:
			f.write( "CS-Info \n" )
			f.write( "\n" )
			for i in CS_info:
				f.write( fmt.format(*i))



def get_lammps_input_reaxfff(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(7,dtype=int)

	coords = [ [] for i in range(9) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []
	coords_Al = []

	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie == 3:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 5:
			coords_Ow.append(r)
			N_atoms_specie[3] += 1
		elif specie == 6:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 7:
			coords_Hw.append(r)
			N_atoms_specie[4] += 1
		elif specie == 8:
			coords_H.append(r)
			N_atoms_specie[5] += 1
		elif specie == 9:
			coords_Al.append(r)
			N_atoms_specie[6] += 1

		coords[  entry[1]-1 ].append( r )


	together = True
	if together:
		coords_O1 = coords_O1 + coords_Ow
		N_atoms_specie[2] += N_atoms_specie[3]
		N_atoms_specie[3] = 0
		coords_Ow = []

		coords_H = coords_H + coords_Hw
		N_atoms_specie[5] += N_atoms_specie[4]
		N_atoms_specie[4] = 0
		coords_Hw = []

	with open( name, "w" ) as f:
		f.write( "Generated with Brickcode \n\n" )
		f.write( "{: 8d} atoms \n".format(np.sum(N_atoms_specie)) )
		f.write( "{: 8d} atom types \n".format(4) )
		f.write( " \n" )
		f.write( "{: 12.6f} {: 12.6f} xlo xhi \n".format(0.0, supercell[0,0]) )
		f.write( "{: 12.6f} {: 12.6f} ylo yhi \n".format(0.0, supercell[1,1]) )
		f.write( "{: 12.6f} {: 12.6f} zlo zhi \n".format(0.0, supercell[2,2]) )
		f.write( "{: 12.6f} {: 12.6f} {: 12.6f} xy xz yz \n".format( supercell[1,0], supercell[2,0], supercell[2,1] ) )
		f.write( " \n" )
		f.write( "Masses \n" )
		f.write( " \n" )
		f.write( "1 40.08  #Ca  \n" )
		f.write( "2 28.10  #Si \n" )
		f.write( "3 15.79  #O \n" )
		f.write( "4 1.00   #H \n" )
		f.write( "5 27.00  #Al \n")
		f.write( " \n" )
		f.write( "Atoms \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 12.6f} {: 12.6f} {: 12.6f}\n"

		cont = 1
		for i in coords_Ca:
			f.write( fmt.format(cont, 1, 0, *i) )
			cont += 1
		for i in coords_Si:
			f.write( fmt.format(cont, 2, 0, *i) )
			cont += 1
		for i in coords_O1:
			f.write( fmt.format(cont, 3, 0, *i) )
			cont += 1
		for i in coords_H:
			f.write( fmt.format(cont, 4, 0, *i) )
			cont += 1
		for i in coords_Al:
			f.write( fmt.format(cont, 5, 0, *i) )





def get_vasp_input(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(7,dtype=int)

	coords = [ [] for i in range(9) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	#coords_O2 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []
	coords_Al = []

	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie == 3:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 5:
			coords_Ow.append(r)
			N_atoms_specie[3] += 1
		elif specie == 6:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 7:
			coords_Hw.append(r)
			N_atoms_specie[4] += 1
		elif specie == 8:
			coords_H.append(r)
			N_atoms_specie[5] += 1
		elif specie == 9:
			coords_Al.append(r)
			N_atoms_specie[6] += 1

		coords[  entry[1]-1 ].append( r )


	together = True
	if together:
		coords_O1 = coords_O1 + coords_Ow
		N_atoms_specie[2] += N_atoms_specie[3]
		N_atoms_specie[3] = 0
		coords_Ow = []

		coords_H = coords_H + coords_Hw
		N_atoms_specie[5] += N_atoms_specie[4]
		N_atoms_specie[4] = 0
		coords_Hw = []

	#print(np.sum(N_atoms_specie))

	#f.write( " \n" )
	with open( name, "w" ) as f:
		f.write( "kk \n" )
		f.write( "1.0 \n" )
		for i in supercell:
			f.write( "{: 12.6f} {: 12.6f} {: 12.6f} \n".format(*i) )
		f.write( "Ca  Si  O  Ow   Hw  H  Al \n" )
		f.write( "{: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} \n".format(*N_atoms_specie) )
		f.write("Cartesian\n")
		fmt = "{: 12.6f} {: 12.6f} {: 12.6f} \n"
		
		# for i in range(8):
		# #for i in [4, 6]:
		# 	for j in coords[i]:
		# 		f.write( fmt.format(*j) )

		for i in coords_Ca:
			f.write( fmt.format(*i) )
		for i in coords_Si:
			f.write( fmt.format(*i) )
		for i in coords_O1:
			f.write( fmt.format(*i) )
		for i in coords_Ow:
			f.write( fmt.format(*i) )
		for i in coords_Oh:
			f.write( fmt.format(*i) )
		for i in coords_Hw:
			f.write( fmt.format(*i) )
		for i in coords_H:
			f.write( fmt.format(*i) )
		for i in coords_Al:
			f.write( fmt.format(*i) )


def get_xyz_input(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(7,dtype=int)

	coords = [ [] for i in range(9) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	#coords_O2 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []
	coords_Al = []

	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie == 3:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 5:
			coords_Ow.append(r)
			N_atoms_specie[3] += 1
		elif specie == 6:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 7:
			coords_Hw.append(r)
			N_atoms_specie[4] += 1
		elif specie == 8:
			coords_H.append(r)
			N_atoms_specie[5] += 1
		elif specie == 9:
			coords_Al.append(r)
			N_atoms_specie[6] += 1

		coords[  entry[1]-1 ].append( r )


	together = True
	if together:
		coords_O1 = coords_O1 + coords_Ow
		N_atoms_specie[2] += N_atoms_specie[3]
		N_atoms_specie[3] = 0
		coords_Ow = []

		coords_H = coords_H + coords_Hw
		N_atoms_specie[5] += N_atoms_specie[4]
		N_atoms_specie[4] = 0
		coords_Hw = []


	#f.write( " \n" )
	with open( name, "w" ) as f:
		f.write( "{: 12d} \n".format(np.sum(N_atoms_specie)) )
		f.write( " \n" )
		fmt = "{:} {: 12.6f} {: 12.6f} {: 12.6f} \n"
		
		# for i in range(8):
		# #for i in [4, 6]:
		# 	for j in coords[i]:
		# 		f.write( fmt.format(*j) )

		for i in coords_Ca:
			f.write( fmt.format("Ca", *i) )
		for i in coords_Si:
			f.write( fmt.format("Si", *i) )
		for i in coords_O1:
			f.write( fmt.format("O",*i) )
		for i in coords_Ow:
			f.write( fmt.format("O",*i) )
		for i in coords_Oh:
			f.write( fmt.format("O", *i) )
		for i in coords_Hw:
			f.write( fmt.format("H",*i) )
		for i in coords_H:
			f.write( fmt.format("H",*i) )
		for i in coords_Al:
			f.write( fmt.format("Al",*i) )


def get_log(log_file, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL ,N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six):

	N_Oh = 0
	for i in range(shape[0]):
		for j in range(shape[1]):
			for k in range(shape[2]):
				N_Oh+= crystal_rs[i,j,k].N_Oh



	#N_Al_Ca_ratio = N_Al / N_Ca if N_Ca != 0 else 0
	Al_Four_ratio = N_Al_Four / N_Al if N_Al != 0 else 0
	Al_Five_ratio = N_Al_Five / N_Al if N_Al != 0 else 0
	Al_Six_ratio = N_Al_Six / N_Al if N_Al != 0 else 0



	with open(log_file, "w") as f:
		f.write( "Ca/Si ratio:   {: 8.6f} \n".format(N_Ca/N_Si) )
		f.write( "SiOH/Si ratio: {: 8.6f} \n".format(r_SiOH) )
		f.write( "CaOH/Ca ratio: {: 8.6f} \n".format(r_CaOH) )
		f.write( "MCL:           {: 8.6f} \n".format(MCL) )
		f.write( "Al/Si ratio:   {: 8.6f} \n".format(N_Al/N_Si) )
		f.write( "AlOH/Al ratio: {: 8.6f} \n".format(r_AlOH) )
		f.write( "Al_Four_ratio: {: 8.6f} \n".format(Al_Four_ratio) )
		f.write( "Al_Five_ratio: {: 8.6f} \n".format(Al_Five_ratio) )
		f.write( "Al_Six_ratio:  {: 8.6f} \n".format(Al_Six_ratio) )
		f.write( "N_Al_Four:     {: 8.6f} \n".format(N_Al_Four) )
		f.write( "N_Al_Five:     {: 8.6f} \n".format(N_Al_Five) )
		f.write( "N_Al_Six:      {: 8.6f} \n".format(N_Al_Six) )
		f.write( " \n" )
		f.write( "Shape: {: 3d} {: 3d} {: 3d} \n".format(*shape) )
		f.write( " \n" )
		f.write( "Supecell Brick Code: \n" )
		f.write( " Na  Nb  Nc  :   Brick Code \n\n" )
		f.write( "brick_code = { \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):
					f.write( "({: 3d}, {: 3d}, {: 3d})  :   {:}, \n".format(i, j, k, crystal_rs[i,j, k].comb) )
		f.write("}\n\n")
		f.write( "water_code = { \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):
					f.write( "({: 3d}, {: 3d},{: 3d})  :   {:}, \n".format(i, j, k, water_in_crystal_rs[i,j, k]) )
		f.write("}\n")

		f.write( " \n" )
		f.write( "Charge Distribution: \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):

					f.write( "{: 3d} {: 3d} {: 3d}  :   {:} \n".format(i, j, k, crystal_rs[i,j, k].charge) )








def get_sorted_log(list_properties):

	sorted_properties = {}
	for i in list_properties:
		Ca_Si = round(i[0], 4)
		SiOH  = round(i[1], 4)
		CaOH  = round(i[2], 4)
		MCL   = round(i[3], 4)
		Al_Si = round(i[7], 4)
		AlOH  = round(i[6], 4)
		Al_Four = round(i[8], 4)
		Al_Five = round(i[9], 4)
		Al_Six = round(i[10], 4)

		if Ca_Si in sorted_properties:
			if SiOH in sorted_properties[Ca_Si]:
				if CaOH in sorted_properties[Ca_Si][SiOH]:
					if MCL in sorted_properties[Ca_Si][SiOH][CaOH]:
						if Al_Si in sorted_properties[Ca_Si][SiOH][CaOH][MCL]:
							if Al_Four in sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si]:
								if Al_Five in sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four]:
									if Al_Six in sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five]:
										if AlOH in sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six]:
											sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six][AlOH].append(i[4])
										else:
											sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six][AlOH] = [i[4]]
									else:
										sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six] = {AlOH:[i[4]]}
								else:
									sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five] = {Al_Six:{AlOH:[i[4]]}}
							else:
								sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four] = {Al_Five:{Al_Six:{AlOH: [i[4]]}}}
						else:
							sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si] = {Al_Four:{Al_Five: {Al_Six:{AlOH: [i[4]]}}}}
					else:
						sorted_properties[Ca_Si][SiOH][CaOH][MCL] = {Al_Si:{Al_Four:{Al_Five: {Al_Six:{AlOH: [i[4]]}}}}}
				else:
					sorted_properties[Ca_Si][SiOH][CaOH] = {MCL: {Al_Si:{Al_Four:{Al_Five: {Al_Six:{AlOH: [i[4]]}}}}}}
			else:
				sorted_properties[Ca_Si][SiOH] = {CaOH: {MCL: {Al_Si:{Al_Four:{Al_Five: {Al_Six: {AlOH:[i[4]]}}}}}}}
		else:
			sorted_properties[Ca_Si] = {SiOH: {CaOH: {MCL: {Al_Si:{Al_Four:{Al_Five: {Al_Six:{AlOH: [i[4]]}}}}} } }}


	with open("created_samples.log", "w") as f:
		fmt = "Sample: {: 5d}     Ca/Si: {: 8.6f}     SiOH/Si: {: 8.6f}    CaOH/Ca: {: 8.6f}    MCL: {: 8.6f}     Al_Si: {: 8.6f}     Al_Four: {: 8.6f}     Al_Five: {: 8.6f}     Al_Six: {: 8.6f}     AlOH/Al: {: 8.6f} \n"

		sorted_Ca_Si = sorted(sorted_properties.keys())
		for Ca_Si in sorted_Ca_Si:
			sorted_SiOH = sorted(sorted_properties[Ca_Si].keys())
			for SiOH in sorted_SiOH:
				sorted_CaOH = sorted(sorted_properties[Ca_Si][SiOH].keys())
				for CaOH in sorted_CaOH:
					sorted_MCL = sorted(sorted_properties[Ca_Si][SiOH][CaOH].keys())
					for MCL in sorted_MCL:
						sorted_Al_Si = sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL].keys())
						for Al_Si in sorted_Al_Si:
							sorted_Al_Four = sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si].keys())
							for Al_Four in sorted_Al_Four:
								sorted_Al_Five = sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four].keys())
								for Al_Five in sorted_Al_Five:
									sorted_Al_Six = sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five].keys())
									for Al_Six in sorted_Al_Six:
										sorted_AlOH = sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six].keys())
										for AlOH in sorted_AlOH:
											for i in sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL][Al_Si][Al_Four][Al_Five][Al_Six][AlOH]):
												f.write(fmt.format(int(i), Ca_Si, SiOH, CaOH, MCL, Al_Si, Al_Four, Al_Five, Al_Six, AlOH))




def write_output( isample, entries_crystal, entries_bonds, entries_angle, shape, crystal_rs, water_in_crystal_rs,
				  supercell, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six,write_lammps, write_lammps_erica, write_vasp,
				  prefix):

	mypath = os.path.abspath(".")
	path = os.path.join(mypath, "output/")

	if write_lammps or write_lammps_erica:
		name = prefix+"_"+str(isample+1)+".data"
		name = os.path.join(path, name)
		get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, supercell, write_lammps_erica) 
	
	if write_lammps:
		name = prefix+"_reax"+str(isample+1)+".data"
		name = os.path.join(path, name)
		get_lammps_input_reaxfff(name, entries_crystal, supercell)


	name = prefix+"_"+str(isample+1)+".log"
	name = os.path.join(path, name)
	get_log(name, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL,N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six )

	if write_vasp:
		name = prefix+"_"+str(isample+1)+".vasp"
		name = os.path.join(path, name)
		get_vasp_input(name, entries_crystal, supercell)

