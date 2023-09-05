# FORMAL

### Migración de la DB a SQLite
Se migró el la DB de un _*.xlsx*_ a una base de datos de SQLite, para usar la librerías SQLite3 de Python para la lectura de los datos de respuesta que requiere el chatbot. Así no solo se mejora la velocidad del _*bootstrapping*_ del programa. Además, se aprovacha la velocidad de la memoria RAM y la caché, haciendo uso solo de dos _*queries*_ a SQLite para crear dos _*arrays*_ con toda la información de la DB, ya que es más rápido ir accediendo a un _*array*_ o _*dict*_ que hacer llamadas a la DB con SQL, pero esto úlitmo es más rápido que leer un archivo.

### Reescritura de la clase _*manager_dataDB*_
En __actions.py__ se reescribió la clase _*manager_dataDB*_ para usar SQLite3 para el acceso a la base de datos. Los métodos se conservaron, así como sus nombres, tan solo cambió la implementación de los mismos

### Añadidos múltiples ejemplos y _*stories*_
En _*nlu.yml*_ y _*stories.yml*_ se añadieron múltiples nuevos ejemplos nuevos para cuando el usuario inserta un _*input*_ con múltiples __tipo_dato__ o __asignatura__ y no hay comas de separación o conjunciones.