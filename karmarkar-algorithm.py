######################################
# Akbar Ghaedi: @1403-02-28.v1.0.0
#     1403-02.term
#
# Dr Salimifard homework
# 
# Karmarkar Algorithm
#   find answer for all model
#
######################################
#
# # Dr. Salimifard slide sample
# A = [1, 1, 1]
# C = [1, 2, 0]
# X = [2, 2, 4]
#
#
# Dr Salimifard homework
#
# max = x1 + 3*x2 - 3*x3;
# X2 - X3 = 0;
# X1 + X2 + X3 = 1;
# X1 >= 0;
# X2 >= 0;
# X3 >= 0;
#
A = [[0, 1, -1],
     [1, 1,  1]]
C = [1, 3, -3]
X = [0.5, 0.25, 0.25]

# max break loop: stop loop if answer does not found in steps: 
#   prevent of infinite loop
MaxBreakLoop = 100
alfa = 0.5
ep = 0.001       # max distance from best optimal point

# print("Len(C) = ", len(C))
I = np.identity(len(C));  print("I = \n", I)
# create row/col identity array-vector [1, 1, 1]
I1 = np.mat([[1] * len(C)]).T;  print("I1 = \n", I1)

A = np.array(A)
C = np.array(C)
X = np.array(X)
print("A = \n", A)
print("C = \n", C)
print("X = \n", X)

# calculate first(previous) Z (answer) via first random X (answer) value
Zpre = np.dot(np.mat(C), np.mat(X).T).item(); print("Zpre = ", Zpre)

steps = 0   # loop steps counter
while True:
  steps += 1
  if steps >= MaxBreakLoop: break
  print(f"--------------- STEP: {steps} ---------------")

  # n) <--- as Dr. Salimifard Karmarkar-Algorithm slids steps

  # 3) diagonal matrix
  D = np.diag(np.squeeze(np.asarray(X)));   print("D = \n", D);
  Di = np.linalg.inv(D);                    print("Di = \n", Di)

  # 4) calculate Xb, Ab, Abt, Cb
  Xb = np.dot(Di, X);               print("Xb = \n", Xb)
  Ab = np.dot(A, D);                print("Ab = \n", Ab)
  Abt = np.mat(Ab).T;               print("Abt = \n", Abt)
  Cb = np.dot(D, np.mat(C).T);      print("Cb = \n", Cb)

  # 5) Projection: calculate projection matrix
  #       part by part for print steps answer
  #
  p1 = np.dot(Ab, Abt);               print("p1 = \n", p1)
  p2 = np.linalg.inv(p1);             print("p2 = \n", p2)
  p3 = p2 * Ab;                       print("p3 = \n", p3)
  p4 = np.mat(Ab).T * np.array(p3);   print("p4 = \n", p4)
  P = I - p4;                         print("P = \n", P)

  # 6) Gradian Vector
  Cp = np.dot(P, Cb);  print("Cp = ", Cp)

  # 7) gama
  gama = abs(np.min(np.where(Cp < 0, Cp, 0)));  print("gama = ", gama)
  Xb = I1 + (alfa / gama) * Cp;                 print("Xb = \n", Xb)

  # 8) reverse projection
  X = np.dot(D, Xb);  print("X = \n", X)

  # Z calculation
  Z = np.dot(C, X).item();  print("Z = ", Z)

  # 9) verify stop condition
  #   z(k) - z(k-1) = Z - Zpre
  newState = abs(Z - Zpre)

  if abs(newState) <= ep:
    # find optimized answer and program END
    print(f"|Z - Zpre| = |{Z} - {Zpre}| = {newState} ≤ {ep}")
    print(f"Optimized Z = {Z} on {steps} steps")
    print("X = ", np.squeeze(np.asarray(X)))
    break
  else:
    # print new Z, Set Z to Zpre and so go to lopp start step
    print(f"|Z - Zpre| = |{Z} - {Zpre}| = {newState}")
    Zpre = Z

##################### End of Program #####################
