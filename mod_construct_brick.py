import numpy as np
import random
import ast

class Piece(object):
	"""docstring for Piece"""
	def __init__(self, charge, file, random_water=True):
		super(Piece, self).__init__()
		self.charge = charge
		self.N_Ca = 0
		self.N_Si = 0
		self.N_O = 0
		self.N_O_S = 0
		self.N_Ow = 0
		self.N_Oh = 0
		self.N_H = 0
		self.N_Hw = 0
		self.N_Al=0

		self.species = []
		self.coord = []

		cell = np.array([ [6.7352,    0.0 ,      0.0],
		 		   [-4.071295, 6.209521,  0.0],
				   [0.7037701, -6.2095578, 13.9936836] ])

		cell_inv = np.linalg.inv(cell)

		with open("./Blocks_Renamed/"+file) as f:
			lines = f.readlines()
			self.N_atom = int(len(lines)/2)
			for i in range(self.N_atom):
				aux = lines[i*2].split()
				specie = aux[0]

				aux = lines[i*2+1].split()
				r = np.array([ float(x) for x in aux ])

				if specie == "Ca":
					self.species.append( 1 )
					self.N_Ca += 1
				if specie == "Al":
					self.species.append( 9 )
					self.N_Al += 1
				if specie == "Si":
					self.species.append( 2 )
					self.N_Si += 1
				if specie == "O" : 
					self.species.append( 3 )
					self.N_O += 1
				if specie == "O(S)" :
					self.species.append( 4 )
					self.N_O_S += 1
				if specie == "Ow" : 
					self.species.append( 5 )
					self.N_Ow += 1


					if random_water:
						u = np.random.rand(3)
						u = u/np.linalg.norm(u)

						v = np.random.rand(3)
						v = v/np.linalg.norm(v)

						v[2] = (np.cos(104*np.pi/180) - u[0]*v[0] - u[1]*v[1])/u[2]
						v = v/np.linalg.norm(v)

						self.r_H1 = u
						self.r_H2 = v

					else:
						if r[2] > 0.0:
							self.r_H1 = np.array([0, 0, -1.0])
						else:
							self.r_H1 = np.array([0, 0, 1.0])

						if r[1] > 0.0:
							self.r_H2 = np.array([0, -1.0, 0])
						else:
							self.r_H2 = np.array([0, 1.0, 0])

				if specie == "Oh" : 
					self.species.append( 6 )
					self.N_Oh += 1

					if r[2] > 0.0:
						self.r_H1 = np.array([0, 0.707, -0.707])
					else:
						self.r_H1 = np.array([0, -0.707, 0.707])



				frac_r = np.matmul(r, cell_inv) + np.array([0.5, 0.5, 0.5])
				#for i in range(3):
				#	if frac_r[i] > 1:
				#		frac_r[i]-=1
				#	if frac_r[i] < 0:
				#		frac_r[i]+=1
				r = np.matmul(frac_r, cell)
				self.coord.append( r )



