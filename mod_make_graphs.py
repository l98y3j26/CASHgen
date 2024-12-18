from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

def exp_SiOH(Ca_Si):
	return  0.82 -0.43*Ca_Si

def exp_CaOH(Ca_Si):
	return -0.6 + 0.65*Ca_Si

def exp_MCL(Ca_Si):
	return 1.8*Ca_Si/(Ca_Si-0.69)


def plot_XOH_X(list_properties):

	transp = 0.5
	lw = 2
	colors = [ "#360568", 
		   "#4281A4", 
		   "#7FC29B", 
		   "#DBAD6A", 
		   "#A4243B", 
		   "#898989",
		   "#7D387D",
		   "#78290F" ]

	x_Ca_Si = np.linspace(0.8, 2.2,100)
	y_CaOH  = exp_CaOH(x_Ca_Si)
	y_SiOH  = exp_SiOH(x_Ca_Si)

	plt.plot( x_Ca_Si, y_CaOH, "--", color=colors[0], alpha=1, label="Ca-OH/Ca (exp)", lw=lw )
	plt.plot( x_Ca_Si, y_SiOH, "--", color=colors[1], alpha=1, label="Si-OH/Si (exp)", lw=lw )

	plt.scatter( list_properties[:,0], list_properties[:,2], color=colors[2], alpha=transp, label="Ca-OH/Ca" )
	plt.scatter( list_properties[:,0], list_properties[:,1], color=colors[3], alpha=transp, label="Si-OH/Si" )


	plt.xlabel('Ca/Si', fontsize=14)
	plt.ylabel('X-OH/X', fontsize=14)
	plt.legend()

	plt.xlim((0.8, 2.2))
	plt.ylim((0, 1))

	plt.tick_params(labelsize=12)

	plt.tight_layout()
	#plt.show()
	plt.savefig( "XOX_X.pdf" )
	plt.clf()


def plot_MCL(list_properties,Al_Si_ratio):
	plt.figure(figsize=(7,5))
	transp = 0.5
	lw = 2
	colors = [ "#360568", 
		   "#4281A4", 
		   "#7FC29B", 
		   "#DBAD6A", 
		   "#A4243B", 
		   "#898989",
		   "#7D387D",
		   "#78290F" ]

	x_Ca_Si = np.linspace(0.8, 2.2,500)
	y_MCL  = MCL_function(x_Ca_Si, Al_Si_ratio)

	plt.plot( x_Ca_Si, y_MCL, "--", color=colors[0], alpha=1, label="MCL (exp)", lw=lw )

	plt.scatter( list_properties[:,0], list_properties[:,3], color=colors[1], alpha=transp, label="MCL (CASHgen)" )


	plt.xlabel('Ca/Si', fontsize=14)
	plt.ylabel('MCL', fontsize=14)
	plt.legend()

	plt.xlim((0.8, 2.2))
	plt.ylim(2, 15)
	plt.tick_params(labelsize=12)

	plt.tight_layout()
	#plt.show()
	plt.savefig( "MCL.pdf" )
	plt.clf()


def smear_distr(Y, width):

	Y_min = np.min(Y)
	Y_max = np.max(Y)
	X_plot = np.linspace(Y_min, Y_max, 1000)

	kde = KernelDensity(kernel="gaussian", bandwidth=width).fit(Y.reshape(-1, 1))
	Y_plot = np.exp(kde.score_samples(X_plot.reshape(-1, 1)))

	return X_plot, Y_plot



