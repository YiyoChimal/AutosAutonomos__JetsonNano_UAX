# DonkeyCar con Raspberry
Devido a los probemas con la corrupción del sismetam operativo que tivimos con el carro Jetracer, decidomos cambiar la unidad de procesamiento 
de una JetsonNano a una Raspberry debido a que esta contaba con mayor documentación y con una potencia necesaroa para hacer funcianar el proyect.

De vido a esto tuvimos que hacer una lijeras adaptaciones, que en su mayoria fueron en cuentión de conexiones electicas. Acontinuación se mostrara el material y las conexiones a realizar para 
la adaptación.

## Material
-Raspberry PI 4 Model B 2GB RAM
-Web cam 
-Jumpers 
-Cable USB C

## Conexiones
I2C: Se realizo la conexión de los para i2c de la raspbery a la placa de drivers del jetracer que comprenden los pines SDA, SCL y GND.
Alimentación: Se relizo la conexión del pin de 3.3V de la Raspberry a la placa del Jetrace y del pin de 5V de la Jetracer seralizo una modificación a un cable USB C para conectarlo a la alimentación de la Raspberry.
¡Advertencia: No conectar el pin de 5V del area del pines GPIO de la Raspberry al pin de 5V de la placa del JetRacer si ya se realizo la conexión con el cable USB C!
<img width="768" height="794" alt="image" src="https://github.com/user-attachments/assets/6195e7d8-db32-407f-af6d-1150fe2f9ec9" />
