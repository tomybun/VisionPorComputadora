fila1 = [2,2,5,6]
fila2 = [0,3,7,4]
fila3 = [8,8,5,2]
fila4 = [1,5,6,1]

matriz = [fila1, fila2, fila3, fila4]

#imprime
for row in matriz:
	print()
	for col in row:
		print(col, end = ' ')
print()

#algoritmo que hace cero la columna
for i, row in enumerate(matriz):
	for j, col in enumerate(row):
		if i == j:
			matriz[i][j] = 0
#imprime
for row in matriz:
	print()
	for col in row:
		print(col, end = ' ')
print()

#algoritmo que pone los pares en cero y los impares en 1
for i, row in enumerate(matriz):
	for j, col in enumerate(row):
		if col % 2 == 0:
			matriz[i][j] = 0
		else:
			matriz[i][j] = 1
					
#imprime
for row in matriz:
	print()
	for col in row:
		print(col, end = ' ')
print()			
			
