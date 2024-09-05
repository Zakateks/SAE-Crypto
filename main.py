import numpy as np
import streamlit as st
import pandas as pd

def imprimir_matriz_estetica(matriz, nombre="Matriz"):
    """Imprime la matriz de forma legible, como tablas con corchetes alineados."""
    max_width = max(len(str(int(num))) for fila in matriz for num in fila)
    st.write(f"### {nombre}")
    for fila in matriz:
        fila_str = " ".join(f"{int(num):{max_width}d}" for num in fila)
        st.text(f"[{fila_str}]")

def calcular_determinante_cofactores(matriz):
    """Calcula el determinante de una matriz usando el método de cofactores."""
    if len(matriz) == 1:
        return matriz[0][0]
    if len(matriz) == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    determinante = 0
    for c in range(len(matriz)):
        menor = [fila[:c] + fila[c+1:] for fila in matriz[1:]]
        cofactor = ((-1) ** c) * matriz[0][c] * calcular_determinante_cofactores(menor)
        determinante += cofactor
    
    return determinante

def calcular_matriz_inversa_modular(matriz, modulo):
    """Calcula la inversa de una matriz en un campo modular."""
    n = len(matriz)
    determinante = calcular_determinante_cofactores(matriz)
    determinante_mod = determinante % modulo
    
    # Asegurarse de que el determinante sea invertible bajo el módulo dado
    determinante_inverso = pow(determinante_mod, -1, modulo)
    
    # Calcular la matriz adjunta (transpuesta de la cofactor)
    matriz_adjunta = np.zeros_like(matriz)
    for i in range(n):
        for j in range(n):
            menor = [fila[:j] + fila[j+1:] for fila in (matriz[:i] + matriz[i+1:])]
            matriz_adjunta[j][i] = ((-1) ** (i + j)) * calcular_determinante_cofactores(menor)
    
    # Matriz inversa antes de aplicar el módulo
    matriz_inversa = determinante_inverso * matriz_adjunta
    
    # Matriz inversa en módulo
    matriz_inversa_mod = matriz_inversa % modulo
    
    return matriz_inversa, matriz_inversa_mod

def imprimir_matriz_inversa(matriz_inversa, matriz_inversa_mod, modulo):
    st.write(f"### Matriz inversa en módulo {modulo}")
    for fila_original, fila_mod in zip(matriz_inversa, matriz_inversa_mod):
        fila_original_str = " ".join(f"{int(num):6d}" for num in fila_original)
        fila_mod_str = " ".join(f"{int(num):2d}" for num in fila_mod)
        st.text(f"[{fila_original_str}]  mod({modulo})  =  [{fila_mod_str}]")

def crear_diccionario_valores():
    """Crea un diccionario asignando valores a cada letra del abecedario, incluyendo la ñ y el espacio."""
    abecedario = 'abcdefghijklmnñopqrstuvwxyz '
    diccionario = {letra: str(index).zfill(2) for index, letra in enumerate(abecedario)}
    return diccionario

def convertir_palabra_a_valores(palabra, diccionario):
    """Convierte una palabra a una lista de valores numéricos según el diccionario."""
    return [int(diccionario.get(letra, '00')) for letra in palabra]

def completar_palabra(palabra, longitud, relleno=" "):
    """Completa una palabra con un carácter de relleno hasta alcanzar la longitud deseada."""
    return palabra.ljust(longitud, relleno)

# Interfaz de Streamlit
st.title("Encriptación y Desencriptación con Matrices Modulares")

# Inicializar el estado del botón si no existe
if 'expandidos' not in st.session_state:
    st.session_state.expandidos = False

