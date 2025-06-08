# MCP Server para Google Search Console

Este código está basado en el código de [Github de Guchey]('https://github.com/guchey/mcp-server-google-search-console') donde vamos a tener un MCP que nos conecte **Claude Desktop** para poderlo utilizar de herramienta.

## Caractéristicas
* Recuperar datos de analíticade búsqueda (con soporte de dimensión)
* Análisis detallado con los periodos de información

## Prerrequisitos
* Python 3.10 o superior
* Proyecto de Google Cloud con la API de Google Search Console
* Credenciales de la cuenta de servicio con acceso a Search Console

## Instalación
Creando un entorno virtual con **uv**
Windows
```shell
uv venv
.venv\Script\activate
```

Linux o Bash
```bash
uv venv
source .venv/bin/activate
```

## Instalación de dependencias 

### Instalando el paquete MCP por separado
```pip install "mcp[cli]"```

## Configuración de la autentificación

Para obtener las credenciales de la API de Google Search Console:

Acceder a la consola de [Google Cloud]('https://console.cloud.google.com/')
* Crea un nuevo proyecto o selecciona uno existente
* Habilitar la API:
  * Vaya a "API y servicios" > "Biblioteca".
* Busque y habilite "API de Search Console"
Crear credenciales:
* Vaya a "API y servicios" > "Credenciales".
  * Haga clic en "Crear credenciales" > "Cuenta de servicio".
* Ingrese los detalles de la cuenta de servicio
* Crear una nueva clave en formato JSON
* El archivo de credenciales (.json) se descargará automáticamente
Conceder acceso:
* Abrir Search Console
  * Agregue la dirección de correo electrónico de la cuenta de servicio (formato: nombre@proyecto.iam.gserviceaccount.com ) como administrador de la propiedad


## Configuración de la aplicación de escritorio de Claude
```json
{
  "mcpServers": {
    "gsc": {
            "command": "C:\\Users\\pichu\\OneDrive\\Documentos\\MCP\\mcp-gsc\\mcp-server-google-search-console\\.venv\\Scripts\\python.exe",
            "args": [
            "-m",
            "mcp_server_gsc",
            "--credentials",
            "C:\\Users\\pichu\\OneDrive\\Documentos\\MCP\\mcp-gsc\\credentials\\credentials.json"
            ]
        }
      }
}
```

## Licencia
MIT