def plot_distributions(list_properties):
	transp = 0.8
	colors = ["#360568",
			  "#4281A4",
			  "#7FC29B",
			  "#DBAD6A",
			  "#A4243B",
			  "#898989",
			  "#7D387D",
			  "#78290F"]

	Nbins = 15

	# Open a PdfPages object to save multiple figures into one PDF file
	with PdfPages("distributions.pdf") as pdf:
		# First page: Plot the first 5 histograms in a 2x3 layout
		fig1, axes1 = plt.subplots(2, 3)  # Creating a 2x3 grid for the first page
		axes1[1][2].set_visible(False)  # Hiding the last empty subplot on the first page

		# Plot the first 5 properties on the first page
		axes1[0][0].hist(list_properties[:, 0], bins=Nbins, density=True, color=colors[0], alpha=transp)
		axes1[0][0].set_xlabel("Ca/Si")

		axes1[0][1].hist(list_properties[:, 1], bins=Nbins, density=True, color=colors[1], alpha=transp)
		axes1[0][1].set_xlabel("SiOH/Si")

		axes1[0][2].hist(list_properties[:, 2], bins=Nbins, density=True, color=colors[2], alpha=transp)
		axes1[0][2].set_xlabel("CaOH/Ca")

		axes1[1][0].hist(list_properties[:, 3], bins=Nbins, density=True, color=colors[3], alpha=transp)
		axes1[1][0].set_xlabel("MCL")

		axes1[1][1].hist(list_properties[:, 5], bins=Nbins, density=True, color=colors[4], alpha=transp)
		axes1[1][1].set_xlabel("2H/Si")

		plt.tight_layout()
		pdf.savefig(fig1)  # Save the first figure into the PDF
		plt.clf()  # Clear the figure for the next page

		# Second page: Plot the next 5 histograms in a 2x3 layout
		fig2, axes2 = plt.subplots(2, 3)  # Creating a 2x3 grid for the second page
		axes2[1][2].set_visible(False)  # Hiding the last empty subplot on the second page

		# Plot the next 5 properties on the second page
		axes2[0][0].hist(list_properties[:, 7], bins=Nbins, density=True, color=colors[0], alpha=transp)
		axes2[0][0].set_xlabel("Al/Si")

		axes2[0][1].hist(list_properties[:, 8], bins=Nbins, density=True, color=colors[1], alpha=transp)
		axes2[0][1].set_xlabel("Al_Four_ratio")

		axes2[0][2].hist(list_properties[:, 9], bins=Nbins, density=True, color=colors[2], alpha=transp)
		axes2[0][2].set_xlabel("Al_Five_ratio")

		axes2[1][0].hist(list_properties[:, 10], bins=Nbins, density=True, color=colors[3], alpha=transp)
		axes2[1][0].set_xlabel("Al_Six_ratio")

		axes2[1][1].hist(list_properties[:, 6], bins=Nbins, density=True, color=colors[4], alpha=transp)
		axes2[1][1].set_xlabel("AlOH/Al")

		plt.tight_layout()
		pdf.savefig(fig2)  # Save the second figure into the same PDF
		plt.clf()  # Clear the figure after saving



def plot_experimental():
	point_CaOH = np.array([[1.70,     0.4529 ],
					   [1.65,     0.4364 ],
					   [1.60,     0.3375 ],
					   [1.45,     0.3241 ],
					   [1.40,     0.3214 ],
					   [1.08,     0.1139 ],
					   [0.95,     0.0250 ],
					   [1.10,     0.1000 ],
					   [1.35,     0.2000 ],
					   [1.45,     0.3500 ],
					   [1.55,     0.6500 ],
					   [0.88,     0.0100 ],
					   [0.98,     0.0300 ],
					   [1.05,     0.0900 ],
					   [1.12,     0.0700 ],
					   [1.32,     0.2200 ],
					   [1.38,     0.4200 ],
					   [1.43,     0.3600 ]])

	point_SiOH = np.array( [
	    [  0.80,     0.4500 ],
	    [  0.90,     0.4000 ],
	    [  1.05,     0.3800 ],
	    [  1.35,     0.2600 ],
	    [  1.45,     0.2000 ],
	    [  1.55,     0.1000 ],
	    [  0.88,     0.4400 ],
	    [  0.98,     0.4100 ],
	    [  1.05,     0.3900 ],
	    [  1.12,     0.3800 ],
	    [  1.32,     0.2900 ],
	    [  1.38,     0.2200 ],
	    [  1.43,     0.2100 ],
	    [  1.57,     0.1400 ]
		] )

	point_MCL = np.array([
		[0.70,     18.6  ],
		[1.08,     7.1  ],
		[1.22,     5.0  ],
		[1.39,     3.9  ],
		[1.58,     3.5  ],
		[1.86,     3.2  ],
		[0.92,     9.2  ],
		[1.03,     6.1  ],
		[1.26,     3.0  ],
		[1.28,     2.9  ],
		[1.44,     2.6  ],
		[0.98, 		9.1  ],
		[1.16, 		3.5  ],
		[1.3,	 	2.55],
		[1.44, 		2.56  ],
		[1.61, 		3.9  ],
		[1.7,	 	2.3  ],
		[1.00, 		6.9  ],
		[1.25, 		3.6  ],
		[1.5, 		3.1  ],
		[1.76, 		2.6  ],
		[2.0,	 	2.3  ],
		[0.81, 		11.5  ],
		[1.0, 		3.7  ],
		[1.2, 		2.7  ],
		[1.5, 		2.4  ],
		[2.4,	 	2.4  ]] )

	list_CaSi = []
	list_SiOH = []
	list_CaOH = []
	list_MCL  = []

	transp = 1.0
	lw = 2
	colors = [ "#360568", 
	   "#4281A4", 
	   "#7FC29B", 
	   "#DBAD6A", 
	   "#A4243B", 
	   "#898989",
	   "#7D387D",
	   "#78290F" ]

	with open( "check_exp.dat", "r" ) as f:
		for line in f:
			aux = [ float(i) for i in line.split() ]
			list_CaSi.append( [aux[0], aux[1]] )
			list_SiOH.append( [aux[2], aux[3]] )
			list_CaOH.append( [aux[4], aux[5]] )
			list_MCL.append(  [aux[6], aux[7]] )

	list_CaSi = np.array(list_CaSi)
	list_SiOH = np.array(list_SiOH)
	list_CaOH = np.array(list_CaOH)
	list_MCL = np.array(list_MCL)


	x_Ca_Si = np.linspace(0.8, 2.2,100)
	y_CaOH  = exp_CaOH(x_Ca_Si)
	y_SiOH  = exp_SiOH(x_Ca_Si)



	plt.scatter( point_SiOH[:,0], point_SiOH[:,1], color=colors[0], alpha=transp, label="Si-OH/Si (exp)" )
	plt.scatter( point_CaOH[:,0], point_CaOH[:,1], color=colors[1], alpha=transp, label="Ca-OH/Ca (exp)" )

	plt.plot( x_Ca_Si, y_SiOH, "--", color=colors[0], alpha=transp, lw=lw )
	plt.plot( x_Ca_Si, y_CaOH, "--", color=colors[1], alpha=transp, lw=lw )

	plt.errorbar(list_CaSi[:,0], list_SiOH[:,0], xerr=list_CaSi[:,1], yerr=list_SiOH[:,1],
				 capsize=4, fmt=".", color=colors[2], alpha=transp, label="Si-OH/Si (CASHgen)")
	plt.errorbar(list_CaSi[:,0], list_CaOH[:,0], xerr=list_CaSi[:,1], yerr=list_CaOH[:,1],
				 capsize=4, fmt=".", color=colors[3], alpha=transp, label="Si-OH/Si (CASHgen)")



	plt.xlim((0.8, 2.1))
	plt.ylabel( "X-OH/X", fontsize=12 )
	plt.xlabel( "Si/Ca", fontsize=12 )

	plt.legend(loc="upper left", fontsize=12)

	plt.tight_layout()
	plt.savefig( "test_XOH_X.pdf" )

	plt.clf()



	plt.scatter( point_MCL[:,0], point_MCL[:,1], color=colors[0], alpha=transp, label="MCL (exp)" )
	plt.plot( x_Ca_Si, exp_MCL(x_Ca_Si), "--", color=colors[0], alpha=transp, lw=lw )
	plt.errorbar(list_CaSi[:,0], list_MCL[:,0], xerr=list_CaSi[:,1], yerr=list_MCL[:,1],
				 capsize=4, fmt=".", color=colors[2], alpha=transp, label="MCL (CASHgen)")
	plt.ylabel( "MCL" )

	plt.xlim((0.8, 2.2))
	plt.ylabel( "MCL", fontsize=12 )
	plt.xlabel( "Si/Ca", fontsize=12 )

	plt.legend(loc="upper right", fontsize=12)

	plt.tight_layout()
	plt.savefig( "test_MCL.pdf" )
	plt.clf()



