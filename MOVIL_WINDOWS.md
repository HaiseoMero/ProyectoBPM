# Vócalis en el teléfono

## Abrir el proyecto

1. Conecta el teléfono al mismo Wi-Fi que el computador. El computador también puede estar conectado por cable al mismo router.
2. Abre **INICIAR_PROYECTO_WIFI.cmd** en la carpeta del proyecto.
3. En el navegador del teléfono, abre la dirección que muestra la ventana, por ejemplo `http://192.168.100.126:5173/`. Usa siempre la dirección del arranque actual: puede cambiar al reconectarte.

El computador debe permanecer encendido y el proyecto debe estar funcionando. En el computador puedes seguir usando `http://localhost:5173/`.

**INICIAR_PROYECTO.cmd** inicia el modo local. Cambiar entre los dos archivos reinicia únicamente el frontend registrado por el script; conserva la API, MySQL y Camunda. Si Vite fue iniciado manualmente en otra terminal, cierra esa terminal antes de usar los archivos de arranque.

## Si el teléfono no logra conectarse

- Comprueba que usas la dirección del computador y el puerto **5173**.
- Usa una red doméstica marcada como **Privada** en Windows. Una red de invitados o con aislamiento entre dispositivos puede impedir la conexión.
- Si el firewall bloquea el puerto, abre PowerShell **como administrador** y ejecuta una vez:

```powershell
New-NetFirewallRule -Name 'Vocalis-Wifi-5173' -DisplayName 'Vocalis Wi-Fi local' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5173 -Profile Private -RemoteAddress LocalSubnet -Program 'C:\Program Files\nodejs\node.exe'
```

Para quitar esa regla cuando ya no la necesites:

```powershell
Remove-NetFirewallRule -Name 'Vocalis-Wifi-5173'
```

La implementación no cambia las reglas del firewall automáticamente.

## Comprobarlo desde el teléfono

1. Revisa la portada y los enlaces **Cómo funciona** y **El test**.
2. Ingresa con tu cuenta o prueba el registro.
3. Abre el panel y la bitácora; gira el teléfono y comprueba que se conserva el contenido.
4. En un cuestionario pendiente, selecciona una respuesta, espera el aviso de guardado y recarga: la respuesta debe conservarse.
5. Abre un reporte y despliega sus dimensiones. En una cuenta de orientador, comprueba la búsqueda, curso, estado y acceso al reporte del alumno.

Se comprobaron estos flujos en navegadores con tamaños de teléfono y una API de prueba. La conexión desde un teléfono físico se confirma abriendo la dirección anterior; no puede comprobarse únicamente con las pruebas del computador.

## Cerrar y volver a abrir

- Abre **DETENER_PROYECTO.cmd** para cerrar los procesos del proyecto y detener MySQL cuando tengas permiso.
- Vuelve a abrir **INICIAR_PROYECTO.cmd** para uso local o **INICIAR_PROYECTO_WIFI.cmd** para el teléfono.

## Configuración para desarrollo

- La configuración local del frontend usa `VITE_API_BASE_URL=/api`. La plantilla es `.env.example`.
- Vite reenvía `/api` a `http://127.0.0.1:8000`. El backend conserva su arranque en `127.0.0.1`; no hace falta abrir su puerto en el teléfono ni cambiar CORS.
- `VOCALIS_API_PROXY_TARGET` permite cambiar el destino del proxy, por ejemplo para una API de prueba en otro puerto. No incluye el sufijo `/api`.
- Las herramientas de Vue en la página se habilitan de forma opcional con `VOCALIS_DEVTOOLS=1` antes de iniciar Vite.
- `npm run build` genera la versión compilada y `npm run preview` la muestra localmente en el puerto 4173, usando el mismo proxy. Para publicar en un servidor propio hay que configurar allí `/api` o indicar `VITE_API_BASE_URL` antes de compilar.

Referencias de configuración: [servidor y proxy de Vite](https://vite.dev/config/server-options), [vista previa de Vite](https://vite.dev/config/preview-options), [reglas del firewall en Windows](https://learn.microsoft.com/powershell/module/netsecurity/new-netfirewallrule).
