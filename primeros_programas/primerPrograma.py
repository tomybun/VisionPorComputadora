#	Crear una función adivinar que permita adivinar un número
#	generado en forma aleatoria
#	 -El número debe estar entre 0 y 100
#	 -Este número se genera adentro de la función
#	 -Además debe recibir un parámetro que sea la cantidad de intentos y
#	en caso de que esta cantidad de intentos sea superada el programa
#	debe terminar con un mensaje
#	 -Si el usuario adivina antes de superar el número de intentos máximo,
#	se debe imprimir un mensaje con el número de intentos en los que
#	adivinó
#	Después de crear la función, llamarla en el mismo archivo
#	Ejecutar el script desde la consola


import random	

def adivinar(intentos):

	num_rand = random.randint(0, 100)
	
	print("\n", num_rand)
	
	for i in range(intentos):
		num = int(input("Ingrese el numero aleatoreo: " ))
		if num == num_rand:
			print("\nCorrecto!!!")
			return i
		else:	
			print("\nIncorrecto!! Intentelo de vuelta.")
			
	return i
	
intentos = int(input("Ingrese la cantidad de intentos que quiere tener: "))

a = adivinar(intentos)

print("\nLa cantidad de intentos que utilizó fueron: ",a+1)		
