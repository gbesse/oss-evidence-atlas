# OSS Evidence Atlas

[Français](README.md) · [English](README.en.md)

**Vincular cada línea de trabajo a un entregable y sus pruebas; distinguir visibilidad, dependencias declaradas y adopción.**

Doce herramientas nuevas y el propio motor de pruebas: **trece proyectos, veintiséis líneas**, con capacidades distintas en repositorios compartidos. Conserva versiones, huellas, recibos y límites. Las pruebas ausentes siguen visibles; una inspección no se convierte en mejora.

## Probar

Python 3.11+; galería con registro guardado, sin clave ni actualización automática por red.

```sh
git clone https://github.com/gbesse/oss-evidence-atlas
cd oss-evidence-atlas
python3 -m evidence_atlas serve --lang es
```

Abrir `http://127.0.0.1:8775/?lang=es`. Explorar proyectos y versiones, filtrar portafolios, simular retirada de pruebas, inspeccionar una declaración y cambiar un contrato sintético de vigencia. El motor recalcula cobertura y vigencia; no son dibujos prefijados.

```sh
python3 -m evidence_atlas demo
```

`pip install .` instala `evidence-atlas`. Interfaz, errores, fichas y documentación FR/EN/ES. Nombres de proyectos, identificadores y datos citados sin cambios.

![Galería](docs/preview-fr.png)

## Tres tipos de prueba

**Capacidad reproducida.** Cada herramienta tiene commit Git fijado, enlaces CI y tres recibos nuevos: demostración con aserciones, suite unitaria sin omisiones y recorrido navegador. Se ejecutaron realmente doce demos, doce suites y doce navegadores. SQL debe encontrar un contraejemplo y salir con 1; es estado esperado, no error ignorado arbitrariamente. Pruebas específicas en cada repositorio; un smoke test no demuestra todas sus propiedades.

Seis líneas transversales corresponden al atlas: cobertura exhaustiva, galería ejecutable, declaraciones, reproducción registrada, vigencia y acceso anónimo. Sus recibos se vinculan a SHA-256 de archivos Python/JS/HTML/CSS del paquete, **no a un commit autorreferencial ficticio**. Cambiarlos invalida los recibos; la CI propia complementa esa autoevaluación. Registro y recibos son observaciones locales, no certificaciones independientes firmadas.

**Dependencia declarada.** Lee `package.json` o dependencias PEP 621 de `pyproject.toml`; primero fija commit y conserva ruta, huella y versión declarada. Distingue runtime/desarrollo/opcional/peer, mismo propietario GitHub y fork. Deduplica observaciones repetidas. Un rango no es versión resuelta. No infiere alias, transitividad, archivos dinámicos ni instalación real.

Prueba real del método: `carlaiau/read-with-jev` declara `@typesafe-ai/sdk` versión `0.6.0` en manifiesto público fijado. **No demuestra adopción de proyectos gbesse** ni número de personas usando el lector. El campo npm `private` no vuelve privado el repositorio GitHub. Aquí no se demuestra adopción humana de los proyectos gbesse. Propietarios distintos no demuestran organizaciones independientes; ausencia de declaraciones recopiladas no demuestra falta de uso.

```sh
pip install .
python3 -m evidence_atlas collect carlaiau/read-with-jev package.json npm @typesafe-ai/sdk typesafe-ai
```

**Vigencia y acceso.** Un contrato vincula huella de fuente con repositorio, commit y control de reproducción. Fuente modificada exige revisión aunque pase el test. Fuente igual + fallo significa reproducción fallida. Sin recibo no se afirma reproducción. Rechaza recibos de otra revisión. Observaciones de fuentes publicadas reales; los interruptores modifican un ejemplo sintético sin afirmar cambios reales de otro proyecto.

```sh
python3 -m evidence_atlas freshness contrato.json fuente-local receipt.json
python3 -m evidence_atlas audit ficha.json
```

La auditoría descarga fuente al commit y rueda de versión **sin autenticación**, comparando ambos SHA-256. Las doce ruedas y fuentes métier se verificaron así. La rueda del atlas se audita tras publicarse y no cuenta entre esas doce observaciones. Red explícita, TLS verificado, hosts GitHub permitidos, timeout y límites de tamaño. No requiere clave GitHub ni Jev.

## Repetir una herramienta

Exportar una entrada `cards` a `ficha.json`, preparar checkout al commit indicado e instalar dependencias. El entorno Python debe contener las del proyecto; para navegador también paquetes npm y Chromium.

```sh
python3 -m evidence_atlas replay ficha.json /ruta/checkout demo
python3 -m evidence_atlas replay ficha.json /ruta/checkout unit
python3 -m evidence_atlas replay ficha.json /ruta/checkout browser
```

Verifica commit, remote y árbol limpio; ejecuta **solo el comando registrado en código**. Nunca ejecuta órdenes shell de un documento, README o manifiesto. No transmite credenciales ni variables secretas. Las doce demos usan datos sintéticos y no controlan sistemas reales. Timeout de 120 segundos por control; salidas con huella, nunca interpretadas como instrucciones.

## Fuentes, comparaciones y límites

[GitHub ya construye grafos desde manifiestos](https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security). El atlas ofrece una observación pequeña, exportable y fijada de un paquete objetivo, no sustituye ese grafo. [GitHub informa aparte de vistas y visitantes](https://docs.github.com/en/rest/metrics/traffic). Esos números, clones, estrellas, visitas del propietario y bots no demuestran adopción humana ni se convierten en usuarios.

Enfoque **línea → versión → prueba → límite**, con vigencia y descarga anónima. Sin descubrimiento exhaustivo de consumidores, identidad humana verificada, cualificación operativa, benchmark SOTA ni certificación criptográfica independiente. Ejercicios acotados; consultar límites de cada repositorio. No envía mensajes sociales, emails ni contactos a mantenedores.

## Verificar

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Dieciséis pruebas: alcances, normalización, duplicados, forks, ausencia de pruebas, recopilación pública fijada, URL prohibidas, huellas, recibos obsoletos, cobertura incompleta e invalidación propia. Navegador FR/EN/ES: galería, veintiséis líneas, prueba retirada, declaración limitada, fuente cambiada, reproducción fallida, exportación, filtros y móvil. CI Python 3.11/3.12, construcción y rueda fuera de fuentes. MIT; alfa pública.
