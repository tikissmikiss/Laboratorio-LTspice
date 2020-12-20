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
fig_directory = "..\\resource\\figures\\"
import matplotlib.pyplot as plot
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')
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


# %% [markdown]
# ## Carrera de condensadores
#
# Ahora tenemos un circuito con dos condensadores en paralelo:
#
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensadores%20en%20paralelo.svg?sanitize=true)
#
# #### **Pregunta:** 
# 
# > Crea el netlist de este circuito e identifica qué condensador se satura primero. Dibuja la evolución de la intensidad en ambas ramas de manera simultánea. [Aquí](https://matplotlib.org/gallery/api/two_scales.html) tienes un ejemplo de cómo se hace esto en Matplotlib. Recuerda que para que Ahkab nos devuelva la corriente en una rama, debe de estar presente una pila. Si es necesario, inserta pilas virtuales de valor nulo (cero voltios), tal y como hemos comentado antes. Grafica también los voltajes (en otra gráfica, pero que aparezcan juntos).
# %% [markdown]
# #### **Respuesta:** 
# 
# Ambos se cargarán al mismo tiempo, debido a que están en paralelo entre sí y en serie con una resistencia común, lo que va a provocar que ambas tenga la misma tensión.# %%
%%writefile "files\carrera_de_condensadores.ckt"
* Carga condensador
v0 1 0 type=vdc vdc=10
r1 0 2 3.3k
c1 2 3 47u ic=0
v1dummy 3 1 type=vdc vdc=0
c2 2 4 22u ic=0
v2dummy 4 1 type=vdc vdc=0
.tran tstep=0.01 tstart=6.5 tstop=7.5 uic=0
.end
# %% [markdown]
# ### Procesamos el circuito con `Ahkab` y extraemos los datos.
# %%
# Procesar circuito
circuito_y_análisis = ahkab.netlist_parser.parse_circuit("files\carrera_de_condensadores.ckt")
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
figura = plt.figure()
plt.title("Carrera de condensadores")
plt.xlim(6.65, 7.5)
plt.ylim(0.0, 0.0005)
plt.grid()
plt.plot(list(map(lambda x: -x if x < 0 else x, resultados['tran']['T'])), 
    list(map(lambda x: -x if x < 0 else x, resultados['tran']['I(V1DUMMY)'])), 
    label="Intensidad en C1")
plt.plot(list(map(lambda x: -x if x < 0 else x, resultados['tran']['T'])), 
    list(map(lambda x: -x if x < 0 else x, resultados['tran']['I(V2DUMMY)'])), 
    label="Intensidad en C2")
# %%
tiempo = resultados['tran']['T']
f = lambda x: -x if x < 0 else x
i_C1 = resultados['tran']['I(V1DUMMY)']
i_C1 = list(map(f, i_C1))
i_C2 = resultados['tran']['I(V2DUMMY)']
i_C2 = list(map(f, i_C2))
i_R1 = resultados['tran']['I(V0)']
i_R1 = list(map(f, i_R1))

plot.rcParams['figure.figsize'] = [6.4*1.1, 4.8*1.2]
plot.rcParams['font.size'] = 12

fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc1 = plot.subplot(211)
line_iC1, = axc1.plot(tiempo, i_C1)
line_iC1.set_label('Corriente C1')
# line_iC1.set_c('tab:brown')
axc1.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc2 = plot.subplot(211)
line_iC2, = axc2.plot(tiempo, i_C2)
line_iC2.set_label('Corriente C2')
# line_iC2.set_c('tab:purple')
axc2.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc3 = plot.subplot(211)
line_iR1, = axc3.plot(tiempo, i_R1)
line_iR1.set_label('Corriente R1')
# line_iR1.set_c('tab:red')
axc3.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
plot.grid(True)
plot.tight_layout()
plot.show()

# %% [markdown]
# Se puede observar la corriente de ambos condensadores y la de la resistencia, que es la misma que la total del circuito, aunque su bajada es diferente, se acercan a cero practicamente a la vez.