def plot_water(list_properties):


	transp = 0.5
	lw = 2
	colors = [ "#360568", 
	   "#4281A4", 
	   "#7FC29B", 
	   "#DBAD6A", 
	   "#A4243B", 
	   "#898989",
	   "#7D387D",
	   "#78290F" ]


	point_Ca_Si  = np.array([1.85,1.77,1.56,1.39,1.06,0.97,1.7,1.54,1.45,1.32,1.19, 1.13, 0.88, 0.79,0.41])
	point_r_H_Si = np.array([2.072,2.071,1.747,1.4595,0.9964,0.8924,1.462,1.4322,1.2035,1.0164,0.9401,0.8701,0.7128,0.6873,0.4674])


	plt.scatter( point_Ca_Si, point_r_H_Si, color=colors[0], alpha=1, label="H/Si (exp)" )
	plt.scatter( list_properties[:,0], list_properties[:,5], color=colors[1], alpha=transp, label="H/Si (CASHgen)" )


	plt.xlabel( "Si/Ca", fontsize=12 )
	plt.ylabel( "2H/Si", fontsize=12 )


	plt.xlim((0.8, 2.1))

	plt.legend(loc="upper left", fontsize=12)

	plt.tight_layout()
	plt.savefig( "water.pdf" )
	plt.clf()







def improved_model(X, a, b, c, d, e, f):
    x, y = X
    return a * np.log(x) + b * (1/x) + c * np.exp(-d * y) + e * x * y + f


def MCL_function(Ca_Si, Al_Si):
    return improved_model((Ca_Si, Al_Si), 1.34920979e+01, 2.75018766e+01, 4.97052398e+03, -4.81237336e-03, 5.20547300e+00, -4.99141184e+03)




xx, yy = np.meshgrid(np.linspace(0.8, 2, 120), np.linspace(0, 0.25, 100))
zz = MCL_function(xx, yy)




#plt.tight_layout()
#plt.show()
