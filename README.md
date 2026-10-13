# La Bandita 🎬🐾

Serie original de historias cómicas y absurdas con pequeños momentos de drama. Personajes recurrentes: Krono (pastor alemán), Issi (beagle), Pepa (beagle angelical), Kuky y Zeus (gatos).

## Pipeline audiovisual

El workflow La Bandita | Generar episodio crea un vídeo con ilustraciones originales generadas por código, narración en español con voces diferenciadas por personaje, subtítulos y metadatos. No necesita API de pago.

### Ejecutar
1. Abre Actions.
2. Selecciona La Bandita | Generar episodio.
3. Pulsa Run workflow.
4. Elige un episodio (pizza, veterinario, kuky) y formato (short o largo).
5. Descarga el artefacto generado y revisa el resultado antes de publicarlo.

También se ejecuta al cambiar guiones, el generador o el workflow.

## Salida
- MP4 H.264/AAC, vertical 9:16 para Shorts o horizontal 16:9 para episodios largos.
- Subtítulos SRT y metadatos JSON.
- Imágenes originales estilizadas creadas por el pipeline.

## Límites y calidad
La primera versión produce animación tipo cuento con ilustraciones 2D, paneo/zoom, voz TTS local y subtítulos. No crea animación 3D cinematográfica ni usa la imagen subida como referencia automática. Revisa pronunciación, sincronización, personajes y derechos antes de publicar. La voz sintética es temporal y se puede sustituir por grabaciones propias o un proveedor autorizado.

No publica en YouTube automáticamente ni promete viralidad o monetización. La publicación automática requerirá configurar OAuth de YouTube como secretos de GitHub y validar permisos.

## Estructura
- episodes/: historias en JSON.
- scripts/build_episode.py: generación de ilustraciones, voces y vídeo.
- .github/workflows/build-episode.yml: automatización.
- dist/: artefactos temporales de ejecución, no versionados.
