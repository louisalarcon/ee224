* Active Butterworth LPF N=5 f0=10MHz
* LPA 14-Apr-2021


**************************************
* integrator core subcircuit
* - differential amplifier with feedback capacitors
* - note the labels of the pos and neg terminals
* - this is a non-inverting integrator
**************************************
.subckt integcore vop von vip vin Cint=1
Eamp	vop von vip vin		-1e6
Cpp		vop vin				{Cint}
Cpn		von vip				{Cint}
.ends

**************************************
* two-input integrator
**************************************
.subckt integ2 vop von v1p v1n v2p v2n Cint=1 R1=1 R2=1
X1		vop von vip vin 	integcore Cint={Cint}
R1p		v1p vip				{R1}
R1n		v1n vin				{R1}
R2p		v2p vip				{R2}
R2n		v2n vin				{R2}
.ends

**************************************
* three-input integrator
**************************************
.subckt integ3 vop von v1p v1n v2p v2n v3p v3n Cint=1 R1=1 R2=1 R3=1
X1		vop von vip vin 	integcore Cint={Cint}
R1p		v1p vip				{R1}
R1n		v1n vin				{R1}
R2p		v2p vip				{R2}
R2n		v2n vin				{R2}
R3p		v3p vip				{R3}
R3n		v3n vin				{R3}
.ends

**************************************
* single-ended to differential conversion
* - uses vcvs, not an actual balun -- not to be used for impedance measurements
**************************************
.subckt se2d vp vn vdm vcm
E1		vp vcm vdm 0	0.5
E2		vcm vn	vdm 0	0.5
.ends

* scaling each integrator output node to 0 dB
.param a=1.0320 b=1.2166 c=1.5589 d=1.8610 e=2

* noise scaling from 2uV to 150uV
.param g=5625.0

* integrator instantiations
* note the polarities are switched for negative inputs
X1		v2p v2n v2n v2p v3n v3p vip vin		integ3 Cint={9.836n/g} R1={1*g/a} R2={1*g*b/a} R3={1*g/a}
X2		v3p v3n	v2p v2n v4n v4p				integ2 Cint={25.75n/g} R1={1*g*a/b} R2={1*g*c/b} 
X3		v4p v4n	v3p v3n	v5n v5p				integ2 Cint={31.83n/g} R1={1*g*b/c} R2={1*g*d/c} 
X4		v5p v5n	v4p v4n	von vop				integ2 Cint={25.75n/g} R1={1*g*c/d} R2={1*g*e/d} 
X5		vop von	v5p v5n	von vop				integ2 Cint={9.836n/g} R1={1*g*d/e} R2={1*g*e/e} 

* create differential inputs from the single-ended source
Xb1		vip vin 1 0 		se2d
Vi		1 0					dc 0 ac 1

.control

ac dec 1000 3meg 40meg
wrdata butter5_active_norm3.dat v(vop)-v(von) v(v2p)-v(v2n) v(v3p)-v(v3n) v(v4p)-v(v4n) v(v5p)-v(v5n)

noise v(vop, von) Vi dec 100 1 1G
print onoise_total

.endc

.end