# Texto introductorio completo
texto_introductorio = """
En la historia, la criptografía se usó para asegurar mensajes entre militares y políticos, ocultando su contenido a quienes no estaban autorizados a leerlos. Aunque los métodos han evolucionado, el objetivo sigue siendo proteger la información y garantizar la privacidad.

Nuestra aplicación utiliza el cifrado de Hill, un método que emplea matrices para cifrar y descifrar mensajes. Los textos se convierten en bloques numéricos, se cifran con una matriz y se descifran utilizando la matriz inversa.

Hoy en día, el cifrado de Hill se utiliza principalmente con fines educativos. Los métodos más avanzados, como el cifrado RSA, son los que se emplean en aplicaciones críticas, como la seguridad de transacciones financieras en línea y comunicaciones digitales.
"""

# Texto parcial
texto_parcial = texto_introductorio.split("\n\n")[0] + "..."

# Mostrar el texto y el botón
if st.session_state.expandidos:
    st.write(texto_introductorio)
    boton_texto = "Leer menos"
else:
    st.write(texto_parcial)
    boton_texto = "Leer más"

if st.button(boton_texto):
    st.session_state.expandidos = not st.session_state.expandidos
    # Actualizar el texto del botón para el siguiente clic
    st.experimental_rerun()

st.write("### Diccionario de Valores Asignados")
st.write("""
Para comenzar con el proceso de encriptado, primero debemos asignar un valor numérico a cada carácter del alfabeto. Esto nos permitirá convertir el texto en una representación numérica que puede ser procesada por la matriz de cifrado.
""")

# Crear diccionario de valores para el abecedario
diccionario_valores = crear_diccionario_valores()

# Mostrar la tabla con los valores asignados a cada carácter en formato horizontal
tabla_valores_horizontal = pd.DataFrame(diccionario_valores.items(), columns=['Carácter', 'Valor']).T
st.table(tabla_valores_horizontal)

st.write("""
Analizando nuestra tabla de caracteres, tenemos un total de 28, ya que estamos contando el espacio " " como caracter. Por lo tanto nuestras matrices las ejecutaremos tomando en cuenta la cantidad de caracteres, es decir en modulo 28.
""")

# Crear dos columnas del mismo tamaño
col1, col2 = st.columns(2)

with col1:
    # Primer rectángulo: número de entrada para el tamaño de la matriz
    tamano = st.number_input("‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎  Introduce el tamaño de la matriz (n x n):", min_value=1, max_value=10, value=3)

with col2:
    # Texto antes del botón de generación automática con tamaño de letra ajustado
    st.markdown(
        """
        <div style="font-size:18px;">
        ‎ ‎ ‎ ‎ ‎ 
        </div>
        """,
        unsafe_allow_html=True
    )
    # Botón para generar automáticamente
    if st.button("‎ ‎‎ ‎‎ ‎‎ ‎‎ ‎Generar matriz automáticamente‎ ‎‎ ‎‎ ‎‎ ‎‎ ‎"):
        st.write(f"El tamaño de la matriz es: {tamaño}")


# Leer la matriz del usuario
st.write(f"Introduce los elementos de la matriz {tamano}x{tamano}, fila por fila:")
matriz = []
for i in range(tamano):
    fila = st.text_input(f"Fila {i + 1} (separada por espacios):")
    if fila:
        matriz.append(list(map(int, fila.split())))

