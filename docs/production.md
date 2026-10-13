# Guía de producción

## Personajes y voces
- Krono: protector, voz grave.
- Issi: rápida y curiosa.
- Pepa: cálida y angelical, alas blancas y aureola dorada.
- Kuky: teatral y dramática.
- Zeus: calmado y sarcástico.
- Narrador: expresivo, ritmo ágil.

El pipeline inicial utiliza variantes de voz local de espeak-ng. Son voces provisionales para validar el flujo, no voces de calidad profesional. Para una versión definitiva se pueden reemplazar los WAV por grabaciones propias o voces sintéticas con licencia comercial adecuada.

## Cómo añadir un episodio
Copia uno de los JSON de episodes/, cambia id, title, description y las escenas. Cada escena necesita speaker, text y characters. Los nombres válidos son Krono, Issi, Pepa, Kuky y Zeus. Para narración usa NARRADOR.

## Control de calidad
Antes de publicar, comprobar nombres y pronunciación en español, coherencia de personajes, sincronización de voces y subtítulos, volumen, duración, miniatura, título, descripción y licencias de recursos. El workflow no publica automáticamente en YouTube.
