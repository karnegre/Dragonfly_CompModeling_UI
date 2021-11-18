import numpy as np 


def r0(n_complex):
	#below eqn 8c, Shkuratov 1999
	return (n_complex.real-1)**2 / (n_complex.real +1)**2

def Re(n_complex):
	# eqn 8b, Shkuratov 1999
	return r0(n_complex)+0.05

def Rb(n_complex):
	# eqn 8a, Shkuratov 1999
	return (0.28*n_complex.real - 0.2)*Re(n_complex)

def Ri(n_complex):
	# eqn 7b, Shkuratov 1999
	return 1-(1-Re(n_complex))/n_complex.real**2

def Te(n_complex):
	return 1-Re(n_complex)

def Ti(n_complex):
	return Te(n_complex)/n_complex.real**2

def rb(tau,n_complex):
	# eqn 5a of Shkuratov 1999, assuming Wm=0.5 for m (number of scatterings)>2
	answer=0.5*Te(n_complex)*Ti(n_complex)*Ri(n_complex)*np.exp(-2*tau)
	answer/=(1-Ri(n_complex)*np.exp(-tau))
	answer += Rb(n_complex)
	return answer

def Rf(n_complex):
	return Re(n_complex)-Rb(n_complex)

def rf(tau,n_complex):
	# eqn 5b of Shkuratov 1999, assuming Wm=0.5 for m (number of scatterings)>2
	answer=0.5*Te(n_complex)*Ti(n_complex)*Ri(n_complex)*np.exp(-2*tau)/(1-Ri(n_complex)*np.exp(-tau))
	answer+= Te(n_complex)*Ti(n_complex)*np.exp(-tau)
	answer+=Rf(n_complex)
	return answer

# 	y /= 2*A
# def n_imag(n_complex,A,q,wave,S):
# 	y = (1-A)**2

# 	a=Te(n_complex)*Ti(n_complex)*(y*Ri(n_complex)+q*Te(n_complex))
# 	b=y*Rb(n_complex)*Ri(n_complex)+(q/2)*(1+Ti(n_complex))*Te(n_complex)**2 -Te(n_complex)*(1-q*Rb(n_complex))
# 	c=2*y*Rb(n_complex) - 2*Te(n_complex)*(1-q*Rb(n_complex))+q*Te(n_complex)**2

# 	answer = -wave/(4*np.pi*S)
# 	answer *= log(b/a + np.sqrt((b/a)**2 - c/a))
# 	return answer

def A_eqn12(rhob,rhof):
	# See eqn 12 of Shkuratov 1999

	A=0.
	A = 1+rhob**2-rhof**2
	A /= 2*rhob
	A -= np.sqrt(((1+rhob**2-rhof**2)/(2*rhob))**2 -1)
	return A

def shkuratov_albedo(n_complex,q,S,wavelength_um):
	# q is the volume fraction filled by particles
	tau=0.
	_rf=0.
	_rb=0.
	ssa=0.
	g=0
	rhob=0.
	rhof=0.
	A=0.

	tau=4*np.pi*n_complex.imag*S/wavelength_um


	_rf=rf(tau,n_complex)
	_rb=rb(tau,n_complex)

	## p. 316 of Poulet et al 2002, ssa assumption
	ssa=_rb+_rf

	## p. 317 of Poulet et al 2002, asymmetry parameter
	g=(_rf-_rb)/(_rf+_rb)

	## eq 10
	rhob=q*_rb
	rhof=q*_rf+1-q

	## eq 12
	A = A_eqn12(rhob,rhof)
	return ssa,A,g



def shkuratov_coarsemix(c,n_complex,q,S,wavelength_um):
	## see eqns 14, 12 of Shkuratov 1999
	## c is an array of concentration for mixture component
	## n is an array of the same length as c with the indecies of refraction
	## S is an array of the "particle size" parameter for mixture component
	rho_b=0.
	rho_f=0.
	answer=0.

	for ci,ni,Si in zip(c,n_complex,S):

		tau=4*np.pi*ni.imag*Si/wavelength_um

		rho_b+=ci*rb(tau,ni)
		rho_f+=ci*rf(tau,ni)

	rho_b*=q
	rho_f*=q
	rho_f+=(1-q)

	answer = A_eqn12(rho_b,rho_f)
	return answer


#def shkuratov_coarsemix
