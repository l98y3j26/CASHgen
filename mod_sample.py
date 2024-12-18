import numpy as np
import random


def random_round(value):
	lower = int(value)
	upper = lower + 1
	return random.choice([lower, upper])

def sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, Al_Si_ratio, Al_Four, Al_Five, Al_Six,Al_Five_inter,Al_Six_inter,offset=[0.0, 0.0, 0.0]):
	width_Ca_Si = widths[0]
	width_SiOH = widths[1]
	width_CaOH = widths[2]

	value_1=-2.083*Ca_Si_ratio**3+10.98*Ca_Si_ratio**2- 19.3*Ca_Si_ratio+15.91
	value = Al_Si_ratio * N_brick * value_1
	N_Al_Total = random_round(value)

	N_Al_Four_Total=int(round(N_Al_Total*Al_Four))

	N_Al_Five_Total=int(round(N_Al_Total*Al_Five))
	N_Al_Five_I = int(round(N_Al_Five_Total*Al_Five_inter))


	N_Al_Six_Total=int(N_Al_Total-N_Al_Four_Total-N_Al_Five_Total)
	N_Al_Six_I = int(round(N_Al_Six_Total * Al_Six_inter))



	brick_Ca_Si = 0.0
	brick_Q = 0.0
	brick_SiOH = 0.0
	brick_CaOH = 0.0

	crystal = []  # _rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	N_Si = 0
	N_Ca = 0
	N_SiO = 0
	N_SiOH = 0
	N_Oh = 0

	N_braket = 0
	N_SUD = 0
	N_AUD = 0
	N_Al = 0
	N_AlO = 0
	N_AlOH = 0
	N_Al_Four = 0
	N_Al_Five = 0
	N_Al_Six = 0
	N_Al_Five_inter = 0
	N_Al_Six_inter = 0
	cont = 0
	while True:
		while len(crystal) != N_brick:
			if N_Al < N_Al_Total:
				if N_Al_Five_inter < N_Al_Five_I:

						key_N_Al_Five = 1
						key_N_Al_Four = 0

						key_N_Al_Six = 0

						keys_Ca_Si = np.array(list(sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six].keys()))
						u1 = np.random.normal(loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
											  scale=width_Ca_Si)
						ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
						key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

						keys_Q = np.array(list(sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si].keys()))
						u2 = np.random.normal(loc=0.0, scale=1.0)
						ind_Q = np.argmin(np.abs(keys_Q - u2))
						key_Q = keys_Q[ind_Q]

						keys_SiOH = np.array(
							list(sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q].keys()))
						u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
						ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
						key_SiOH = keys_SiOH[ind_SiOH]

						keys_CaOH = np.array(list(
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH].keys()))
						# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2], scale=width_CaOH)
						u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
						ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
						key_CaOH = keys_CaOH[ind_CaOH]

						#if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
						ind = np.random.randint(len(
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH]))

						crystal.append(
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][ind])

						N_Ca += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Ca
						N_Si += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Si
						N_SiO += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_SiO
						N_SiOH += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_SiOH
						N_Oh += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Oh

						N_AUD += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_AUD
						N_Al += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Al
						N_AlO += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_AlO
						N_AlOH += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_AlOH
						N_Al_Four += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Al_Four
						N_Al_Five += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Al_Five
						N_Al_Six += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_Al_Six
						N_Al_Five_inter += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][ind].N_Al_Five_inter
						N_Al_Six_inter += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][ind].N_Al_Six_inter
						N_braket += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_braket
						N_SUD += \
							sorted_bricks[1][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
								key_CaOH][
								ind].N_SUD

						brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
						brick_Q += keys_Q[ind_Q]
						brick_SiOH += keys_SiOH[ind_SiOH]
						brick_CaOH += keys_CaOH[ind_CaOH]
				else:
					if N_Al_Six_inter < N_Al_Six_I:
							key_N_Al_Four = 0
							key_N_Al_Five = 0
							key_N_Al_Six = 1

							keys_Ca_Si = np.array(
								list(sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six].keys()))
							u1 = np.random.normal(loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
												  scale=width_Ca_Si)
							ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
							key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

							keys_Q = np.array(
								list(sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si].keys()))
							u2 = np.random.normal(loc=0.0, scale=1.0)
							ind_Q = np.argmin(np.abs(keys_Q - u2))
							key_Q = keys_Q[ind_Q]

							keys_SiOH = np.array(
								list(sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][
										 key_Q].keys()))
							u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
							ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
							key_SiOH = keys_SiOH[ind_SiOH]

							keys_CaOH = np.array(list(
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH].keys()))
							# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2], scale=width_CaOH)
							u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
							ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
							key_CaOH = keys_CaOH[ind_CaOH]

							#if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
							ind = np.random.randint(len(
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH]))

							crystal.append(
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][ind])

							N_Ca += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][key_CaOH][
									ind].N_Ca
							N_Si += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][key_CaOH][
									ind].N_Si
							N_SiO += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][key_CaOH][
									ind].N_SiO
							N_SiOH += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][key_CaOH][
									ind].N_SiOH
							N_Oh += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][key_CaOH][
									ind].N_Oh

							N_AUD += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_AUD
							N_Al += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_Al
							N_AlO += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_AlO
							N_AlOH += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_AlOH
							N_Al_Four += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_Al_Four
							N_Al_Five += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_Al_Five
							N_Al_Six += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_Al_Six
							N_Al_Five_inter += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][ind].N_Al_Five_inter
							N_Al_Six_inter += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][ind].N_Al_Six_inter
							N_braket += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_braket
							N_SUD += \
								sorted_bricks[0][1][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH][
									key_CaOH][
									ind].N_SUD

							brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
							brick_Q += keys_Q[ind_Q]
							brick_SiOH += keys_SiOH[ind_SiOH]
							brick_CaOH += keys_CaOH[ind_CaOH]
					else:
						if N_Al_Four < N_Al_Four_Total:
							# way1
							if N_Al_Four < (N_Al_Four_Total - 1):

								key_N_Al_Four = random.choice([1, 2])
							else:
								key_N_Al_Four = random.choice([1])
							# way2
							# key_N_Al_Four = random.choice([1, 2])

							if N_Al_Five < N_Al_Five_Total:
								keys_N_Al_Five = np.array(list(sorted_bricks[0][0][key_N_Al_Four].keys()))
								key_N_Al_Five = random.choice(keys_N_Al_Five)
								# N_Al_Five += key_N_Al_Five
								if N_Al_Six < N_Al_Six_Total:
									keys_N_Al_Six = np.array(list(sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five].keys()))
									key_N_Al_Six = random.choice(keys_N_Al_Six)
								# N_Al_Six += key_N_Al_Six
								else:
									key_N_Al_Six = 0
							else:
								key_N_Al_Six = 0
								key_N_Al_Five = 0
							keys_Ca_Si = np.array(
								list(sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six].keys()))
							u1 = np.random.normal(loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
												  scale=width_Ca_Si)
							ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
							key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

							keys_Q = np.array(
								list(sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si].keys()))
							u2 = np.random.normal(loc=0.0, scale=1.0)
							ind_Q = np.argmin(np.abs(keys_Q - u2))
							key_Q = keys_Q[ind_Q]

							keys_SiOH = np.array(list(
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q].keys()))
							u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
							ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
							key_SiOH = keys_SiOH[ind_SiOH]

							keys_CaOH = np.array(list(
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
									key_SiOH].keys()))
							# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2], scale=width_CaOH)
							u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
							ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
							key_CaOH = keys_CaOH[ind_CaOH]

							if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
								ind = np.random.randint(len(
									sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
										key_SiOH][key_CaOH]))

								crystal.append(
									sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
										key_SiOH][key_CaOH][ind])

								N_Ca += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Ca
								N_Si += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Si
								N_SiO += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_SiO
								N_SiOH += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_SiOH
								N_Oh += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Oh

								N_AUD += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_AUD
								N_Al += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Al
								N_AlO += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_AlO
								N_AlOH += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_AlOH
								N_Al_Four += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Al_Four
								N_Al_Five += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Al_Five
								N_Al_Six += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_Al_Six

								N_braket += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_braket
								N_SUD += \
								sorted_bricks[0][0][key_N_Al_Four][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
									key_CaOH][ind].N_SUD

								brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
								brick_Q += keys_Q[ind_Q]
								brick_SiOH += keys_SiOH[ind_SiOH]
								brick_CaOH += keys_CaOH[ind_CaOH]

						else:
							if N_Al_Five < N_Al_Five_Total:
								# way1
								if N_Al_Five < (N_Al_Five_Total - 1):
									key_N_Al_Five = random.choice([1, 2])
								else:
									key_N_Al_Five = random.choice([1])
								# way2
								# key_N_Al_Five = random.choice([1,2])

								if N_Al_Six < N_Al_Six_Total:
									keys_N_Al_Six = np.array(list(sorted_bricks[0][0][0][key_N_Al_Five].keys()))
									key_N_Al_Six = random.choice(keys_N_Al_Six)
								else:
									key_N_Al_Six = 0

								keys_Ca_Si = np.array(list(sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six].keys()))
								u1 = np.random.normal(
									loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
									scale=width_Ca_Si)
								ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
								key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

								keys_Q = np.array(
									list(sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si].keys()))
								u2 = np.random.normal(loc=0.0, scale=1.0)
								ind_Q = np.argmin(np.abs(keys_Q - u2))
								key_Q = keys_Q[ind_Q]

								keys_SiOH = np.array(
									list(sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q].keys()))
								u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
								ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
								key_SiOH = keys_SiOH[ind_SiOH]

								keys_CaOH = np.array(list(
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][
										key_SiOH].keys()))
								# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2], scale=width_CaOH)
								u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
								ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
								key_CaOH = keys_CaOH[ind_CaOH]

								if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
									ind = np.random.randint(len(
										sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
											key_CaOH]))

									crystal.append(
										sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][
											key_CaOH][ind])

									N_Ca += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Ca
									N_Si += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Si
									N_SiO += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SiO
									N_SiOH += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SiOH
									N_Oh += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Oh

									N_AUD += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AUD
									N_Al += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al
									N_AlO += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AlO
									N_AlOH += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AlOH
									N_Al_Four += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Four
									N_Al_Five += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Five
									N_Al_Six += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Six

									N_braket += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_braket
									N_SUD += \
									sorted_bricks[0][0][0][key_N_Al_Five][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SUD

									brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
									brick_Q += keys_Q[ind_Q]
									brick_SiOH += keys_SiOH[ind_SiOH]
									brick_CaOH += keys_CaOH[ind_CaOH]
							else:
								if N_Al_Six < N_Al_Six_Total:
									# way1
									if N_Al_Six < (N_Al_Six_Total - 1):
										key_N_Al_Six = random.choice([1, 2])
									else:
										key_N_Al_Six = random.choice([1])
								# way2
								# key_N_Al_Six = random.choice([1,2])
								else:
									key_N_Al_Six = 0

								keys_Ca_Si = np.array(list(sorted_bricks[0][0][0][0][key_N_Al_Six].keys()))
								u1 = np.random.normal(
									loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
									scale=width_Ca_Si)
								ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
								key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

								keys_Q = np.array(
									list(sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si].keys()))
								u2 = np.random.normal(loc=0.0, scale=1.0)
								ind_Q = np.argmin(np.abs(keys_Q - u2))
								key_Q = keys_Q[ind_Q]

								keys_SiOH = np.array(
									list(sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q].keys()))
								u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
								ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
								key_SiOH = keys_SiOH[ind_SiOH]

								keys_CaOH = np.array(list(
									sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][
										key_SiOH].keys()))
								# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2], scale=width_CaOH)
								u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
								ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
								key_CaOH = keys_CaOH[ind_CaOH]

								if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
									ind = np.random.randint(
										len(sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH]))

									crystal.append(
										sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind])

									N_Ca += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Ca
									N_Si += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Si
									N_SiO += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SiO
									N_SiOH += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SiOH
									N_Oh += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Oh

									N_AUD += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AUD
									N_Al += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al
									N_AlO += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AlO
									N_AlOH += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_AlOH
									N_Al_Four += \
									sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Four
									N_Al_Five += \
									sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Five
									N_Al_Six += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_Al_Six

									N_braket += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_braket
									N_SUD += sorted_bricks[0][0][0][0][key_N_Al_Six][key_Ca_Si][key_Q][key_SiOH][key_CaOH][
										ind].N_SUD

									brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
									brick_Q += keys_Q[ind_Q]
									brick_SiOH += keys_SiOH[ind_SiOH]
									brick_CaOH += keys_CaOH[ind_CaOH]
			else:

				keys_Ca_Si = np.array(list(sorted_bricks[0][0][0][0][0].keys()))
				u1 = np.random.normal(loc=Ca_Si_ratio + Ca_Si_stepper(Ca_Si_ratio, brick_Ca_Si, crystal),
									  scale=width_Ca_Si)
				ind_Ca_Si = np.argmin(np.abs(keys_Ca_Si - u1))
				key_Ca_Si = keys_Ca_Si[ind_Ca_Si]

				keys_Q = np.array(
					list(sorted_bricks[0][0][0][0][0][key_Ca_Si].keys()))
				u2 = np.random.normal(loc=0.0, scale=1.0)
				ind_Q = np.argmin(np.abs(keys_Q - u2))
				key_Q = keys_Q[ind_Q]

				keys_SiOH = np.array(
					list(sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q].keys()))
				u3 = np.random.normal(loc=exp_SiOH(key_Ca_Si) + offset[0], scale=width_SiOH)
				ind_SiOH = np.argmin(np.abs(keys_SiOH - u3))
				key_SiOH = keys_SiOH[ind_SiOH]

				keys_CaOH = np.array(list(
					sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][
						key_SiOH].keys()))
				# u4 = np.random.normal(loc=exp_CaOH_stepper(Ca_Si_ratio, brick_CaOH, crystal) + offset[2],scale=width_CaOH)
				u4 = np.random.normal(loc=exp_CaOH(key_Ca_Si) + offset[1], scale=width_CaOH)
				ind_CaOH = np.argmin(np.abs(keys_CaOH - u4))
				key_CaOH = keys_CaOH[ind_CaOH]

				if abs(key_Q - u2) < 1.0 and abs(key_SiOH - u3) < 0.3 and abs(key_CaOH - u4) < 0.3:
					ind = np.random.randint(len(sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH]))
					crystal.append(sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind])

					N_Ca += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Ca
					N_Si += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Si
					N_SiO += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SiO
					N_SiOH += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SiOH
					N_Oh += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Oh

					N_AUD += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_AUD
					N_Al += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Al
					N_AlO += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_AlO
					N_AlOH += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_AlOH
					N_Al_Four += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Al_Four
					N_Al_Five += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Al_Five
					N_Al_Six += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Al_Six

					N_braket += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_braket
					N_SUD += sorted_bricks[0][0][0][0][0][key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SUD

					brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
					brick_Q += keys_Q[ind_Q]
					brick_SiOH += keys_SiOH[ind_SiOH]
					brick_CaOH += keys_CaOH[ind_CaOH]















		if brick_Q == 0:
			list_elegible_water = np.array([len(crystal[i_brick].elegible_water) for i_brick in range(N_brick)])
			N_water = int(np.rint(N_Si * W_Si_ratio))
			r_2H_Si = W_Si_ratio + 0.5 * N_Oh / N_Si

			if np.sum(list_elegible_water) >= N_water:
				break
			elif np.sum(list_elegible_water) >= N_water - 1:
				N_water -= 1
				break
			else:
				brick_Ca_Si = 0.0
				brick_Q = 0.0
				brick_Al_Si = 0.0
				crystal = []  # _rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]
				N_Si = 0
				N_Ca = 0
				N_SiOH = 0
				N_SiO = 0
				N_braket = 0
				N_SUD = 0
				N_Oh = 0

				N_AUD = 0
				N_Al = 0
				N_AlO = 0
				N_AlOH = 0
				N_Al_Four = 0
				N_Al_Five = 0
				N_Al_Six = 0
				N_Al_Five_inter = 0
				N_Al_Six_inter = 0
				cont += 1

				if cont >= 5000:
					print("Could not find any structure")
					break

		else:
			brick_Ca_Si = 0.0
			brick_Al_Si = 0.0
			brick_Q = 0.0
			crystal = []  # _rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]
			N_Si = 0
			N_Ca = 0
			N_SiOH = 0
			N_SiO = 0
			N_braket = 0
			N_SUD = 0
			N_Oh = 0
			N_AUD = 0
			N_Al = 0
			N_AlO = 0
			N_AlOH = 0
			N_Al_Four = 0
			N_Al_Five = 0
			N_Al_Six = 0
			N_Al_Five_inter = 0
			N_Al_Six_inter = 0
			cont += 1

			if cont >= 5000:
				print("Could not find any structure")
				break

	r_SiOH = N_SiOH / N_Si
	r_CaOH = (N_Oh - N_SiOH - N_AlOH) / N_Ca
	if N_Al!=0:
		r_AlOH = N_AlOH / N_Al
	else:
		r_AlOH = 0
	if N_braket != 2 * (N_SUD + N_AUD):
		MCL = (N_braket + N_SUD + N_AUD) / (0.5 * N_braket - N_SUD - N_AUD)
	else:
		MCL = 0

	return crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_Al, r_AlOH, N_Al_Four, N_Al_Five, N_Al_Six, N_water, r_2H_Si


def exp_SiOH(Ca_Si):
	return 0.82 - 0.43 * Ca_Si


# return (15-7*Ca_Si)/16

def exp_CaOH(Ca_Si):
	return -0.6 + 0.65 * Ca_Si
def exp_CaOH_stepper(Ca_Si_ratio,brick_CaOH,crystal):
	if len(crystal) == 0:
		return -0.6 + 0.65 * Ca_Si_ratio
	else:
		return 2*(-0.6 + 0.65 * Ca_Si_ratio)-brick_CaOH/(len(crystal))

# return (5*Ca_Si-4)/9



def Ca_Si_stepper(Ca_Si_ratio,brick_Ca_Si,crystal):
	if len(crystal) == 0:
		return 0
	else:
		#return 0
		return Ca_Si_ratio-brick_Ca_Si/(len(crystal))





def fill_water(crystal, N_water):
	N_brick = len(crystal)
	water_distr = np.zeros(N_brick, dtype=int)

	N_elegible_brick = N_brick
	N_left = N_water
	list_elegible_water = np.array([len(crystal[i_brick].elegible_water) for i_brick in range(N_brick)])
	list_elegible_brick = np.array([True for i in range(N_brick)])

	while N_left != 0:
		aux = (list_elegible_water - water_distr) * list_elegible_brick
		N_try = np.min(aux[np.nonzero(aux)])

		if N_try * N_elegible_brick <= N_left:
			add = np.ones(N_brick, dtype=int) * N_try * list_elegible_brick

			water_distr += add

			N_left = N_water - np.sum(water_distr)
			list_elegible_brick = water_distr < list_elegible_water
			N_elegible_brick = np.sum(list_elegible_brick)


		else:
			for i in range(N_brick):
				if list_elegible_brick[i]:
					water_distr[i] += 1
					N_left -= 1

					if N_left == 0:
						break

	# Fill each brick
	water_in_crystal = []
	for i_brick in range(N_brick):
		aux = np.random.choice(crystal[i_brick].elegible_water, size=water_distr[i_brick], replace=False)

		water_in_crystal.append(list(aux))

	return water_in_crystal

def get_offset(N_samples, sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, Al_Si_ratio, Al_Four, Al_Five, Al_Six):
	aux_SiOH = np.zeros(N_samples)
	aux_CaOH = np.zeros(N_samples)
	aux_MCL = np.zeros(N_samples)

	for isample in range(N_samples):
		ccrystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_Al,_,_,_,_,_,_ = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, Al_Si_ratio, Al_Four, Al_Five, Al_Six)

		aux_SiOH[isample] = r_SiOH
		aux_CaOH[isample] = r_CaOH
		aux_MCL[isample]  = MCL


	return exp_SiOH(Ca_Si_ratio)-np.mean(aux_SiOH), exp_CaOH(Ca_Si_ratio)-np.mean(aux_CaOH)
