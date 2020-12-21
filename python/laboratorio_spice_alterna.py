# %%
from shutil import rmtree
from os.path import isdir
from os import mkdir
from IPython.core.display import set_matplotlib_formats
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
fig_directory = "..\\resource\\figures\\"
import matplotlib.pyplot as plot
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

# Primero preparamos un lugar para ubicar todo los archivos que genere el Notebook
# %%
files_directory = "files\\"
# si el directorio existe se elimina con su contenido
if isdir(files_directory):
    rmtree(files_directory)
# crea un directorio para alojar todo los archivos que se generen
mkdir(files_directory)

fig_directory = "..\\resource\\figures\\"
# si el directorio existe se elimina con su contenido
if isdir(fig_directory):
    rmtree(fig_directory)
# crea un directorio para alojar todo los archivos que se generen
mkdir(fig_directory)

get_ipython().run_line_magic(
    'alias', 'lts /Applications/LTspice.app/Contents/MacOS/LTspice -ascii -b')
if platform.system() == "Windows":
    get_ipython().run_line_magic(
        'alias', 'lts "C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe" -ascii -b ')


# ########################################################
#  # Circuitos en AC 
# ########################################################


# %% [markdown]
# ## Circuitos en corriente alterna
#
# ### ** Ejercicio:** 
# 
# Simula este circuito con LTspice y representa el voltaje y la intensidad en función del tiempo. Traduce este ejercicio a la versión Spice de Akhab y haz la misma representación. Ahkab utiliza otra sintaxis para expresar la corriente alterna. Esta está descrita en la [documentación](https://ahkab.readthedocs.io/en/latest/help/Netlist-Syntax.html#id24).
# ```* Circuito en corriente alterna
# v1 1 0 sin(0 120 60 0 0)
# r1 0 1 10k
# .tran 1
# .end
# ```
# %% [markdown]
# ### ** Solución:** 
# 
# ![](https://raw.githubusercontent.com/tikissmikiss/Laboratorio-LTspice/master/resource/Circuito_alterna_lab_fisica.svg?sanitize=true)
# 
# Se simula un circuito de corriente alterna usando un generador de onda sinosoidal configurado con un voltaje de pico de $\mathrm{120\ v}$, es decir, $V_{pp}=\mathrm{240\ v}$, y una fecuencia de $\mathrm{60\ Hz}$, conectado a una carga de $\mathrm{10\ k\Omega}$
# %%
%%writefile "files\corriente_alterna.net"
* Circuito en corriente alterna
v1 1 0 sin(0 120 60 0 0)
r1 0 1 10k
.tran 1
.end
# %% [markdown]
# Ejetumos LTspice con el netlist como parametro para generar los archivos `.log` y `.raw`.
# %%
# ############################################################
# lts "files\corriente_alterna.net"
# ############################################################
if platform.system() == "Darwin":
    get_ipython().system('/Applications/LTspice.app/Contents/MacOS/LTspice -ascii -b files/corriente_alterna.net')

if platform.system() == "Windows":
    get_ipython().system('"C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe" -ascii -b files\\corriente_alterna.net')

# %% [markdown]
# Ahora extraemos los datos relativos al tiempo, la corriente y tensión del archivo `.raw` y los almacenamos en vectores diferentes.
# %%
l = ltspice.Ltspice("files\corriente_alterna.raw")
l.parse()

tiempo = l.get_time()
vac = l.get_data('V(1)')
i_R1 = l.get_data('I(R1)')
nSvg=0
# %% [markdown]
# Representamos los datos obtenidos con LTspice en una misma gráfica.
# %%
plot.rcParams['figure.figsize'] = [6.4*1.9, 4.8]
plot.rcParams['font.size'] = 12
rojo='tab:red'
verde='tab:green'

fig, ax_V = plot.subplots()
plot.title('Circuito Corriente Alterna - ($\mathrm{10v}$) - VAC:$\mathrm{120v}$-$\mathrm{60Hz}$ R:$\mathrm{10k\Omega}$ - LTspice')
ax_I = ax_V.twinx()  

ax_V.tick_params(axis='y', labelcolor=verde)
ax_I.tick_params(axis='y', labelcolor=rojo)

ax_V.set_xlabel('Tiempo (s)')
ax_V.set_ylabel('Voltaje (V)', color=verde)
ax_I.set_ylabel('Corriente (A)', color=rojo)

line_V, = ax_V.plot(tiempo, vac)
line_V.set_label('Corriente R1')
line_V.set_c(verde)