# %%
tiempo = resultados['tran']['T']
v_R1 = resultados['tran']['V2']
v_C1 = resultados['tran']['V3']
v_C2 = resultados['tran']['V4']
f = lambda a, b: a - b
v_C1 = list(map(f, v_C1, v_R1))
v_C2 = list(map(f, v_C2, v_R1))

plot.rcParams['figure.figsize'] = [6.4*1.2, 4.8*1.3]
plot.rcParams['font.size'] = 12
fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1 = plot.subplot(211)
line_vC1, = axv1.plot(tiempo, v_C1)
line_vC1.set_label('Voltios C1')
line_vC1.set_c('tab:blue')
axv1.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1.grid(True)
axv3 = plot.subplot(211)
line_vR1, = axv3.plot(tiempo, v_R1)
line_vR1.set_label('Voltios R1')
line_vR1.set_c('tab:red')
axv3.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
axv2 = plot.subplot(212)
line_vC2, = axv2.plot(tiempo, v_C2)
line_vC2.set_label('Voltios C2')
line_vC2.set_c('tab:green')
axv2.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv3 = plot.subplot(212)
line_vR1, = axv3.plot(tiempo, v_R1)
line_vR1.set_label('Voltios R1')
line_vR1.set_c('tab:red')
axv3.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
plot.grid(True)
plot.tight_layout()
plt.savefig("test.svg", format="svg")
plot.rcParams['figure.figsize'] = [6.4, 4.8]
# {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}

# %% [markdown]
# Puesto que el voltaje de la fuente no cambia, se reparten la diferencia de potencial entre la resistencia y los dos condensadores.
# 
# #### Todas juntas.

# %%
fig, ax1 = plot.subplots()
ax2 = ax1.twinx()  
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$') 
ax1.set_xlabel('Tiempo (s)') 
ax1.set_ylabel('Corriente (A)')
ax2.set_ylabel('Voltios (V)')
ax1.tick_params(axis='y')#, labelcolor=color)
ax2.tick_params(axis='y')
ax1.grid(True)
line_iC1, = ax1.plot(tiempo, i_C1)
line_iC2, = ax1.plot(tiempo, i_C2)
line_iR1, = ax1.plot(tiempo, i_R1)
line_vC1, = ax2.plot(tiempo, v_C1)
line_vC2, = ax2.plot(tiempo, v_C2)
line_vR1, = ax2.plot(tiempo, v_R1)
line_iC1.set_c('tab:blue')
line_iC2.set_c('tab:orange')
line_iR1.set_c('tab:green')
line_vC1.set_c('tab:cyan')
line_vC2.set_c('tab:purple')
line_vR1.set_c('tab:red')

plot.legend(
    (line_iC1, line_iC2, line_iR1, line_vC1, line_vC2, line_vR1, ), 
    ("Corriente C1", "Corriente C2", "Corriente R1", "Voltios C1", "Voltios C2", "Voltios R1"))
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# %%









plot.rcParams['figure.figsize'] = [6.4*1.2, 4.8*1.3]
plot.rcParams['font.size'] = 12
fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1 = plot.subplot()
line_vC1, = axv1.plot(tiempo, v_C1)
line_vC1.set_label('Voltios C1')
line_vC1.set_c('tab:blue')
axv1.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1.grid(True)
axv3 = plot.subplot()
line_vR1, = axv3.plot(tiempo, v_R1)
line_vR1.set_label('Voltios R1')
line_vR1.set_c('tab:red')
axv3.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
axv2 = plot.subplot()
line_vC2, = axv2.plot(tiempo, v_C2)
line_vC2.set_label('Voltios C2')
line_vC2.set_c('tab:green')
axv2.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv3 = plot.subplot()
line_vR1, = axv3.plot(tiempo, v_R1)
line_vR1.set_label('Voltios R1')
line_vR1.set_c('tab:red')
axv3.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')

