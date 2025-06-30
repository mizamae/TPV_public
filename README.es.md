<!-- Este archivo es parte del entorno Tiny TPV.

Tiny TPV es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal y como han sido publicados por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.

Tiny TPV se distribuye con la esperanza de que sea útil, pero SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con Tiny TPV. En caso contrario, visita <https://www.gnu.org/licenses/>. -->

# Tiny TPV
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](README.es.md)

Esto crea una aplicación web (conectada a Tiny TPV) que puede utilizarse como un sitio web comercial. Incluye las siguientes características:
- Diseño adaptable para una visualización cómoda en cualquier dispositivo
- Actualización automática de productos desde Tiny TPV (requiere una configuración menor en la aplicación Tiny TPV)

## Instalación

Crea un entorno virtual basado en Python 3.11 o superior.
Utiliza el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar Tiny TPV.

```
pip install -r requirements.txt
```

El servidor web debe configurarse según sea necesario dependiendo del software utilizado. En este repositorio, se entrega una aplicación de ejemplo configurada con Nginx y Gunicorn.

La configuración predeterminada para Nginx está detallada en el archivo ![Configuración de Nginx](/customerPortal.conf).

Los archivos para configurar los servicios de Gunicorn y Celery se proporcionan en ![Configuración de Gunicorn](/gunicorn.service) y ![Configuración de Celery](/celery_worker.service) respectivamente.

## Apariencia

Una vez que todo está configurado y en funcionamiento, al acceder al punto de entrada predeterminado (webpage-endpoint.com en el archivo de configuración de Nginx) aparece la página predeterminada.
![página predeterminada](/assets/images/default_page.png)
La página está estructurada en secciones que pueden ser fácilmente alcanzadas desplazándose hacia abajo o haciendo clic en los títulos de la barra de navegación. Cabe mencionar que esta página es totalmente personalizable en apariencia y forma.

Lo interesante es que en el el background se está ejecutando una aplicación Django (sobre una base de datos Postgresql) con los siguientes modelos disponibles:

- Familia de productos: esto sirve como un contenedor para agrupar productos que comparten una característica similar, como comida para perros, comida para gatos, etc.
- Producto: representa cada producto individual que puedes ofrecer a los visitantes.

Si el comercio vende libros, una familia de productos podría ser Cómics. A través de la interfaz de Tiny TPV se crea esa familia y de forma automática se reflejará en la página web pública para que los clientes en línea puedan acceder.
![familias de productos](/assets/images/familias.png)
Al hacer clic en la imagen de una familia, aparecerán todos los productos pertenecientes a esa familia (que han sido creados a través de la interfaz de Tiny TPV), mostrando su precio y stock actual.
![productos de la familia](/assets/images/productos.png)

## Contribuciones

Las solicitudes de incorporación de cambios (pull requests) son bienvenidas. Para cambios importantes, por favor abre primero una incidencia para discutir qué te gustaría modificar.

Por favor, asegúrate de actualizar las pruebas según sea necesario.

## Licencia

Tiny TPV es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal y como han sido publicados por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a tu elección) cualquier versión posterior.

Tiny TPV se distribuye con la esperanza de que sea útil, pero SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con Tiny TPV (consulta [licencia](gpl-3.txt)).