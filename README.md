# Mi Blog

Blog desarrollado con Django 5.2 que incluye un listado de posts, una página
"About", un ranking de posts populares (por número de visitas) y la creación de
posts desde el sitio por usuarios autenticados.

## Requisitos

- Python 3.10 o superior
- pip

## Cómo levantar el proyecto

1. Clona o entra al directorio del proyecto:

   ```bash
   cd blog_test
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Aplica las migraciones:

   ```bash
   python manage.py migrate
   ```

5. Crea un superusuario para acceder al admin y poder iniciar sesión:

   ```bash
   python manage.py createsuperuser
   ```

6. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

7. Abre el navegador en <http://127.0.0.1:8000/>.

## Rutas principales

| Ruta | Descripción |
| --- | --- |
| `/` | Listado de todos los posts publicados |
| `/post/<slug>/` | Detalle del post (registra una visita) |
| `/populares/` | Posts ordenados por número de visitas |
| `/about/` | Información del blog |
| `/post/nuevo/` | Crear un post (requiere iniciar sesión) |
| `/accounts/login/` | Inicio de sesión |
| `/admin/` | Panel de administración de Django |

## Ejecutar las pruebas

```bash
python manage.py test
```

## Estructura del proyecto

```
blog_test/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── blog/                        # App principal del blog
│   ├── admin.py                 # Registro de Post y Visita en el admin
│   ├── forms.py                 # PostForm (creación de posts)
│   ├── models.py                # Modelos Post y Visita
│   ├── urls.py                  # Rutas de la app (namespace "blog")
│   ├── views.py                 # Listado, detalle, populares, about y crear
│   ├── tests.py                 # Pruebas de vistas y modelos
│   └── migrations/              # Migraciones de la base de datos
├── blog_test/                   # Configuración del proyecto Django
│   ├── settings.py              # Apps, templates, media, idioma, auth
│   ├── urls.py                  # URLs raíz + admin + accounts + media
│   ├── asgi.py
│   └── wsgi.py
├── templates/                   # Templates globales
│   ├── base.html                # Layout con navbar y Bootstrap 5
│   ├── blog/
│   │   ├── post_list.html       # Listado de posts
│   │   ├── post_detail.html     # Detalle del post
│   │   ├── popular_posts.html   # Ranking de más visitados
│   │   ├── post_form.html       # Formulario de creación
│   │   ├── about.html           # Página About
│   │   └── _pagination.html     # Paginación reutilizable
│   └── registration/
│       └── login.html           # Inicio de sesión
├── static/                      # Archivos estáticos propios
└── media/                       # Archivos subidos (imágenes de posts)
    └── posts/
```

## Modelos

- **Post**: `titulo`, `slug` (único y automático), `autor`, `resumen`,
  `contenido`, `imagen`, `publicado`, `creado`, `actualizado`.
- **Visita**: `post`, `fecha`, `ip`, `user_agent`. Se crea una por cada
  apertura del detalle de un post.

## Notas

- El contador de "populares" se calcula agregando las visitas de cada post.
- La creación de posts y el admin requieren autenticación.
- Las imágenes se guardan en `media/posts/` y solo se sirven con `DEBUG = True`.
- Este proyecto usa la base de datos SQLite incluida por defecto.
