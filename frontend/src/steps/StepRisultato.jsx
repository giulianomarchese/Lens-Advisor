export default function StepRisultato({ risultato, onRestart }) {
  if (!risultato) return <div>Caricamento...</div>;

  const lv = risultato.livello_consigliato;
  const nome = risultato.nome_commerciale;
  const desc = risultato.descrizione_commerciale;
  const vantaggi = risultato.vantaggi || [];
  const alternative = risultato.alternative || [];
  const trattamenti = risultato.trattamenti_preselezionati || [];
  const tratInfo = risultato.trattamenti_info || {};

  function buildMotivazione() {
    const parti = [];
    if (risultato.hard_triggers > 0) {
      parti.push(`${risultato.hard_triggers} parametro/i critico/i nella prescrizione`);
    }
    if (risultato.soft_triggers > 0) {
      parti.push(`${risultato.soft_triggers} parametro/i di attenzione`);
    }
    if (risultato.delta_questionario > 0) {
      parti.push(`profilo paziente che richiede maggiore personalizzazione (+${risultato.delta_questionario})`);
    }
    if (risultato.pd_anomalo) {
      parti.push('distanza interpupillare fuori norma');
    }
    if (parti.length === 0) {
      parti.push('prescrizione nella norma, profilo standard');
    }
    return parti;
  }

  const motivazioni = buildMotivazione();

  return (
    <div className="result-container">
      {/* Main recommendation */}
      <div className="card result-main">
        <div className="result-level">
          <div className={`level-badge l${lv}`}>L{lv}</div>
          <div className="level-info">
            <h2>{nome}</h2>
            <p className="level-desc">{desc}</p>
          </div>
        </div>

        {vantaggi.length > 0 && (
          <ul className="vantaggi-list">
            {vantaggi.map((v, i) => (
              <li key={i}>{v}</li>
            ))}
          </ul>
        )}
      </div>

      {/* Motivation */}
      <div className="card">
        <div className="motivation">
          <h4>Perché questo livello</h4>
          <p>
            Il motore ha analizzato la prescrizione (base tecnica: L{risultato.livello_base_trigger})
            e il profilo del paziente per determinare il livello ottimale.
          </p>
          <div style={{ marginTop: 8 }}>
            {motivazioni.map((m, i) => (
              <span key={i} className="tag">{m}</span>
            ))}
          </div>
          <p style={{ marginTop: 12, fontSize: 13, color: 'var(--text-light)' }}>
            Indice suggerito: <strong>{risultato.indice_suggerito}</strong>
          </p>
        </div>
      </div>

      {/* Pre-selected treatments */}
      {trattamenti.length > 0 && (
        <div className="card">
          <h4 style={{ marginBottom: 12, color: 'var(--primary)' }}>Trattamenti consigliati</h4>
          {trattamenti.map(trt => {
            const info = tratInfo[trt] || {};
            return (
              <div key={trt} style={{ marginBottom: 8 }}>
                <strong style={{ fontSize: 14 }}>{info.nome || trt}</strong>
                <p style={{ fontSize: 13, color: 'var(--text-light)' }}>
                  {info.descrizione || ''}
                </p>
              </div>
            );
          })}
        </div>
      )}

      {/* Alternatives */}
      {alternative.length > 0 && (
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <h4 style={{ marginBottom: 12, color: 'var(--primary)' }}>Alternative disponibili</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 12 }}>
            {alternative.map(alt => (
              <div key={alt.livello} className={`alternative-card ${alt.is_l1 ? 'is-l1' : ''}`}>
                <span className={`alt-badge ${alt.tipo}`}>{alt.tipo}</span>
                <h4>L{alt.livello} — {alt.nome}</h4>
                <p>{alt.descrizione}</p>
                {alt.is_l1 && (
                  <p style={{ fontSize: 12, color: 'var(--warn)', marginTop: 4, fontWeight: 600 }}>
                    Opzione economica — non consigliata dal motore
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Restart */}
      <div style={{ gridColumn: '1 / -1', textAlign: 'center', paddingTop: 12 }}>
        <button className="btn btn-outline" onClick={onRestart}>
          Nuova consulenza
        </button>
      </div>
    </div>
  );
}