pieces = { "SL"   : Piece( charge = -2, file = "SL"   ),
		   "BL"   : Piece( charge = 0,  file = "BL"   ),
		   "SR"   : Piece( charge = 0,  file = "SR"   ),
		   "BR"   : Piece( charge = -2, file = "BR"   ),
                                                             
		   "SLo"  : Piece( charge = -1, file = "SLo"  ),
		   "BLo"  : Piece( charge = 1,  file = "BLo"  ),
		   "SRo"  : Piece( charge = 1,  file = "SRo"  ),
		   "BRo"  : Piece( charge = -1, file = "BRo"  ),
                                                             
                                                             
		   "SU"   : Piece( charge = 0, file =  "SU"  ),
		   "SD"   : Piece( charge = 0, file =  "SD"  ),
		   "SUo"  : Piece( charge = 1, file =  "SUo" ),
		   "SDo"  : Piece( charge = 1, file =  "SDo" ),
		   #"AU"   : Piece( charge = -1,file =  "AU"  ),
		   #"AD"   : Piece( charge = -1,file =  "AD"  ),
		   "AUo"  : Piece( charge = 0, file =  "AUo" ),
		   "ADo"  : Piece( charge = 0, file =  "ADo" ),
		   "AUFo" : Piece( charge = -1, file =  "AUFo" ),
		   "ADFo" : Piece( charge = -1, file =  "ADFo" ),
		   "AUSo" : Piece( charge = -1, file =  "AUSo" ),
		   "ADSo" : Piece( charge = -1, file =  "ADSo" ),
		   "CU"   : Piece( charge = 2, file =  "CU"  ),
		   "CD"   : Piece( charge = 2, file =  "CD"  ),

		   "AIF"  : Piece( charge = -3,  file = "AIF" ),
		   "AIS"  : Piece( charge = -3,  file = "AIS" ),
		   "CII"  : Piece( charge = 2,  file = "CII" ),
                                                             
		   "CIU"  : Piece( charge = 2,  file = "CIU" ),
		   "CID"  : Piece( charge = 2,  file = "CID" ),
                                                             
		   "XU"   : Piece( charge = 2,  file = "XU"  ),
		   "XD"   : Piece( charge = 2,  file = "XD"  ),
                                                             
                                                             
		   "oDL"  : Piece( charge = -1, file = "oDL" ),
		   "oDR"  : Piece( charge = -1, file = "oDR" ),
		   "oUL"  : Piece( charge = -1, file = "oUL" ),
		   "oUR"  : Piece( charge = -1, file = "oUR" ),
		   "oXU"  : Piece( charge = -1, file = "oXU" ),
		   "oXD"  : Piece( charge = -1, file = "oXD" ),
                                                             
                                                             
		   "oMDL" : Piece( charge = -1, file = "oMDL"),
		   "oMDR" : Piece( charge = -1, file = "oMDR"),
		   "oMUL" : Piece( charge = -1, file = "oMUL"),
		   "oMUR" : Piece( charge = -1, file = "oMUR"),
                                                             
                                                             
		   "wDR"  : Piece( charge = 0,  file = "wDR" , random_water = True),
		   "wDL"  : Piece( charge = 0,  file = "wDL" , random_water = True),
		   "wIL"  : Piece( charge = 0,  file = "wIL" , random_water = True),
		   "wIR"  : Piece( charge = 0,  file = "wIR" , random_water = True),
		   "wIR2" : Piece( charge = 0,  file = "wIR2", random_water = True),
		   "wUL"  : Piece( charge = 0,  file = "wUL" , random_water = True),
		   "wXD"  : Piece( charge = 0,  file = "wXD" , random_water = True),
		   "wXU"  : Piece( charge = 0,  file = "wXU" , random_water = True),
                                                             
		   "wMDL" : Piece( charge = 0,  file = "wMDL", random_water = True),
		   "wMUL" : Piece( charge = 0,  file = "wMUL", random_water = True),
		   "wMDR" : Piece( charge = 0,  file = "wMDR", random_water = True),
		   "wMUR" : Piece( charge = 0,  file = "wMUR", random_water = True),

		   "w14" : Piece( charge = 0,  file = "w14",   random_water = True),
		   "w15" : Piece( charge = 0,  file = "w15",   random_water = True),
		   "w16" : Piece( charge = 0,  file = "w16",   random_water = True),

}




