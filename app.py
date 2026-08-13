import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Título
st.title("Servicio de Soporte Técnico en la Nube")

# 1. Usuario completa el formulario
with st.form("form_reporte"):
    nombre = st.text_input("Nombre del usuario")
    correo_usuario = st.text_input("Correo del usuario")
    tipo_problema = st.selectbox(
        "Tipo de problema",
        ["Conexión", "Aplicación", "Cuenta", "Otro"]
    )
    prioridad = st.selectbox(
        "Prioridad",
        ["Alta", "Media", "Baja"]
    )
    descripcion = st.text_area("Descripción de la incidencia")

    enviar = st.form_submit_button("ENVIAR REPORTE")


# 2. Validación y envío
if enviar:

    if nombre and correo_usuario and descripcion:

        # Preparar mensaje
        mensaje = f"""
Nuevo reporte de soporte técnico:

- Usuario: {nombre}
- Correo: {correo_usuario}
- Tipo de problema: {tipo_problema}
- Prioridad: {prioridad}
- Descripción: {descripcion}
"""

        # Configuración de correo usando secrets
        remitente = st.secrets["email"]["user"]
        clave = st.secrets["email"]["password"]
        destinatario = st.secrets["email"]["admin"]

        # Crear mensaje con codificación UTF-8
        msg = MIMEText(mensaje, "plain", "utf-8")

        # Asunto con UTF-8
        msg["Subject"] = Header(
            "Nuevo reporte de soporte técnico",
            "utf-8"
        )

        # Direcciones
        msg["From"] = formataddr(("Servicio de Soporte Técnico", remitente))
        msg["To"] = destinatario

        try:
            # Conexión con Gmail
            with smtplib.SMTP("smtp.gmail.com", 587) as server:

                server.ehlo()
                server.starttls()
                server.ehlo()

                # Inicio de sesión
                server.login(remitente, clave)

                # Enviar mensaje
                server.send_message(
                    msg,
                    from_addr=remitente,
                    to_addrs=[destinatario]
                )

            st.success(
                "¡Reporte enviado correctamente! "
                "Su reporte ha sido enviado al administrador."
            )

        except Exception as e:
            st.error(f"Error al enviar el reporte: {e}")

    else:
        st.warning("Por favor complete todos los campos obligatorios.")

