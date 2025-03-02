Se necesitan 2 terminales para ejecutar el programa correctamente.

En una terminal ejecutamos python productor.py (numero de productores)

En otra terminal ejecutamos python consumidor.py (numero de consumidores)

Modele a los productores como pasteleros, los cuales tienen una lista de pasteles disponibles para producir.
La eleccion es al azar.

Igualmente los consumidores, son quienes agotan los pasteles.

Tuve que manejar exclusion mutua en todos los txts que genero. Pues la ejecucion del programa en una terminal
es independiente, esto quiere decir que no hay forma de acceder a las variables compartidas, en este caso los semaforos,
el contador y los pasteles producidos.

Estaba implementando esto en java, pero su lector y escritor chillaban mucho.


Defino un tamaño maximo de pasteles que se pueden almacenar en pasteles.txt, lo defino en buffer.py con un valor de 30, se puede moficar
para aumentar o reducir la capacidad. Hice una implementacion de colores para que sea más facil identificar coincidencias en producciones y consumos, por ejemplo si un productor produce un pastel, la impresión del consumo será del mismo color con el que se imprimio cuando se produjo.