class Brick(object):
	def __init__(self, comb, pieces, ind):
		self.ind = ind
		self.comb = comb
		self.charge = 0
		self.N_Si = 0
		self.N_Ca = 0
		self.N_SiO = 0
		self.N_SiOH = 0
		self.N_Al = 0
		self.N_AlO = 0
		self.N_AlOH = 0
		self.N_Al_Four=0
		self.N_Al_Five = 0
		self.N_Al_Six = 0
		self.N_Al_Five_inter = 0
		self.N_Al_Six_inter = 0
		self.N_Oh = 0
		self.N_AUD = 0
		self.N_SUD = 0
		self.N_braket = 0

		list_water = set( ["wDR", "wIL", "wIR", "wIR2", "wUL", "wXD", "wXU", "wMDL", "wMUL", "wMDR", "wMUR", "w14", "w15", "w16"] )

		#list_water = set( ["wDR", "wDR", "wIL", "wIR2", "wUL", "wXD", "wXU", "wMDL", "wMUL", "wMDR", "wMUR"] )

		incompatibility = { "oMUL" : ["wMUL"],
							"oMDL" : ["wMDL"],
							"oMDR" : ["wMDR"],
							"oMUR" : ["wMUR"],
							"oDL" : ["wDL"],
							"oDR" : ["wDR"],
							"oUL" : ["wUL"],
							"oXD" : ["wXD"],
							"oXU" : ["wXU"],

							"oUR" : ["wIR"],

							"SD"  : ["wMDR", "wDR"],
							"SDo" : ["wMDR", "wDR"],
							"SU"  : ["wMUR", "wUL"],
							"SUo" : ["wMUR", "wUL", "w16"],
							#"AD"  : ["wMDR", "wDR"],
							"ADo" : ["wMDR", "wDR"],
							#"AU"  : ["wMUR", "wUL"],
							"AUo" : ["wMUR", "wUL", "w16"],
							"ADFo": ["wMDR", "wDR"],
							"AUFo": ["wMUR", "wUL", "w16"],
							"ADSo": ["wMDR", "wDR"],
							"AUSo": ["wMUR", "wUL", "w16"],
							"AIF" : ["wDR", "oDR"],
							"AIS": ["wDR", "oDR"]

		}


		self.elegible_water = []

		self.excluded = set()
		for p in comb:
			if p != None:
				self.charge += pieces[p].charge
				self.N_Si += pieces[p].N_Si
				self.N_Ca += pieces[p].N_Ca
				self.N_Oh += pieces[p].N_Oh
				self.N_Al += pieces[p].N_Al

			if p in [ "SLo", "SRo", "BLo", "BRo", "SUo", "SDo" ]:
				self.N_SiOH += 1
			#if p in [ "AU", "AD"]:
				#self.N_Al_Four += 1
			if p in [ "AUo", "ADo"]:
				self.N_AlOH += 1
				self.N_Al_Four += 1
			if p in [ "AUFo", "ADFo"]:
				self.N_AlOH += 2
				self.N_Al_Five += 1
			if p in [ "AUSo", "ADSo"]:
				self.N_AlOH += 4
				self.N_Al_Six += 1
			if p in [ "AIF"]:
				self.N_AlOH += 4
				self.N_Al_Five += 1
				self.N_Al_Five_inter +=1
			if p in [ "AIS"]:
				self.N_Al_Six += 1
				self.N_AlOH += 6
				self.N_Al_Six_inter += 1
			if p in [ "SLo", "SRo", "BLo", "BRo", "SL", "SR", "BL", "BR"]:
				self.N_braket += 1

			if p in [ "SU", "SUo", "SD", "SDo" ]:
				self.N_SUD += 1

			#if p in [ "AUo", "ADo", "AU", "AD", "AUFo", "ADFo", "AUSo", "ADSo"]:
				#self.N_AUD += 1
			if p in [ "AUo", "ADo", "AUFo", "ADFo", "AUSo", "ADSo"]:
				self.N_AUD += 1

			if p in incompatibility:
				for w in incompatibility[p]:
					self.excluded.add( w )

		self.elegible_water = np.array( sorted(list(list_water.difference(self.excluded) )) )




def above_layer():

	#bridging = [["SU"], ["SUo"], ["CU"], [None], ["AU"], ["AUo"], ["AUFo"], ["AUSo"]]
	bridging = [["SU"], ["SUo"], ["CU"], [None], ["AUo"], ["AUFo"], ["AUSo"]]
	combs_above = []
	for i_bridge in bridging:
		if i_bridge in [["SU"], ["SUo"]]:
			for oh_bridge in [ [None], ["oMUL"] ]:
				comb = ["SL"] + i_bridge + oh_bridge + ["SR"]
				combs_above.append( [x for x in comb if x is not None] )
		#if i_bridge in [["AU"], ["AUo"], ["AUFo"], ["AUSo"]]:
		if i_bridge in [ ["AUo"], ["AUFo"], ["AUSo"]]:
			for oh_bridge in [ [None], ["oMUL"] ]:
				comb = ["SL"] + i_bridge + oh_bridge + ["SR"]
				combs_above.append( [x for x in comb if x is not None] )

		if i_bridge == [None]:
			for i_left in [["SL"], ["SLo"]]:
				for i_right in  [["SR"], ["SRo"]]:
					comb = i_left + i_right
					combs_above.append(comb)

		if i_bridge == ["CU"]:
			for i_left in [["SL"], ["SLo"]]:
				for i_right in  [["SR"], ["SRo"]]:
					for oh_bridge_1 in [ [None], ["oMUL"] ]:
						for oh_bridge_2 in [ [None], ["oMUR"] ]:
							comb = i_left + i_bridge + oh_bridge_1 + oh_bridge_2 + i_right

							combs_above.append( [x for x in comb if x is not None] )

	return combs_above