line_I, = ax_I.plot(tiempo, i_R1)
line_I.set_label('Voltaje VAC')
line_I.set_c(rojo)

plot.grid(True)
plot.tight_layout()
nSvg += 1
fig.savefig(fig_directory + 'alterna' + str(nSvg) + '.svg', transparent='true', format='svg')
# %% [markdown]
# Hemos representado la señal en el transcurso de 1 segundo y es difícil de apreciar la señal con claridad. 
# Vamos a representar usando el mismo espacio, tres ciclos completos. Puesto que la onda generada es de $\mathrm{60\ Hz}$, tenemos que captura tres veces la sexagésima parte de un segundo, es decir, $\mathrm{\frac{1}{20}\ s}$.
# %%
plot.rcParams['figure.figsize'] = [6.4*1.9, 4.8]
plot.rcParams['font.size'] = 12
rojo='tab:red'
verde='tab:green'

fig, ax_V = plot.subplots()
ax_V.set_xlim(0, 1/20)
plot.title('Circuito Corriente Alterna - ($\mathrm{10v}$) - VAC:$\mathrm{120v}$-$\mathrm{60Hz}$ R:$\mathrm{10k\Omega}$ - LTspice')
ax_I = ax_V.twinx()  

ax_V.tick_params(axis='y', labelcolor=verde)
ax_I.tick_params(axis='y', labelcolor=rojo)

ax_V.set_xlabel('Tiempo (s)')
ax_V.set_ylabel('Voltaje (V)', color=verde)
ax_I.set_ylabel('Corriente (A)', color=rojo)

line_V, = ax_V.plot(tiempo, vac)
line_V.set_label('Corriente R1')
line_V.set_c(verde)

line_I, = ax_I.plot(tiempo, i_R1)
line_I.set_label('Voltaje VAC')
line_I.set_c(rojo)

plot.grid(True)
plot.tight_layout()
nSvg += 1
fig.savefig(fig_directory + 'alterna' + str(nSvg) + '.svg', transparent='true', format='svg')
# %% [markdown]
# Vaya,... Parece que se ha perdido algo de calidad en la representación y la onda no se ve todo lo suavizada que debería. Esto es debido a que hemos pedido a LTspice que muestre la señal durante un segundo, por lo que ha adaptado el sampling rate a ese tiempo. Ahora, al dibujar solo 0.05 segundos, el número de muestras contenidas en ese tiempo es relativamente bajo, y por eso podemos apreciar en el gráfico vectorial los vectores rectos que dibujan la curva, apreciándose los vértices donde confluyen dos vectores.
# 
#   Aunque la calidad es podría ser suficiente para analizar el resultado, estamos por aprender, así que vamos a volver a repetir la simulación pero esta vez le pediremos a LTspice que concentre todas las muestras en 0.05 segundos.
# 
# Veamos el resultado.
# %%
%%writefile "files\corriente_alterna.net"
* Circuito en corriente alterna
v1 1 0 sin(0 120 60 0 0)
r1 0 1 10k
.tran 0.05
.end
# %%
# ############################################################
# lts "files\corriente_alterna.net"
# ############################################################
if platform.system() == "Darwin":
    get_ipython().system('/Applications/LTspice.app/Contents/MacOS/LTspice -ascii -b files/corriente_alterna.net')

if platform.system() == "Windows":
    get_ipython().system('"C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe" -ascii -b files\\corriente_alterna.net')

l = ltspice.Ltspice("files\corriente_alterna.raw")
l.parse()

tiempo = l.get_time()
vac = l.get_data('V(1)')
i_R1 = l.get_data('I(R1)')

plot.rcParams['figure.figsize'] = [6.4*1.9, 4.8]
plot.rcParams['font.size'] = 12
rojo='tab:red'
verde='tab:green'

fig, ax_V = plot.subplots()
ax_V.set_xlim(0, 1/20)
plot.title('Circuito Corriente Alterna - ($\mathrm{10v}$) - VAC:$\mathrm{120v}$-$\mathrm{60Hz}$ R:$\mathrm{10k\Omega}$ - LTspice')
ax_I = ax_V.twinx()  

ax_V.tick_params(axis='y', labelcolor=verde)
ax_I.tick_params(axis='y', labelcolor=rojo)

ax_V.set_xlabel('Tiempo (s)')
ax_V.set_ylabel('Voltaje (V)', color=verde)
ax_I.set_ylabel('Corriente (A)', color=rojo)

