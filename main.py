import flet as ft
from gtts import gTTS
import os
from playsound import playsound
import json
import speech_recognition as sr
import winsound  #  "Bing"

def main(page: ft.Page):
    page.title = "Laboratorio de Ingles - FamilyApp"
    page.window_width = 460
    page.window_height = 760 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    #  Autor
    marca_agua = ft.Text(
        "El taller del Orfebre",
        style=ft.TextThemeStyle.BODY_SMALL,
        opacity=0.3,          # marca de agua
        italic=True,          
        color=ft.Colors.GREY_400
    )
    
    
    # FRASES 
    try:
        with open("frases.json", "r", encoding="utf-8") as archivo_json:
            datos_curso = json.load(archivo_json)
    except Exception:
        # Respaldo de seguridad si el archivo JSON falla
        datos_curso = {
            "Principiantes": [{"en": "Coffee, please.", "pron": "kófi, plis.", "es": "Café, por favor."}],
            "Avanzados": [{"en": "I am looking for a job.", "pron": "ái ám lúking for e dchób.", "es": "Estoy buscando trabajo."}]
        }

    # Control de nivel ( arranca directo en Principiantes)
    estado = {"nivel": "Principiantes", "indice": 0}

   
    nombres_etapas = {
        "Principiantes": "🌱 Nivel: Principiantes (Presente, Pasado y Futuro)",
        "Avanzados": "🚀 Nivel: Avanzados (Situaciones Complejas)"
    }

    # ELEMENTOS VISUALES
    txt_nivel_visible = ft.Text(value=nombres_etapas["Principiantes"], size=16, color="blue", weight=ft.FontWeight.BOLD)
    txt_ingles = ft.Text(value=datos_curso["Principiantes"][0]["en"], size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    txt_pronunciacion = ft.Text(value=f"« {datos_curso['Principiantes'][0]['pron']} »", size=16, color="blue", italic=True, text_align=ft.TextAlign.CENTER)
    txt_espanol = ft.Text(value=datos_curso["Principiantes"][0]["es"], size=18, italic=True, text_align=ft.TextAlign.CENTER, visible=False)
    
    txt_tu_voz = ft.Text(value="Tu transcripción aparecerá aquí...", size=16, color="grey", italic=True, text_align=ft.TextAlign.CENTER)
    txt_resultado = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    
    def actualizar_pantalla():
        nivel = estado["nivel"]
        indice = estado["indice"]
        
        if indice >= len(datos_curso[nivel]):
            estado["indice"] = 0
            indice = 0
            
        frase = datos_curso[nivel][indice]
        
        txt_ingles.value = frase["en"]
        txt_pronunciacion.value = f"« {frase.get('pron', '')} »"
        txt_espanol.value = frase["es"]
        txt_espanol.visible = False
        
        txt_tu_voz.value = "Tu transcripción aparecerá aquí..."
        txt_tu_voz.color = "grey"
        txt_nivel_visible.value = nombres_etapas[nivel]
        page.update()

    # NAVEGACIÓN  (SOLO DOS BOTONES)
    def cambiar_a_principiantes(e):
        txt_resultado.value = ""
        estado["nivel"] = "Principiantes"
        estado["indice"] = 0
        actualizar_pantalla()

    def cambiar_a_avanzados(e):
        txt_resultado.value = ""
        estado["nivel"] = "Avanzados"
        estado["indice"] = 0
        actualizar_pantalla()

    # AUDIO TUTOR
    def escuchar_tutor(e):
        nivel = estado["nivel"]
        indice = estado["indice"]
        frase = datos_curso[nivel][indice]["en"]
        
        archivo = "tutor_temp.mp3"
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
            except Exception:
                pass 
        
        tts = gTTS(text=frase, lang='en', tld='com')
        tts.save(archivo)
        try:
            playsound(archivo)
        except Exception as error:
            print(f"Error al reproducir: {error}")

    # MICRÓFONO 
    def escuchar_alumno(e):
        txt_resultado.value = ""
        txt_tu_voz.value = "Calibrando silencio... ¡Espera un segundo!"
        txt_tu_voz.color = "orange"
        page.update()
        
        r = sr.Recognizer()
        
        with sr.Microphone(device_index=2) as origen:
            r.adjust_for_ambient_noise(origen, duration=0.5)
            r.dynamic_energy_threshold = True
            r.pause_threshold = 1.5
        
        # cambiar!
        winsound.Beep(1200, 250) 
        
        txt_tu_voz.value = "¡¡ HABLA AHORA !! 🎤"
        txt_tu_voz.color = "red"
        page.update()
        
        with sr.Microphone(device_index=2) as origen:
            try:
                audio = r.listen(origen, timeout=5, phrase_time_limit=5)
                txt_tu_voz.value = "Procesando tu voz..."
                txt_tu_voz.color = "blue"
                page.update()
                
                texto_dicho = r.recognize_google(audio, language="en-US")
                
                txt_tu_voz.value = f'Dijiste: "{texto_dicho}"'
                txt_tu_voz.color = "black"
                
                frase_correcta = txt_ingles.value.lower().replace(".", "").replace("?", "").replace(",", "").strip()
                frase_usuario = texto_dicho.lower().replace(".", "").replace("?", "").replace(",", "").strip()
                
                if frase_usuario == frase_correcta:
                    txt_resultado.value = "¡Perfecto! 🟢 Excelente pronunciación."
                    txt_resultado.color = "green"
                else:
                    txt_resultado.value = "Casi... 🔴 Inténtalo de nuevo."
                    txt_resultado.color = "red"
                    
            except sr.WaitTimeoutError:
                txt_tu_voz.value = "Error: Se agotó el tiempo. No se escuchó nada."
                txt_tu_voz.color = "red"
            except sr.UnknownValueError:
                txt_tu_voz.value = "Error: Presta atencion a la pronunciación e inténtalo de nuevo!"
                txt_tu_voz.color = "red"
            except Exception as error:
                txt_tu_voz.value = f"Error del micrófono: {error}"
                txt_tu_voz.color = "red"
        
        page.update()

    def revelar_clic(e):
        txt_espanol.visible = True
        page.update()

    def acierto_juego(e):
        txt_resultado.value = ""
        nivel = estado["nivel"]
        indice = estado["indice"]
        if indice < len(datos_curso[nivel]) - 1:
            estado["indice"] = indice + 1
        else:
            estado["indice"] = 0
        actualizar_pantalla()

    def fallo_juego(e):
        nivel = estado["nivel"]
        indice = estado["indice"]
        if len(datos_curso[nivel]) > 1:
            frase_rebelde = datos_curso[nivel].pop(indice)
            datos_curso[nivel].append(frase_rebelde)
            txt_resultado.value = "↩️ La dejamos para el final."
            txt_resultado.color = "orange"
        else:
            txt_resultado.value = "¡Es la única frase de este nivel! Practícala."
            txt_resultado.color = "blue"
        actualizar_pantalla()

    # NUEVA FILA DE BOTONES EN LA INTERFAZ
    fila_niveles = ft.Row(
        controls=[
            ft.Button("🌱 Principiantes", on_click=cambiar_a_principiantes),
            ft.Button("🚀 Avanzados", on_click=cambiar_a_avanzados),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    fila_juego = ft.Row(
        controls=[
            ft.Button("Aún no 🔴", on_click=fallo_juego),
            ft.Button("¡Lo logré! 🟢", on_click=acierto_juego),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

     
    page.add(
        ft.Text("Motor Sistemático de Aprendizaje - FamilyApp", size=14, color="grey"),
        fila_niveles,
        ft.Container(height=15),
        txt_nivel_visible,
        ft.Container(
            content=ft.Column([
                txt_ingles,
                txt_pronunciacion,
                ft.Container(height=5),
                ft.Button("🔊 Escuchar Tutor", on_click=escuchar_tutor),
                ft.Container(height=10),
                
            
                ft.Container(
                    content=ft.Text("🎙️ Empezar a Hablar", color="white", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    bgcolor="blue",
                    padding=ft.Padding.symmetric(vertical=12, horizontal=24),
                    border_radius=8,
                    on_click=escuchar_alumno,
                    width=220
                ),
               
                txt_tu_voz,
                txt_resultado,
                
                ft.Container(height=10),
                txt_espanol,
                ft.Button("👁️  Significado", on_click=revelar_clic),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="lightgrey",
            border_radius=10,
            width=420
        ),
        ft.Container(height=15),
        ft.Text("¿Cómo estuvo tu pronunciación?", size=14, color="grey"),
        fila_juego
    ) #  Este paréntesis cierra el page.add 

    actualizar_pantalla()


ft.app(target=main, view=ft.AppView.WEB_BROWSER)