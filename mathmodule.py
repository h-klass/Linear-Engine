import numpy as np

# scale vector
def scale_vect(scale,vector):
    outvector = [0 for n in range(len(vector))]
    for i in range(len(vector)):
        outvector[i] = scale*vector[i]
    return outvector

# scale matrix
def scale_matrix(scale,mat):
    outmat = [[0 for j in range(len(mat[0]))] for i in range(len(mat))]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            outmat[i][j] = scale*mat[i][j]
    return outmat

# transform vector by matrix
def transform_vect(matrix, vector):
    outvector = [0 for n in range(len(vector))]
    for i in range(len(vector)):
        runtotal = 0
        for j in range(len(vector)):
            runtotal += matrix[i][j]*vector[j]
        outvector[i] = runtotal
    return outvector

# get vector length/magnitude
def vect_length(vect):
        runtotal = 0
        for i in range(len(vect)):
            runtotal += np.power(vect[i],2)
        return np.sqrt(runtotal)

# calculate cross product of 2 vectors
def vect_cross(vect1,vect2):
    return [(vect1[1]*vect2[2]-vect1[2]*vect2[1]),(vect1[2]*vect2[0]-vect1[0]*vect2[2]),(vect1[0]*vect2[1]-vect1[1]*vect2[0])]

# calculate sum of 2 matrices
def matrix_add(mat1,mat2):
    outmatrix = [[0 for j in range(len(mat1[0]))] for i in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
          outmatrix[i][j] = mat1[i][j] + mat2[i][j]
    return outmatrix

# calculate dot product of 2 vectors
def vect_dot(vect1,vect2):
    runtotal = 0
    for i in range(len(vect1)):
        runtotal += vect1[i]*vect2[i]
    return runtotal

# calculate product/composition of 2 matrices
def matrix_prod(mat1,mat2):
    outmat = [[0 for n in range(len(mat2[0]))] for n in range(len(mat1))]
    for i in range(len(mat1)): #i denotes row#
        for j in range(len(mat2[0])): #j denotes column#
            rowvect = mat1[i]
            colvect = [mat2[n][j] for n in range(len(mat2))]
            outmat[i][j] = vect_dot(rowvect,colvect)
    return outmat