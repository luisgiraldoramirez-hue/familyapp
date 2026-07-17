import flet as ft
import json
#import os

def main(page: ft.Page):
    page.title = "Laboratorio de Inglés - FamilyApp"
    page.window_width = 450
    page.window_height = 700
    # REPRODUCTOR WEB (Para que funcione en internet)
    audio_web = ft.Audio(autoplay=False)
    page.overlay.append(audio_web)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Cargar las frases desde el archivo JSON local
    try:
        with open("frases.json", "r", encoding="utf-8") as archivo_json:
            datos_curso = json.load(archivo_json)
    except Exception:
        # Copia de seguridad si no encuentra el archivo
        datos_curso = {
            "Principiantes": [{"en": "Coffee, please.", "pron": "kófi, plis.", "es": "Café, por favor."}],
            "Avanzados": [{"en": "I am looking for a job.", "pron": "ái ám lúking for e dchób.", "es": "Estoy buscando trabajo."}]
        }

    estado = {"nivel": "Principiantes", "indice": 0}

    nombres_etapas = {
        "Principiantes": "🌱 Nivel: Principiantes",
        "Avanzados": "🚀 Nivel: Avanzados"
    }

    # ELEMENTOS VISUALES (Volvemos al diseño original y limpio)
    txt_nivel_visible = ft.Text(value=nombres_etapas["Principiantes"], size=16, color="blue", weight=ft.FontWeight.BOLD)
    txt_ingles = ft.Text(value=datos_curso["Principiantes"][0]["en"], size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    txt_pronunciacion = ft.Text(value=f"« {datos_curso['Principiantes'][0]['pron']} »", size=16, color="blue", italic=True, text_align=ft.TextAlign.CENTER)
    txt_espanol = ft.Text(value=datos_curso["Principiantes"][0]["es"], size=18, italic=True, text_align=ft.TextAlign.CENTER, visible=False)
    
    txt_resultado = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    
    # Reproductores de audio locales (Cargan directo desde tu carpeta)
    audio_bing = ft.Audio(src="Bing mp3.mp3", autoplay=False)
    page.overlay.append(audio_bing)

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
        txt_nivel_visible.value = nombres_etapas[nivel]
        page.update()

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
        
        frase_url = frase.replace(" ", "%20")
        enlace_google = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={frase_url}"
        
        try:
            audio_web.src = enlace_google
            page.update()
            audio_web.play()
        except Exception as error:
            print(f"Error al reproducir en la web: {error}")
            
    def escuchar_alumno(e):
        txt_resultado.value = ""
        try:
            audio_bing.play()
        except Exception as error:
            print(f"Error al reproducir audio local: {error}")

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
            txt_resultado.value = "¡Es la única frase!"
        actualizar_pantalla()

    # BOTONES ORIGINALES
    btn_principiantes = ft.ElevatedButton("🌱 Principiantes", on_click=cambiar_a_principiantes)
    btn_avanzados = ft.ElevatedButton("🚀 Avanzados", on_click=cambiar_a_avanzados)
    
    btn_tutor =ft.ElevatedButton ("🔊 Escuchar Tutor", on_click=escuchar_tutor)
    btn_senal = ft.ElevatedButton("🔔 Sonar Señal", on_click=escuchar_alumno)
    btn_significado =ft.ElevatedButton("👁️ Ver Significado", on_click=revelar_clic)
    
    btn_no =ft.ElevatedButton("Aún no 🔴", on_click=fallo_juego)
    btn_si = ft.ElevatedButton("¡Lo logré! 🟢", on_click=acierto_juego)

    page.add(
        ft.Text("Laboratorio de Idiomas - Escritorio", size=12, color="grey"),
        ft.Row([btn_principiantes, btn_avanzados], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        txt_nivel_visible,
        ft.Container(
            content=ft.Column([
                txt_ingles,
                txt_pronunciacion,
                ft.Row([btn_tutor, btn_senal], alignment=ft.MainAxisAlignment.CENTER),
                txt_resultado,
                txt_espanol,
                btn_significado
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F0F0F0",
            border_radius=10
        ),
        ft.Container(height=10),
        ft.Text("¿Cómo estuvo tu pronunciación?", size=14, color="grey"),
        ft.Row([btn_no, btn_si], alignment=ft.MainAxisAlignment.CENTER)
    )
    actualizar_pantalla()

# CONFIGURACIÓN DE ESCRITORIO
ft.app(target=main)
