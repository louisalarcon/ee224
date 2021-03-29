* Butterworth LPF N=5 f0=10MHz
* LPA 24-Mar-2021

Rs		1 2		1
C1		2 0 	9.836n
L2 		2 3 	25.75n
C3		3 0		31.83n
L4		3 4		25.75n
C5		4 0		9.836n
RL		4 0 	1

Vi		1 0		dc 0 ac 1

.control

ac dec 1000 3meg 40meg
wrdata butter_lpf_5.dat v(4)

.endc

.end