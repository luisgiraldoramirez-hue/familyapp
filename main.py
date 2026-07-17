import flet as ft
import json

def main(page: ft.Page):
    page.title = "Laboratorio de Inglés - FamilyApp"
    page.window_width = 450
    page.window_height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # CARGA DE FRASES
    try:
        with open("frases.json", "r", encoding="utf-8") as archivo_json:
            datos_curso = json.load(archivo_json)
    except Exception:
        datos_curso = {
            "Principiantes": [{"en": "Coffee, please.", "pron": "kófi, plis.", "es": "Café, por favor."}],
            "Avanzados": [{"en": "I am looking for a job.", "pron": "ái ám lúking for e dchób.", "es": "Estoy buscando trabajo."}]
        }

    estado = {"nivel": "Principiantes", "indice": 0}

    # ELEMENTOS VISUALES
    txt_ingles = ft.Text(value=datos_curso["Principiantes"][0]["en"], size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    txt_pronunciacion = ft.Text(value=f"« {datos_curso['Principiantes'][0]['pron']} »", size=16, color="blue", italic=True, text_align=ft.TextAlign.CENTER)
    txt_espanol = ft.Text(value=datos_curso["Principiantes"][0]["es"], size=18, italic=True, text_align=ft.TextAlign.CENTER, visible=False)
    txt_resultado = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    
    def actualizar_pantalla():
        nivel = estado["nivel"]
        indice = estado["indice"]
        frase = datos_curso[nivel][indice]
        txt_ingles.value = frase["en"]
        txt_pronunciacion.value = f"« {frase.get('pron', '')} »"
        txt_espanol.value = frase["es"]
        txt_espanol.visible = False
        page.update()

    def revelar_clic(e):
        txt_espanol.visible = True
        page.update()

    def acierto_juego(e):
        nivel = estado["nivel"]
        indice = estado["indice"]
        if indice < len(datos_curso[nivel]) - 1:
            estado["indice"] = indice + 1
        else:
            estado["indice"] = 0
        actualizar_pantalla()

    page.add(
        ft.Text("Laboratorio de Inglés", size=14, color="grey"),
        ft.Container(height=20),
        txt_ingles,
        txt_pronunciacion,
        ft.Container(height=20),
        ft.ElevatedButton("👁️ Ver significado", on_click=revelar_clic),
        txt_espanol,
        ft.Container(height=20),
        ft.ElevatedButton("¡Lo logré! 🟢", on_click=acierto_juego)
    )

    actualizar_pantalla()

ft.app(target=main)