if len(matriz) == tamano:
    # Imprimir la matriz clave
    imprimir_matriz_estetica(matriz, "Clave (K)")

    # Calcular y mostrar el determinante usando el método de cofactores
    determinante_cofactores = calcular_determinante_cofactores(matriz)
    st.write(f"### Determinante (usando método de cofactores): {determinante_cofactores}")

    # Calcular el determinante en módulo 28
    determinante_mod_28 = determinante_cofactores % 28
    st.write(f"### Determinante en módulo 28: {determinante_mod_28}")

    # Calcular la matriz inversa en módulo 28
    try:
        matriz_inversa, matriz_inversa_mod = calcular_matriz_inversa_modular(matriz, 28)
    except ValueError:
        matriz_inversa, matriz_inversa_mod = None, None
        st.write("No se puede calcular la matriz inversa: el determinante no es invertible bajo el módulo 28.")

    # Preguntar al usuario qué palabra desea encriptar
    palabra = st.text_input("¿Qué palabra deseas encriptar?").lower()

    if palabra:
        # Completar la palabra a una longitud adecuada para la matriz
        longitud_palabra = tamano ** 2
        palabra_completa = completar_palabra(palabra, longitud_palabra)

        # Convertir la palabra completa a valores numéricos
        valores_palabra = convertir_palabra_a_valores(palabra_completa, diccionario_valores)

        if len(valores_palabra) == longitud_palabra:
            # Crear la matriz de nxn a partir de los valores de la palabra completa
            matriz_columna = np.array(valores_palabra).reshape(tamano, tamano)
            
            # Mostrar la multiplicación paso a paso
            st.write("### Proceso de encriptación:")
            st.write(f"Multiplicando la Clave (K) por los valores de la palabra '{palabra_completa.upper()}':")
            
            # Realizar la multiplicación
            resultado = np.dot(matriz, matriz_columna)
            resultado_mod_28 = resultado % 28  # Aplicar módulo 28

            # Convertir el resultado en letras usando el diccionario inverso
            diccionario_inverso = {v: k for k, v in diccionario_valores.items()}
            letras_resultado = []
            for num in resultado_mod_28.flatten():
                letra = diccionario_inverso[str(int(num)).zfill(2)].upper()
                letras_resultado.append(letra if letra != ' ' else '-')

            # Mostrar el resultado con la matriz de letras
            for i in range(tamano):
                fila_matriz = " ".join(f"{int(num):2d}" for num in matriz[i])
                fila_valor = " ".join(f"{valores_palabra[j]:02d}" for j in range(i*tamano, (i+1)*tamano))
                resultado_nums = " ".join(f"{int(resultado[i][j]):02d}" for j in range(tamano))
                resultado_mods = " ".join(f"{int(resultado_mod_28[i][j]):02d}" for j in range(tamano))
                letras = " ".join(letras_resultado[i*tamano:(i+1)*tamano])
                st.text(f"[{fila_matriz}] x [{fila_valor}] = [{resultado_nums}] ⇒ [{resultado_nums}] mod(28) = [{resultado_mods}] [{letras}]")

            # Mostrar la matriz inversa si se calculó exitosamente
            if matriz_inversa_mod is not None:
                imprimir_matriz_inversa(matriz_inversa, matriz_inversa_mod, 28)
                
                # Multiplicar la matriz inversa por el resultado encriptado
                resultado_desencriptado = np.dot(matriz_inversa_mod, resultado_mod_28)
                resultado_desencriptado_mod_28 = resultado_desencriptado % 28
                
                # Convertir el resultado desencriptado en letras
                letras_desencriptadas = []
                for num in resultado_desencriptado_mod_28.flatten():
                    letra = diccionario_inverso[str(int(num)).zfill(2)].upper()
                    letras_desencriptadas.append(letra if letra != ' ' else '-')
                
                # Mostrar el proceso de desencriptación
                st.write("### Proceso de desencriptación:")
                for i in range(tamano):
                    fila_inversa = " ".join(f"{int(num):2d}" for num in matriz_inversa_mod[i])
                    resultado_mod = " ".join(f"{int(resultado_mod_28[i][j]):02d}" for j in range(tamano))
                    desencriptado_nums = " ".join(f"{int(resultado_desencriptado[i][j]):02d}" for j in range(tamano))
                    desencriptado_mods = " ".join(f"{int(resultado_desencriptado_mod_28[i][j]):02d}" for j in range(tamano))
                    letras_desencriptadas_fila = " ".join(letras_desencriptadas[i*tamano:(i+1)*tamano])
                    st.text(f"[{fila_inversa}] x [{resultado_mod}] = [{desencriptado_nums}] ⇒ [{desencriptado_nums}] mod(28) = [{desencriptado_mods}] [{letras_desencriptadas_fila}]")