def below_layer():

	#bridging = [["SD"], ["SDo"], ["CD"], [None], ["AD"], ["ADo"], ["ADFo"], ["ADSo"]]
	bridging = [["SD"], ["SDo"], ["CD"], [None],["ADo"], ["ADFo"], ["ADSo"]]
	combs_below = []
	for i_bridge in bridging:

		if i_bridge in [["SD"], ["SDo"]]:
			for oh_bridge in [ [None], ["oMDL"] ]:
				comb = ["BL"] + i_bridge + oh_bridge + ["BR"]
				combs_below.append( [x for x in comb if x is not None] )

		#if i_bridge in [["AD"], ["ADo"], ["ADFo"], ["ADSo"]]:
		if i_bridge in [ ["ADo"], ["ADFo"], ["ADSo"]]:
			for oh_bridge in [ [None], ["oMDL"] ]:
				comb = ["BL"] + i_bridge + oh_bridge + ["BR"]
				combs_below.append( [x for x in comb if x is not None] )

		if i_bridge == [None]:
			for i_left in [["BL"], ["BLo"]]:
				for i_right in  [["BR"], ["BRo"]]:
					comb = i_left + i_right
					combs_below.append(comb)

		if i_bridge == ["CD"]:
			for i_left in [["BL"], ["BLo"]]:
				for i_right in  [["BR"], ["BRo"]]:
					for oh_bridge_1 in [ [None], ["oMDL"] ]:
						for oh_bridge_2 in [ [None], ["oMDR"] ]:
							comb = i_left + i_bridge + oh_bridge_1 + oh_bridge_2 + i_right

							combs_below.append( [x for x in comb if x is not None] )		

	return combs_below



def interlayer():
	inter_Ca_1 = ["AIF","AIS",None, "CII"]
	inter_Ca_2 = [None, "XU"]
	inter_Ca_3 = [None, "XD"]
	inter_Ca_4 = [None, "CID"]
	inter_Ca_5 = [None, "CIU"]

	inter_OH_1 = [None, "oDL"]
	inter_OH_2 = [None, "oDR"]
	inter_OH_3 = [None, "oUL"]
	inter_OH_4 = [None, "oUR"]

	combs_inter = []

	for i_Ca_1 in inter_Ca_1:
		for i_Ca_2 in inter_Ca_2:
			for i_Ca_3 in inter_Ca_3:
				for i_Ca_4 in inter_Ca_4:
					for i_Ca_5 in inter_Ca_5:

						for i_OH_1 in inter_OH_1:
							for i_OH_2 in inter_OH_2:
								for i_OH_3 in inter_OH_3:
									for i_OH_4 in inter_OH_4:

										comb = [i_Ca_1, i_Ca_2, i_Ca_3, i_Ca_4, i_Ca_5,
										        i_OH_1, i_OH_2, i_OH_3, i_OH_4]


										inter_OH_5 = [None]
										if i_Ca_2 == "XU": inter_OH_5.append("oXU")
										if i_Ca_3 == "XD": inter_OH_5.append("oXD")

										# if i_Ca_2 == "XU" or i_Ca_3 == "XD":
										# 	print(inter_OH_5)

										for i_OH_5 in inter_OH_5:

											comb1 = [i for i in comb]
											comb1.append(i_OH_5)
											comb1 = [x for x in comb1 if x is not None]
											combs_inter.append(comb1)

	return combs_inter




def check_restrictions(comb):
	satisfy = True
	if "SD" in comb or "SDo" in comb:
		if "oMDR" in comb or "oDR" in comb :
			satisfy =  False
	if "SU" in comb or "SUo" in comb:
		if "oMUR" in comb or "oUL" in comb :
			satisfy =  False
	#if "AD" in comb or "ADo" in comb or "ADFo" in comb or "ADSo" in comb:
	if  "ADo" in comb or "ADFo" in comb or "ADSo" in comb:
		if "oMDR" in comb or "oDR" in comb:
			satisfy = False

	#if "AU" in comb or "AUo" in comb or "AUFo" in comb or "AUSo" in comb:
	if "AUo" in comb or "AUFo" in comb or "AUSo" in comb:
		if "oMUR" in comb or "oUL" in comb :
			satisfy =  False

	if "AIF" in comb or "AIS" in comb :
		if "AD" in comb or "ADo" in comb or "ADFo" in comb or "ADSo" in comb or "SD" in comb or "SDo" in comb or "CD" in comb or "oDR" in comb:
			satisfy =  False

