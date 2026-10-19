const translations = {
  fr: {
    eyebrow: 'CAPACITÉS · PREUVES · FRAÎCHEUR',
    title: 'Une promesse. Son test. Sa limite.',
    lede: 'Explorez les chantiers, ouvrez les versions vérifiées et retrouvez les preuves exécutées. Une inspection, un téléchargement ou une dépendance déclarée ne deviennent pas un utilisateur par magie.',
    inspect: 'Choisir une preuve',
    projects: 'Projets',
    coverage: 'Couverture',
    usage: 'Déclarations d’usage',
    freshness: 'Fraîcheur',
    filter: 'Portefeuille concerné',
    all: 'Tous les portefeuilles',
    download: 'Exporter le registre',
    recorded:
      'Observations datées du 19 octobre 2026. Aucun rafraîchissement réseau automatique. Les vérifications CLI sont explicites et sans authentification pour les sources publiques.',
    bounded: 'OBSERVATIONS BORNÉES',
    covered: 'chantiers reproduits / prévus',
    audits: 'roues et sources accessibles sans compte',
    removeProof: 'Simuler le retrait de la preuve du premier projet',
    coverageExplain:
      'La simulation retire ses reçus de démonstration, tests unitaires et navigateur. Le registre original reste intact. Un résultat manquant ou une autre révision ne compte pas comme terminé.',
    notAdoption: 'Une déclaration de dépendance reste une déclaration.',
    noPortfolioUse:
      'Aucune preuve d’adoption humaine de ces projets n’est établie par ce registre. L’absence de déclaration collectée ne prouve pas l’absence d’usage.',
    methodOnly:
      'Validation de la méthode sur un dépôt tiers : read-with-jev déclare le SDK TypeSafe. Ce n’est pas une preuve d’adoption des projets gbesse. Propriétaires GitHub différents ne prouvent pas des organisations indépendantes.',
    freshExplain:
      'Une preuve peut continuer à passer alors que sa source a changé. Le contrat relie l’empreinte de source à un reproducteur précis ; un changement impose la revue.',
    sourceChanged: 'Simuler une source modifiée',
    replayFailed: 'Simuler un reproducteur en échec',
    freshCheck: 'Vérifier le contrat synthétique',
    simulation:
      'Les deux cases modifient un exemple synthétique local. Elles ne prétendent pas qu’un amont réel a changé ou échoué.',
    snapshots: 'Observations réelles de sources publiées',
    limits:
      'Les reçus sont des observations locales, pas des attestations indépendantes signées. Les tests de chaque capacité et leurs limites restent liés au dépôt. Vues, clones, étoiles, propriétaires et bots ne prouvent pas une adoption humaine. Aucun label SOTA n’est attribué.',
    release: 'Version et roue',
    source: 'Sources',
    ci: 'CI de la version',
    replay: 'Rejouer',
    verified: 'Reproduit',
    missing: 'Preuve manquante',
    self: 'Atlas : empreinte des fichiers du paquet ; sa CI propre valide cette version.',
    declared: 'Version déclarée',
    scope: 'Portée',
    runtime: 'exécution réelle non démontrée',
    current_and_reproduced: 'Source identique et reproducteur réussi',
    source_changed_requires_review: 'Source modifiée : revue requise, même si le test passe',
    reproduction_failed: 'Reproducteur en échec',
    current_not_replayed: 'Source identique ; pas de rejeu',
    ready: 'Registre chargé.',
    error: 'Preuve indisponible.',
  },
  en: {
    eyebrow: 'CAPABILITIES · EVIDENCE · FRESHNESS',
    title: 'A promise. Its test. Its limit.',
    lede: 'Explore workstreams, open verified releases and trace executed evidence. Inspection, downloads or dependency declarations do not magically become users.',
    inspect: 'Choose evidence',
    projects: 'Projects',
    coverage: 'Coverage',
    usage: 'Usage declarations',
    freshness: 'Freshness',
    filter: 'Relevant portfolio',
    all: 'All portfolios',
    download: 'Export ledger',
    recorded:
      'Observations dated 19 October 2026. No automatic network refresh. Public-source CLI verification is explicit and unauthenticated.',
    bounded: 'BOUNDED OBSERVATIONS',
    covered: 'reproduced / planned workstreams',
    audits: 'wheels and sources accessible without account',
    removeProof: 'Simulate removing evidence for the first project',
    coverageExplain:
      'Simulation removes its demo, unit and browser receipts. Original ledger stays intact. Missing evidence or another revision never counts as completed.',
    notAdoption: 'A dependency declaration remains a declaration.',
    noPortfolioUse:
      'This ledger establishes no human adoption of these projects. Missing collected declarations do not establish nonuse.',
    methodOnly:
      'Method validation on a third-party repository: read-with-jev declares the TypeSafe SDK. This is not adoption of gbesse projects. Different GitHub owners do not establish independent organizations.',
    freshExplain:
      'A test can keep passing after its source changes. A contract binds the source fingerprint to a pinned reproducer; changes require review.',
    sourceChanged: 'Simulate changed source',
    replayFailed: 'Simulate failing reproducer',
    freshCheck: 'Check synthetic contract',
    simulation:
      'The checkboxes modify a local synthetic example. They do not claim a real upstream changed or failed.',
    snapshots: 'Actual observations of published sources',
    limits:
      'Receipts are local observations, not independently signed attestations. Capability tests and limits remain linked to each repository. Views, clones, stars, owner visits and bots do not establish human adoption. No SOTA label is assigned.',
    release: 'Release and wheel',
    source: 'Source',
    ci: 'Release CI',
    replay: 'Replay',
    verified: 'Reproduced',
    missing: 'Missing evidence',
    self: 'Atlas: package-file fingerprint; its own CI validates this release.',
    declared: 'Declared version',
    scope: 'Scope',
    runtime: 'runtime execution not proven',
    current_and_reproduced: 'Matching source and successful reproducer',
    source_changed_requires_review: 'Source changed: review required even when test passes',
    reproduction_failed: 'Reproducer failed',
    current_not_replayed: 'Matching source; no replay',
    ready: 'Ledger loaded.',
    error: 'Evidence unavailable.',
  },
  es: {
    eyebrow: 'CAPACIDADES · PRUEBAS · VIGENCIA',
    title: 'Una promesa. Su prueba. Su límite.',
    lede: 'Explore líneas de trabajo, abra versiones verificadas y encuentre pruebas ejecutadas. Una inspección, descarga o dependencia declarada no se convierte mágicamente en usuario.',
    inspect: 'Elegir prueba',
    projects: 'Proyectos',
    coverage: 'Cobertura',
    usage: 'Declaraciones de uso',
    freshness: 'Vigencia',
    filter: 'Portafolio afectado',
    all: 'Todos los portafolios',
    download: 'Exportar registro',
    recorded:
      'Observaciones del 19 de octubre de 2026. Sin actualización automática por red. Verificación CLI pública explícita y sin autenticación.',
    bounded: 'OBSERVACIONES ACOTADAS',
    covered: 'líneas reproducidas / previstas',
    audits: 'ruedas y fuentes accesibles sin cuenta',
    removeProof: 'Simular retirada de pruebas del primer proyecto',
    coverageExplain:
      'La simulación retira recibos de demo, pruebas unitarias y navegador. El registro original no cambia. Prueba ausente u otra revisión no cuenta como terminado.',
    notAdoption: 'Una dependencia declarada sigue siendo una declaración.',
    noPortfolioUse:
      'Este registro no demuestra adopción humana de estos proyectos. La ausencia de declaraciones recopiladas no demuestra falta de uso.',
    methodOnly:
      'Validación del método en un repositorio tercero: read-with-jev declara el SDK TypeSafe. No demuestra adopción de proyectos gbesse. Propietarios GitHub distintos no demuestran organizaciones independientes.',
    freshExplain:
      'Una prueba puede seguir pasando aunque cambie su fuente. El contrato vincula la huella a un reproductor fijado; los cambios exigen revisión.',
    sourceChanged: 'Simular fuente modificada',
    replayFailed: 'Simular reproductor fallido',
    freshCheck: 'Verificar contrato sintético',
    simulation:
      'Las casillas modifican un ejemplo sintético local. No afirman cambios ni fallos de un proyecto real.',
    snapshots: 'Observaciones reales de fuentes publicadas',
    limits:
      'Recibos como observaciones locales, no certificaciones independientes firmadas. Pruebas y límites vinculados a cada repositorio. Vistas, clones, estrellas, visitas del propietario y bots no demuestran adopción humana. Sin etiqueta SOTA.',
    release: 'Versión y rueda',
    source: 'Fuentes',
    ci: 'CI de la versión',
    replay: 'Repetir',
    verified: 'Reproducido',
    missing: 'Prueba ausente',
    self: 'Atlas: huella de archivos del paquete; su propia CI valida esta versión.',
    declared: 'Versión declarada',
    scope: 'Alcance',
    runtime: 'ejecución real no demostrada',
    current_and_reproduced: 'Fuente idéntica y reproductor correcto',
    source_changed_requires_review: 'Fuente modificada: revisión necesaria aunque pase la prueba',
    reproduction_failed: 'Reproductor fallido',
    current_not_replayed: 'Fuente idéntica; sin reproducción',
    ready: 'Registro cargado.',
    error: 'Prueba no disponible.',
  },
};
const language = new URLSearchParams(location.search).get('lang') || 'en',
  lang = translations[language] ? language : 'en',
  t = translations[lang];
