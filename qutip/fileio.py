#This file is part of QuTIP.
#
#    QuTIP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    QuTIP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTIP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011, Paul D. Nation & Robert J. Johansson
#
###########################################################################

from scipy import *

# ------------------------------------------------------------------------------
# Write matrix data to a file
#
def file_data_store(datafile, data, sep=",", numtype="complex", numformat="decimal"):

    if datafile == None or data == None:
        raise ValueError("datafile or data is unspecified")

    M,N = shape(data)

    f = open(datafile, "w")
    
    if numtype == "complex":

        if numformat == "exp":

            for m in range(M):
                for n in range(N):
                    if imag(data[m,n]) >= 0.0:
                        f.write("%.10e+%.10ej" % (real(data[m,n]),imag(data[m,n])))
                    else:
                        f.write("%.10e%.10ej" % (real(data[m,n]),imag(data[m,n])))
                    if n != N-1:
                        f.write(sep)
                f.write("\n")

        elif numformat == "decimal":

            for m in range(M):
                for n in range(N):
                    if imag(data[m,n]) >= 0.0:
                        f.write("%.10f+%.10fj" % (real(data[m,n]),imag(data[m,n])))
                    else:
                        f.write("%.10f%.10fj" % (real(data[m,n]),imag(data[m,n])))
                    if n != N-1:
                        f.write(sep)
                f.write("\n")

        else:
            raise ValueError("illegal numformat value (should be 'exp' or 'decimal')")    


    elif numtype == "real":

        if numformat == "exp":

            for m in range(M):
                for n in range(N):
                    f.write("%.10e" % (real(data[m,n])))
                    if n != N-1:
                        f.write(sep)
                f.write("\n")

        elif numformat == "decimal":

            for m in range(M):
                for n in range(N):
                    f.write("%.10f" % (real(data[m,n])))
                    if n != N-1:
                        f.write(sep)
                f.write("\n")

        else:
            raise ValueError("illegal numformat value (should be 'exp' or 'decimal')")    
    

    else:
        raise ValueError("illegal numtype value (should be 'complex' or 'real')")    

    f.close()

# ------------------------------------------------------------------------------
# Read matrix data from a file
#
def file_data_read(datafile, sep=","):

    if datafile == None:
        raise ValueError("datafile is unspecified")

    f = open(datafile, "r")

    #
    # first count lines and numbers of 
    #
    M = N = 0
    for line in f:
        line_vec = line.split(sep)
        n = len(line_vec)
        if N == 0 and n > 0:
            N = n
            # check type
            if ("j" in line_vec[0]) or ("i" in line_vec[0]):
                numtype = "complex"
            else:
                numtype = "real"

            # check format
            if ("e" in line_vec[0]) or ("E" in line_vec[0]):
                numformat = "exp"
            else:
                numformat = "decimal"

        elif N != n:
            raise ValueError("Badly formatted data file: unequal number of columns")
        M += 1

    #
    # read data and store in a matrix
    #

    f.seek(0)

    if numtype == "complex":

        data = zeros((M,N), dtype="complex")
        m = n = 0
        for line in f:
            n = 0
            for item in line.rstrip().split(sep):
                data[m,n] = complex(item)
                n += 1
            m += 1
    
    else:

        data = zeros((M,N), dtype="float")        
        m = n = 0
        for line in f:
            n = 0
            for item in line.rstrip().split(sep):
                data[m,n] = float(item)
                n += 1
            m += 1
                    

    f.close()


    return data