#	if "SD" in comb or "SDo" in comb:
#		if "AD" in comb or "ADo" in comb :
#			satisfy =  False
#	if "SU" in comb or "SUo" in comb:
#		if "AU" in comb or "AUo" in comb :
#			satisfy =  False

	return satisfy




def get_all_bricks(pieces):
	combs_above = above_layer()
	combs_below = below_layer()
	combs_inter = interlayer()

	combs = []
	for i_above in combs_above:
		for i_inter in combs_inter:
			for i_below in combs_below:
				comb = i_above + i_inter + i_below

				if check_restrictions(comb):
					combs.append(comb)

	random.shuffle(combs)


	sorted_bricks = {}

	bricks = []

	ind = 0
	for i_comb in combs:
		b = Brick(i_comb, pieces, ind)

		Ca_Si = round( b.N_Ca/b.N_Si, 15 )
		Al_Si = round( b.N_Al/b.N_Si, 15 )

		Q     = b.charge

		SiOH = round( b.N_SiOH/b.N_Si, 4)
		if b.N_Al !=0:
			AlOH = round(b.N_AlOH / b.N_Al, 4)
			Al_Four = round(b.N_Al_Four / b.N_Al, 4)
			Al_Five = round(b.N_Al_Five / b.N_Al, 4)
			Al_Six = round(b.N_Al_Six / b.N_Al, 4)
		else:
			AlOH = 0
			Al_Four = 0
			Al_Five =0
			Al_Six = 0
		CaOH = round( (b.N_Oh - b.N_SiOH -b.N_AlOH)/b.N_Ca, 4)
		N_Al_Four = b.N_Al_Four
		N_Al_Five = b.N_Al_Five
		N_Al_Six = b.N_Al_Six
		N_Al_Five_inter = b.N_Al_Five_inter
		N_Al_Six_inter = b.N_Al_Six_inter
		if abs(Q) < 3:
			bricks.append(b)
			if N_Al_Five_inter in sorted_bricks:
				if N_Al_Six_inter in sorted_bricks[N_Al_Five_inter]:
					if N_Al_Four in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter]:
						if N_Al_Five in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four]:
							if N_Al_Six in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five]:
								if Ca_Si in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six]:
									if Q in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si]:
										if SiOH in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q]:
											if CaOH in sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q][SiOH]:
												sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q][SiOH][CaOH].append(b)
											else:
												sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q][SiOH][CaOH] = [b]
										else:
											sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q][SiOH] = {CaOH: [b]}
									else:
										sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si][Q] = {SiOH: {CaOH: [b]}}
								else:
									sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six][Ca_Si] = {Q: {SiOH: {CaOH: [b]}}}
							else:
								sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five][N_Al_Six] = {Ca_Si: {Q: {SiOH: {CaOH: [b]}}}}
						else:
							sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four][N_Al_Five] = {N_Al_Six: {Ca_Si: {Q: {SiOH: {CaOH: [b]}}}}}
					else:
						sorted_bricks[N_Al_Five_inter][N_Al_Six_inter][N_Al_Four] = {N_Al_Five: {N_Al_Six: {Ca_Si: {Q: {SiOH: {CaOH: [b]}}}}}}
				else:
					sorted_bricks[N_Al_Five_inter][N_Al_Six_inter] = {N_Al_Four: {N_Al_Five: {N_Al_Six: {Ca_Si: {Q: {SiOH: {CaOH: [b]}}}}}}}
			else:
				sorted_bricks[N_Al_Five_inter]= {N_Al_Six_inter: {N_Al_Four: {N_Al_Five: {N_Al_Six: {Ca_Si: {Q: {SiOH: {CaOH: [b]}}}}}}}}
		ind += 1


	return bricks, sorted_bricks


