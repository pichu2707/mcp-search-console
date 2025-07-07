# MCP Server para Google Search Console

Este código está basado en el código de [Github de Guchey](https://github.com/guchey/mcp-server-google-search-console) donde vamos a tener un MCP que nos conecte **Claude Desktop** para poderlo utilizar de herramienta.

## Características
* Recuperar datos de analítica de búsqueda (con soporte de dimensión)
* Análisis detallado con los períodos de información

## Prerrequisitos
* Python 3.10 o superior
* Proyecto de Google Cloud con la API de Google Search Console
* Credenciales de la cuenta de servicio con acceso a Search Console

## Instalación

### Creando un entorno virtual con **uv**

**Windows:**
```shell
uv venv
.venv\Scripts\activate
```

**Linux o Bash:**
```bash
uv venv
source .venv/bin/activate
```

### Instalación de dependencias 
```bash
pip install "mcp[cli]"
```

## Configuración de la autenticación

Para obtener las credenciales de la API de Google Search Console:

### 1. Acceder a Google Cloud Console
* Ir a [Google Cloud Console](https://console.cloud.google.com/)
* Crear un nuevo proyecto o seleccionar uno existente

### 2. Habilitar la API
* Ir a "APIs y servicios" > "Biblioteca"
* Buscar y habilitar "Google Search Console API"

### 3. Crear credenciales
* Ir a "APIs y servicios" > "Credenciales"
* Hacer clic en "Crear credenciales" > "Cuenta de servicio"
* Ingresar los detalles de la cuenta de servicio
* Crear una nueva clave en formato JSON
* El archivo de credenciales (.json) se descargará automáticamente

### 4. Conceder acceso
* Abrir [Google Search Console](https://search.google.com/search-console)
* Agregar la dirección de correo electrónico de la cuenta de servicio como administrador
* Formato: `nombre@proyecto.iam.gserviceaccount.com`

## Configuración de Claude Desktop

Agregar esta configuración a tu archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gsc": {
      "command": "C:\\Users\\[TU_USUARIO]\\ruta\\al\\proyecto\\.venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "mcp_server_gsc",
        "--credentials",
        "C:\\Users\\[TU_USUARIO]\\ruta\\al\\archivo\\credentials.json"
      ]
    }
  }
}
```

**Nota:** Reemplaza `[TU_USUARIO]` y las rutas con tus rutas específicas.

## Uso

Una vez configurado, puedes usar las siguientes funciones en Claude:

* **Obtener datos de Search Console** para tu sitio web
* **Analizar rendimiento de búsqueda** con diferentes dimensiones
* **Consultar métricas específicas** por períodos de tiempo

## Licencia
MIT