# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from shutil import rmtree
from os.path import isdir
from os import mkdir
from sympy import solve, symbols, Eq
from sympy.physics.units import kilo, milli
from sympy.physics.units import convert_to
from sympy.physics.units import ohms, amperes, volts
import ltspice
import platform
import ahkab
import pylab as plt
from IPython import get_ipython

files_directory = "files\\"
fig_directory = "figuras\\"
import matplotlib.pyplot as plot



# ########################################################
#  # Carrera de condensadores
# ########################################################


# %% [markdown]
# ## Carrera de condensadores
#
# Ahora tenemos un circuito con dos condensadores en paralelo:
#
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensadores%20en%20paralelo.svg?sanitize=true)
#
# > **Pregunta:** Crea el netlist de este circuito e identifica qué condensador se satura primero. Dibuja la evolución de la intensidad en ambas ramas de manera simultánea. [Aquí](https://matplotlib.org/gallery/api/two_scales.html) tienes un ejemplo de cómo se hace esto en Matplotlib. Recuerda que para que Ahkab nos devuelva la corriente en una rama, debe de estar presente una pila. Si es necesario, inserta pilas virtuales de valor nulo (cero voltios), tal y como hemos comentado antes. Grafica también los voltajes (en otra gráfica, pero que aparezcan juntos).

# %%
get_ipython().run_cell_magic('writefile', '"carrera en condensadores.ckt"',
                             '* Carga condensador\nv0 0 1 type=vdc vdc=10\nr1 0 2 3k\nc1 2 3 47u ic=0\nv1dummy 3 1 type=vdc vdc=0\nc2 2 4 22u ic=0\nv2dummy 4 1 type=vdc vdc=0\n.tran tstep=0.01 tstart=6.5 tstop=7.5 uic=0\n.end')


# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit("carrera en condensadores.ckt")
netlist = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(netlist, análisis_en_netlist)
lista_de_análisis[0]['outfile'] = "simulación tran carrera condensadores.tsv"
resultados = ahkab.run(netlist, lista_de_análisis)


# %%
figura = plt.figure()
plt.title("Carrera de condensadores")
plt.xlim(6.65, 7.5)
plt.ylim(0.0, 0.0005)
plt.grid()
plt.plot(resultados['tran']['T'], resultados['tran']
         ['I(V1DUMMY)'], label="Intensidad en C1")
plt.plot(resultados['tran']['T'], resultados['tran']
         ['I(V2DUMMY)'], label="Intensidad en C2")

# %% [markdown]
# **Ejercicio premium:** Repite la simulación con LTspice (invocándolo como comando externo, leyendo los datos de un fichero `.raw` y volviendo a graficar con Matplotlib.
# %% [markdown]
# ## Circuitos en corriente alterna
#
# ** Ejercicio:** Simula este circuito con LTspice y representa el voltaje y la intensidad en función del tiempo. Traduce este ejercicio a la versión Spice de Akhab y haz la misma representación. Ahkab utiliza otra sintaxis para expresar la corriente alterna. Esta está descrita en la [documentación](https://ahkab.readthedocs.io/en/latest/help/Netlist-Syntax.html#id24).

# %%
get_ipython().run_cell_magic('writefile', '"corriente alterna.net"',
                             '* Circuito en corriente alterna\nv1 1 0 sin(0 120 60 0 0)\nr1 0 1 10k\n.tran 1\n.end')


# %%
lts "corriente alterna.net"

# %% [markdown]
# # Resumen de lo que se pide
# Volved a realizar todos los ejercicios y demos en vuestro propio notebook, explicando con vuestras palabras cada paso, cada gráfica y respondiendo a cada pregunta. Cuidad la belleza, coherencia, narración, explicaciones y gráficas. Todas las gráficas se han pintado con Matplotlib, que es una biblioteca extendidísima en ciencia y tecnología. Es muuuuy bueno que la conozcáis. [Aquí](https://matplotlib.org/tutorials/introductory/pyplot.html) tenéis muchos ejemplos.