document.documentElement.lang = lang;
document.querySelectorAll('[data-i18n]').forEach((e) => (e.textContent = t[e.dataset.i18n]));
const $ = (id) => document.getElementById(id);
let data,
  view = 'projects';
function el(tag, text, cls) {
  const n = document.createElement(tag);
  n.textContent = text;
  if (cls) n.className = cls;
  return n;
}
function link(text, url) {
  const a = el('a', text);
  if (typeof url === 'string' && url.startsWith('https://github.com/')) {
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
  }
  return a;
}
function renderCards() {
  const project = $('project-filter').value,
    allowed = new Set(
      data.requirements
        .filter((r) => project === 'all' || r.project === project)
        .map((r) => r.repository),
    );
  $('cards').replaceChildren();
  for (const card of data.cards) {
    if (!allowed.has(card.repository)) continue;
    const div = el('section', '', 'card');
    div.dataset.repo = card.repository;
    div.append(
      el('h3', card.repository.split('/')[1]),
      el('p', card.summary[lang]),
      el('code', card.commit),
      el('p', card.limits[lang], 'hint'),
    );
    if (card.module) div.append(el('pre', `python3 -m ${card.module} demo`));
    else div.append(el('p', t.self, 'hint'));
    div.append(
      link(t.source, `https://github.com/${card.repository}`),
      link(t.release, card.release),
    );
    if (card.ci?.length) div.append(link(t.ci, card.ci[0]));
    $('cards').append(div);
  }
}
function renderCoverage(report) {
  $('coverage-count').textContent = `${report.reproduced}/${report.total}`;
  $('requirements').replaceChildren();
  const project = $('project-filter').value;
  for (const r of report.requirements) {
    if (project !== 'all' && r.project !== project) continue;
    const div = el('section', '', `topic ${r.status}`);
    div.append(
      el('strong', `${r.id} · ${r.title[lang]}`),
      el('p', `${r.repository} · ${r.status === 'reproduced' ? t.verified : t.missing}`),
    );
    if (r.test_ref) div.append(link(r.test_ref.name, r.test_ref.url));
    $('requirements').append(div);
  }
}
function select(next) {
  view = next;
  for (const name of ['projects', 'coverage', 'usage', 'freshness'])
    $(`panel-${name}`).hidden = name !== next;
  $('panel-title').textContent = t[next];
}
async function post(path, body) {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw Error();
  return response.json();
}
$('remove-proof').onchange = async () => {
  try {
    renderCoverage(await post('/api/coverage-demo', { remove_first: $('remove-proof').checked }));
  } catch {
    $('status').textContent = t.error;
  }
};
$('fresh-check').onclick = async () => {
  try {
    const result = await post('/api/freshness-demo', {
      changed: $('source-changed').checked,
      replay_passed: !$('replay-failed').checked,
    });
    $('fresh-result').textContent = t[result.status];
    $('fresh-result').dataset.status = result.status;
    $('fresh-result').classList.toggle('warn', result.status !== 'current_and_reproduced');
  } catch {
    $('status').textContent = t.error;
  }
};
for (const name of ['projects', 'coverage', 'usage', 'freshness'])
  $(`tab-${name}`).onclick = () => select(name);