# plot.rcParams['legend.fontsize'] = 'large'
# plot.rcParams['figure.titlesize'] = 'medium'
fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc1 = plot.subplot()
line_iC1, = axc1.plot(tiempo, i_C1)
line_iC1.set_label('Corriente C1')
# line_iC1.set_c('tab:brown')
axc1.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc2 = plot.subplot()
line_iC2, = axc2.plot(tiempo, i_C2)
line_iC2.set_label('Corriente C2')
# line_iC2.set_c('tab:purple')
axc2.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc3 = plot.subplot()
line_iR1, = axc3.plot(tiempo, i_R1)
line_iR1.set_label('Corriente R1')
# line_iR1.set_c('tab:red')
axc3.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
plot.grid(True)
plot.tight_layout()
plot.show()



# %%
plot.legend()
plot.grid(True)
plot.tight_layout()
plt.savefig("test.svg", format="svg")
plot.rcParams['figure.figsize'] = [6.4, 4.8]
# {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}















# %% [markdown]
# ### **Ejercicio premium:** 
# 
# Repite la simulación con LTspice (invocándolo como comando externo, leyendo los datos de un fichero `.raw` y volviendo a graficar con Matplotlib.
# 
# ### Resolución del mismo circuito con LTspice
# 
# Vamos a adaptar el netlist para que sea compatible con LTspice.
# 
# 
# El efecto de la configuración del análisis `.tran` difiere bastante entre LTspice y Ahkab. 
# En Ahkab tenemos puesto:
# ````Ahkab
# .tran tstep=0.01 tstart=6.5 tstop=7.5 uic=0
# ````
# Esta configuración mantiene el circuito en reposo hasta que se alcanza `tstart` (6.5 seg.). Un instante antes se activa la pila y en el instante siguiente se inicia al mismo tiempo la simulación y las mediciones del análisis.
# 
# La expresión equivalente en LTspice sería la siguiente:
# ````LTspice
# .tran 0.01 7.5 6.5 uic
# ````
# Pero el efecto que tiene es totalmente diferente. En este caso LTspice, inicia la simulación en el instante 0, pero no comienza a tomar medidas hasta los 6.5 seg. y deja de tomar medias 1 seg. después de la primera medición. Por lo que para cuando se empieza muestrear la señal los condensadores ya están cargados.
# 
# Para simular un escenario similar al de la simulación con `Ahkab`, usaremos la opción PWL que permite establecer un voltaje concreto en el instante deseado.
#
# %% [markdown]
# ¿Como funciona PWL?
# 
# $\mathrm{PWL([T_1\ V_1]\ [T_2\ V_3]\ ...\ [T_n\ V_n]\ )}$
# 
# Se ponen números separados por espacios, que están relacionados por parejas, de modo que las posiciones impares representan un instante en el tiempo, y las posiciones pares el voltaje al que se pondrá la pila en ese instante.
# 
# Nuestra configuración va a estar construida por la combinación de PWL con el análisis `.tran`. 
# 
# * PWL: Esta configuración mantendrá la pila sin tensión hasta los 6.5 segundos, y en la décima de segundo siguiente se pondrá a 10 v.
# 
# ````PWL(6.5 0 6.51 10)````
# 
# * .tran: Esta configuración afectara de modo que, no se van a realizar mediciones hasta una décima de segundo antes de que se active la pila, y tomará medias cada décima de segundo hasta el segundo 8.
# 
# ````.tran 0 8 6.4 0.01 uic````

# %%
%%writefile "files\carrera_de_condensadores.net"
* Carga condensador
v0 1 0 PWL(6.5 0 6.51 10)
r1 2 0 3.3k
c1 1 2 47u
c2 1 2 22u 
.tran 0 8 6.4 0.01 uic
.end

# %% [markdown]
# Ejecutamos LTspice pasando al ejecutable el archivo que acabamos de crear como parametro.

