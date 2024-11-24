# Aplicación Web para diseños de Tablaroca
 Página web para visualizar diferentes tipos de diseño en tablaroca, así como poder subir tus propias imagenes.

## Interfaz

![Tutorial](images/4.png)

  Cuenta con servicio de autenticación y registro de usuarios.

## Subida de imágenes

![Tutorial](images/5.png)

  El usuario también es capaz de subir sus propias imágenes de diseños.

![Tutorial](images/6.png)

  Y también tiene la opción de visualizarlas mejor.

![Tutorial](images/7.png)

  Una vez que se cierra sesión, las imagenes subidas no se podran ver hasta que el usuario vuelva a ingresar sus datos de sesión.

![Tutorial](images/8.png)

![Tutorial](images/5.png)

## Backend

Los servicios están alojados en contenedores utilizando Docker, y orquestando con Kubernetes.

![Tutorial](images/10.png)

De momento los servicios que se encuentran funcionando son el servicio de autenticación y registro, y el servicio de imágenes.

### Servicios en Kubernetes

![Tutorial](images/11.png)

### Pods en Kubernetes

![Tutorial](images/12.png)

### Todos los contenedores en Docker

![Tutorial](images/13.png)

## Tabla de autenticación y registro 

  Utilizo una base de datos en PostgreSQL para almacenar el nombre de usuario y la contraseña de los usuarios que se registran, al momento de registrarse, la base de datos guarda el id como PK, el nombre de usuario y la contraseña. La contraseña se guarda en forma de hash utilizando JWT(libreria) para seguridad de la misma.

  ![Tutorial](images/14.png)

## Tabla para subida de imagenes

  En esta tabla se almacena el id como PK, el usuario que subió dicha imagen, el nombre del archivo ya que se puede elegir que archivo subir desde el frontend y la fecha de la subida.

  ![Tutorial](images/15.png)

  Las imágenes se guardan localmente en mi computadora y estas son devueltas para ser visualizadas en el frontend.

  ![Tutorial](images/16.png)