$('project-filter').onchange = () => {
  renderCards();
  $('remove-proof').onchange();
};
$('download').onclick = () => {
  if (!data) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }),
    ),
    a = document.createElement('a');
  a.href = url;
  a.download = 'oss-evidence-ledger.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
try {
  data = await (await fetch('/api/portfolio')).json();
  $('projects-count').textContent = data.cards.length;
  $('audits-count').textContent = data.anonymous_audits.filter((a) => a.passed).length;
  renderCards();
  renderCoverage(data.summary.coverage);
  for (const record of data.manifest_records) {
    for (const claim of record.claims) {
      const div = el('section', '', 'proof');
      div.append(
        el('h3', claim.repository),
        el('p', `${claim.dependency.name} · ${t.declared}: ${claim.dependency.declared_version}`),
        el('p', `${claim.dependency.scope} · ${t.runtime}`),
        link(t.source, claim.source_url),
      );
      $('declarations').append(div);
    }
  }
  for (const record of data.source_freshness || []) {
    const div = el('section', '', 'proof');
    div.append(
      el('strong', record.contract.reproducer.repository),
      el('p', t[record.result.status]),
    );
    $('source-records').append(div);
  }
  await $('fresh-check').onclick();
  select('projects');
  $('status').textContent = t.ready;
} catch {
  $('status').textContent = t.error;
}