# %%
# ############################################################
# lts "files\carrera_de_condensadores.net"
# ############################################################
if platform.system() == "Darwin":
    get_ipython().system('/Applications/LTspice.app/Contents/MacOS/LTspice -ascii -b files/carrera_de_condensadores.net')

if platform.system() == "Windows":
    get_ipython().system('"C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe" -ascii -b files\\carrera_de_condensadores.net')

# %% [markdown]
# Veamos el contenido del archivo, `.log`.
# 
# ## Contenido del `.log`:
# %%
get_ipython().run_line_magic('pycat', 'files\carrera_de_condensadores.log')
# %% [markdown]
# Ahora extraemos los datos del archivo `.raw`.

# %%
l = ltspice.Ltspice("files\carrera_de_condensadores.raw")
l.parse()

tiempo = l.get_time()
i_C1 = l.get_data('I(C1)')
i_C2 = l.get_data('I(C2)')
i_R1 = l.get_data('I(R1)')
v_R1 = l.get_data('V(2)')
vcc = l.get_data('V(1)')
v_Cs = l.get_data('V(1)')
f = lambda a, b: a - b
v_Cs = list(map(f, v_Cs, v_R1))

# %% [markdown]
# Dibujamos las gráficas con los datos obtenidos con LTspice.
# %%
plot.rcParams['figure.figsize'] = [6.4*1.1, 4.8*1.2]
plot.rcParams['font.size'] = 12
# plot.rcParams['legend.fontsize'] = 'large'
# plot.rcParams['figure.titlesize'] = 'medium'
fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc1 = plot.subplot(211)
line_iC1, = axc1.plot(tiempo, i_C1)
line_iC1.set_label('Corriente C1')
axc1.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc2 = plot.subplot(211)
line_iC2, = axc2.plot(tiempo, i_C2)
line_iC2.set_label('Corriente C2')
axc2.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axc3 = plot.subplot(211)
line_iR1, = axc3.plot(tiempo, i_R1)
line_iR1.set_label('Corriente R1')
axc3.set(xlabel='Tiempo (s)', 
    ylabel='Corriente (A)', 
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
plot.grid(True)
plot.tight_layout()
plot.show()

# %%
plot.rcParams['figure.figsize'] = [6.4*1.2, 4.8*1.3]
plot.rcParams['font.size'] = 12
# plot.rcParams['legend.fontsize'] = 'large'
# plot.rcParams['figure.titlesize'] = 'medium'
fig, ax = plot.subplots()
plot.title('Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
plot.legend()
axv2 = plot.subplot(211)
line_vC2, = axv2.plot(tiempo, v_Cs)
line_vC2.set_label('Voltios C1 y C2')
line_vC2.set_c('tab:green')
axv2.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv3 = plot.subplot(211)
line_vR1, = axv3.plot(tiempo, v_R1)
line_vR1.set_label('Voltios R1')
line_vR1.set_c('tab:red')
axv3.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1 = plot.subplot(211)
line_vC1, = axv1.plot(tiempo, vcc)
line_vC1.set_label('Voltios VCC')
line_vC1.set_c('tab:blue')
axv1.set(xlabel='Tiempo (s)', ylabel='Voltios (V)',
    title='Circuito carrera condensadores - ($\mathrm{10v}$) - C1:$\mathrm{47\mu\Omega}$ - C2:$\mathrm{22\mu\Omega}$')
axv1.grid(True)
plot.legend()
plot.grid(True)
plot.tight_layout()
plt.savefig("test.svg", format="svg")
plot.rcParams['figure.figsize'] = [6.4, 4.8]
# {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}

# %%













# %% [markdown]
# Esto habrá generado dos archivos, un `.log` y un .raw, con el resultado de la 
# %%
lts "files\carrera_de_condensadores.net"

# %%
get_ipython().system('"C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe" -ascii -b files\\circuito_sencillo.net')

# get_ipython().system('%windir%\\system32\\notepad.exe')
# %%