line_V, = ax_V.plot(tiempo, vac)
line_V.set_label('Corriente R1')
line_V.set_c(verde)

line_I, = ax_I.plot(tiempo, i_R1)
line_I.set_label('Voltaje VAC')
line_I.set_c(rojo)

# plot.legend()
plot.grid(True)
plot.tight_layout()
nSvg += 1
fig.savefig(fig_directory + 'alterna' + str(nSvg) + '.svg', transparent='true', format='svg')
# %% [markdown]
# Ahora sí, otra cosa es esto. Como podemos apreciar en la gráfica, el voltaje y la corriente evolucionan con una proporcionalidad inversa de 10000:1, justamente el número de ohmios que tiene una resistencia de $\mathrm{10\ k\Omega}$ como la de nuestro circuito. ¿Que porqué coincide?, pues por la Ley de Ohm, para $\mathrm{10\ k\Omega}$ hacen falta $\mathrm{10\ kV}$ para tener $\mathrm{1\ A}$.


# %% [markdown]
# ### Ahora realicemos la simulación con Ahkab
# Lo primero es adaptar el netlist

# %%
%%writefile "files\corriente_alterna.ckt"
* Circuito alterna
V1 1 0 type=sin vo=0 va=120 freq=60
R1 0 1 10k
.tran tstep=0.0001 tstart=0 tstop=0.05
.end

# %% [markdown]
# ### Procesamos el circuito con `Ahkab` y extraemos los datos.

# %%
# Procesar circuito
circuito_y_análisis = ahkab.netlist_parser.parse_circuit("files\corriente_alterna.ckt")
# Separar datos netlist y simulaciones
netlist = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
# Extraer datos de simulaciones
lista_de_análisis = ahkab.netlist_parser.parse_analysis(netlist, análisis_en_netlist)
# Establecer condiciones óptimas para los análisis `.dc` y/o `.tran` si lo hay.
for análisis in [d for i, d in enumerate(lista_de_análisis) if "dc" in d.values() or "tran" in d.values()]:
    análisis['outfile'] = files_directory + "simulación_" + análisis['type'] + ".tsv"
# %% [markdown]
#  Ejecutamos la simulación
# %%
resultados = ahkab.run(netlist, lista_de_análisis)
# %%
tiempo = resultados['tran']['T']
vac = resultados['tran']['V1']
f = lambda x: -x if x < 0 else x
i_R1 = resultados['tran']['I(V1)']
# i_R1 = list(map(f, i_R1))

plot.rcParams['figure.figsize'] = [6.4*1.9, 4.8]
plot.rcParams['font.size'] = 12
rojo='tab:red'
verde='tab:green'

fig, ax_V = plot.subplots()
# ax_V.set_xlim(0, 1/20)
plot.title('Circuito Corriente Alterna - ($\mathrm{10v}$) - VAC:$\mathrm{120v}$-$\mathrm{60Hz}$ R:$\mathrm{10k\Omega}$ - Ahkab')
ax_I = ax_V.twinx()  

ax_V.tick_params(axis='y', labelcolor=verde)
ax_I.tick_params(axis='y', labelcolor=rojo)

ax_V.set_xlabel('Tiempo (s)')
ax_V.set_ylabel('Voltaje (V)', color=verde)
ax_I.set_ylabel('Corriente (A)', color=rojo)

line_V, = ax_V.plot(tiempo, vac)
line_V.set_label('Corriente R1')
line_V.set_c(verde)

line_I, = ax_I.plot(tiempo, i_R1)
line_I.set_label('Voltaje VAC')
line_I.set_c(rojo)

plot.grid(True)
plot.tight_layout()
nSvg += 1
fig.savefig(fig_directory + 'alterna' + str(nSvg) + '.svg', transparent='true', format='svg')




















# %% [markdown]
# ## CONCLUSION
# 
# <<<< Cuando se em ocurra >>>>
# 
# 
# Volved a realizar todos los ejercicios y demos en vuestro propio notebook, explicando con vuestras palabras cada paso, cada gráfica y respondiendo a cada pregunta. Cuidad la belleza, coherencia, narración, explicaciones y gráficas. Todas las gráficas se han pintado con Matplotlib, que es una biblioteca extendidísima en ciencia y tecnología. Es muuuuy bueno que la conozcáis. [Aquí](https://matplotlib.org/tutorials/introductory/pyplot.html) tenéis muchos ejemplos.

