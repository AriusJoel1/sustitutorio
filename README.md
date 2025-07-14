## Examen Sustitutorio
En este proyecto generamos reportes automaticos a partir del historial del repositorio git y analizará con algoritmos sobre el grafo de commits. 

### Instalación
'''
git clone https://github.com/AriusJoel1/sustitutorio.git
cd sustitutorio
'''

### Pruebas automaticas 
'''
py -m pip install pytest
py -m pytest .\tests\test_graph.py
py -m pytest .\tests\test_report_suite.py
'''

## Reportes 
'''
py src/report_suite.py --input metrics.json --output report.md --format md
py src/graph_analysis.py --output metrics.json
'''

## Make Report (make all) 
'''
powershell -ExecutionPolicy Bypass -File scripts\make_report.ps1
'''

## Preguntas:

#### 1) grafo de commits como dag

    a. Demuestra que no existen ciclos en el grafo de commits de git explicando el modelo de contenido inmutable de objetos.

    En el proyecto, al analizar el historial de commits usando git rev-list --all --parents, se puede observar que el grafo de commits es un DAG esto viene por defecto como diseño fundamental de Git y modela su historial como una estructura inmutable, donde cada commit apunta a uno o mas padres que ya existen. Ademas cada commit se guarda en un hash y este no puede ser modificado sin que cmabie su hash. Por eso los ciclos no pueden existir ya que los commits sólo conocen a sus padres esto garantiza que el grafo de commits de cualquier repositorio como el que podemos ver con nuestro graph_analysis.py donde siempre es un DAG. 

    b. Analiza la complejidad de la busqueda del critical merge path en un dag con N nodos y M aristas

    En nuestro proyecto tenemos una métrica llamada critical merge path en la funcion compute_metrics() donde podemos encontrar commits que representan merges. Esta métrica recorre el grafo de commits desde el último hacia el primero. Como el grafo es un DAG, se puede procesar en orden topológico y si quisiéramos encontrar el camino más critico entre dos commits en nuestro caso desde HEAD hasta v0.0.0, podemos hacerlo eficientemente con un algoritmo sobre dicho orden. Y finalmente la complejidad de esto sería O(N + M), porque cada nodo y cada arista se procesa una sola vez. En mi proyecto no he implementamos este recorrido por caminos, pero sí identificamos los commits críticos al recorrer el grafo una vez, lo que encaja con esa misma complejidad

#### 2)di, dip e isp
    
    a) Argumenta como la dependency injection en la micro-suite respeta el dependency inversion principle y el interface segregation principle, ejemplificando con tus clases de servicios y sus interfaces
 
    En la micro-suite que construimos en report_suite.py, usamos DI para mantener nuestras clases desacopladas y reutilizables. Por ejemplo, la clase principal ReportingSuite no crea por si misma los servicios que necesita y por otro lado recibe en su constructor instancias de CommitStatsService, ReleaseNotesService y ChangeLogWriter. Esto nuestro caso tenemos el DIP que en vez de depender directamente de clases concretas, depende de comportamientos lo que nos permitió fácilmente inyectar mocks en los tests unitarios con unittest.mock


