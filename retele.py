import pathlib

from numpy import matrix

# 1. Parsing the System of Equations
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A: list[list[float]] = []
    B: list[float] = []

    with open(path, "r") as f:
        for line in f:
            if "=" not in line:
                continue
            st,dr=line.split("=")
            B.append(float(dr))

            linie=[]
            semn=1.0
            for token in st.split():
                if token=="+":
                    semn=1.0
                elif token=="-":
                    semn=-1.0
                else:
                    val_str=token[:-1]
                    if(val_str==""):
                        val=1.0
                    else:
                        val=float(val_str)
                    linie.append(val*semn)
            A.append(linie)
    return A,B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=}")
print(f"{B=}")

# 2. Matrix and Vector Operations
def determinant(matrix: list[list[float]]) -> float:
    a11,a12,a13=matrix[0]#despachetare
    a21,a22,a23=matrix[1]
    a31,a32,a33=matrix[2]
    det=a11*(a22*a33-a23*a32)-a12*(a21*a33-a23*a31)+a13*(a21*a32-a22*a31)
    return det
print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    tr=matrix[0][0]+matrix[1][1]+matrix[2][2]
    return tr
print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    norma=vector[0]**2+vector[1]**2+vector[2]**2
    return norma**0.5
print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    n=len(matrix)
    rez=[]
    for i in range(n):
        linie_noua=[]
        for j in range(n):
            linie_noua.append(matrix[j][i])
        rez.append(linie_noua)
    return rez
print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    m=[]
    n=len(matrix)
    for i in range(n):
        val=matrix[i][0]*vector[0]+matrix[i][1]*vector[1]+matrix[i][2]*vector[2]
        m.append(val)
    return m
print(f"{multiply(A, B)=}")

# 3. Solving using Cramer's Rule
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A=determinant(matrix)
    A_x = [[vector[0], matrix[0][1], matrix[0][2]],
        [vector[1], matrix[1][1], matrix[1][2]],
        [vector[2], matrix[2][1], matrix[2][2]]]
    A_y = [[matrix[0][0], vector[0], matrix[0][2]],
        [matrix[1][0], vector[1], matrix[1][2]],
        [matrix[2][0], vector[2], matrix[2][2]]]
    A_z=[[matrix[0][0], matrix[0][1], vector[0]],
        [matrix[1][0], matrix[1][1], vector[1]],
        [matrix[2][0], matrix[2][1], vector[2]]]
    x = determinant(A_x)/det_A
    y = determinant(A_y)/det_A
    z = determinant(A_z)/det_A
    return [x,y,z]
print(f"{solve_cramer(A, B)=}")

# 4. Solving using Inversion
def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    m = []
    n = len(matrix)
    for i1 in range(n):
        if i1==i:
            continue
        linie=[]
        for j1 in range(n):
            if j1==j:
                continue
            linie.append(matrix[i1][j1])
        m.append(linie)
    return m

def cofactor(matrix: list[list[float]]) -> list[list[float]]: #cofactor=A de i si j
    n=len(matrix)
    A_ij=[]
    for i in range (n):
        linie = []
        for j in range (n):
            m=minor(matrix, i, j)
            det=m[0][0]*m[1][1]-m[0][1]*m[1][0]
            linie.append((-1)**(i+j)*det)
        A_ij.append(linie)
    return A_ij

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    adj=[]
    cof=cofactor(matrix)
    adj=transpose(cof)
    return adj

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    X=[]
    det_A=determinant(matrix)
    adj_A=adjoint(matrix)
    n=len(matrix)
    inv_A=[]
    for i in range(n):
        linie=[]
        for j in range(n):
            linie.append(1/det_A*adj_A[i][j])
        inv_A.append(linie)

    X=multiply(inv_A, vector)
    return X
print(f"{solve(A, B)=}")