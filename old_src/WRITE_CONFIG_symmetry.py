from math import *
import numpy as np
from time import strftime
import sys

if len(sys.argv) != 5:
    print "Arguments should be: sidelength, # of molecules and I1 and output file"
    sys.exit()
else:
    D = sys.argv[1]         # sidelength of simulation cubic box
    N = sys.argv[2]         # number of particles in the box
    I1 = sys.argv[3]        # declare the value of I1. Refer to Water Model
    filedirectory_to = sys.argv[4]

# create and open CONFIG file
fout = open(filedirectory_to,"w")

# write the header
fout.write('Configurations for symmetry water model '+'I1='+str(I1)+'  '+strftime("%Y-%m-%d %H:%H:%S")+'\n')

# write the levcfg and imcon key
# levcfg: 0 Coordinates included in file
#         1 Coordinates and velocities included in file
#         2 Coordinates, velocities and forces included in file
# imcon:  0 no periodic boundaries
#         1 cubic boundary conditions
#         2 orthorhombic boundary conditions
#         3 parallelepiped boundary conditions
#         4 truncated octahedral boundary conditions
#         5 rhombic dodecahedral boundary conditions
#         6 x-y parallelogram boundary conditions with no periodicity in the z direction
#         7 hexagonal prism boundary conditions
fout.write(str(0).rjust(10)+str(2).rjust(10)+"\n")

# write the simulation box cell vector
fout.write((str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+"\n")

# write the coordinates of SPC/E water atoms
# initially put all atoms approximately at the lattice points

l = ceil(N**(1./3.))       # total number of particles is 1000. 1000**(1/3)=10
small_D = D/l              # sidelength of a small cell
natm = 5

for n in range(1,N+1):
    fout.write("OW".ljust(8)+str((n-1)*3+1).rjust(10)+"\n")    # write the coordinate of oxygen atom
    k = ceil((float(n)/(int(l)**2)))
    temp = n-(k-1)*int(l)**2
    j = ceil(temp/l)
    i = temp - (j-1)*l
    x = -(j-1)*small_D + (D/2.0 - small_D/2.0)
    y = (i-1)*small_D + (-D/2.0 + small_D/2.0)
    z = -(k-1)*small_D + (D/2.0 - small_D/2.0)
    fout.write(("%.12f" % x).rjust(20)+("%.12f" % y).rjust(20)+("%.12f" % z).rjust(20)+"\n")
    # assign the zero initial velocities to each particles
    #fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")

    phi1 = 2*pi*np.random.random()
    phi2 = 2*pi*np.random.random()
    phi3 = 2*pi*np.random.random()

    x1 = I1*sin(phi2)+x
    y1 = -I1*cos(phi2)*sin(phi1)+y
    z1 = I1*cos(phi2)*cos(phi1)+z

    x2 = -(1./3.)*sqrt(2)*I1*cos(phi2)*cos(phi3)-(1./3.)*I1*sin(phi2)-sqrt(2./3.)*I1*cos(phi2)*sin(phi3)+x
    y2 = (1./3.)*I1*cos(phi2)*sin(phi1)-(1./3.)*sqrt(2)*I1*(cos(phi1)*sin(phi3)+cos(phi3)*sin(phi2)*sin(phi1))+sqrt(2./3.)*I1*(cos(phi3)*cos(phi1)-sin(phi2)*sin(phi3)*sin(phi1))+y
    z2 = -(1./3.)*I1*cos(phi2)*cos(phi1)+sqrt(2./3.)*I1*(cos(phi1)*sin(phi2)*sin(phi3)+cos(phi3)*sin(phi1))-(1./3.)*sqrt(2)*I1*(-cos(phi3)*cos(phi1)*sin(phi2)+sin(phi3)*sin(phi1))+z

    x3 = (2./3.)*sqrt(2)*I1*cos(phi2)*cos(phi3)-(1./3.)*I1*sin(phi2)+x
    y3 = (1./3.)*I1*cos(phi2)*sin(phi1)+(2./3.)*sqrt(2)*I1*(cos(phi1)*sin(phi3)+cos(phi3)*sin(phi2)*sin(phi1))+y
    z3 = -(1./3.)*I1*cos(phi2)*cos(phi1)+(2./3.)*sqrt(2)*I1*(-cos(phi3)*cos(phi1)*sin(phi2)+sin(phi3)*sin(phi1))+z

    x4 = -(1./3.)*sqrt(2)*I1*cos(phi2)*cos(phi3)-(1./3.)*I1*sin(phi2)+sqrt(2./3.)*I1*cos(phi2)*sin(phi3)+x
    y4 = (1./3.)*I1*cos(phi2)*sin(phi1)-(1./3.)*sqrt(2)*I1*(cos(phi1)*sin(phi3)+cos(phi3)*sin(phi2)*sin(phi1))-sqrt(2./3.)*I1*(cos(phi3)*cos(phi1)-sin(phi2)*sin(phi3)*sin(phi1))+y
    z4 = -(1./3.)*I1*cos(phi2)*cos(phi1)-sqrt(2./3.)*I1*(cos(phi1)*sin(phi2)*sin(phi3)+cos(phi3)*sin(phi1))-(1./3.)*sqrt(2)*I1*(-cos(phi3)*cos(phi1)*sin(phi2)+sin(phi3)*sin(phi1))+z

    # randomly put the Hydrogen atoms in the unit cell while keeping the structure right
    fout.write("HW".ljust(8)+str((n-1)*natm+2).rjust(10)+"\n")    # write the coordinate of hydrogen atom
    fout.write(("%.12f" % (x1)).rjust(20)+("%.12f" % (y1)).rjust(20)+("%.12f" % (z1)).rjust(20)+"\n")

    fout.write("HW".ljust(8)+str((n-1)*natm+3).rjust(10)+"\n")
    fout.write(("%.12f" % (x2)).rjust(20)+("%.12f" % (y2)).rjust(20)+("%.12f" % (z2)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*natm+4).rjust(10)+"\n")
    fout.write(("%.12f" % (x3)).rjust(20)+("%.12f" % (y3)).rjust(20)+("%.12f" % (z3)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*natm+5).rjust(10)+"\n")
    fout.write(("%.12f" % (x4)).rjust(20)+("%.12f" % (y4)).rjust(20)+("%.12f" % (z4)).rjust(20)+"\n")

fout.close()