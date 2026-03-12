import { useState } from 'react';

const DOMANDE = [
  {
    id: 'q0p',
    titolo: 'Età del paziente',
    sottotitolo: 'Inserisci l\'età anagrafica',
    tipo: 'number',
    min: 10,
    max: 99,
    default: 45,
    skippable: false,
  },
  {
    id: 'q1',
    titolo: 'Tipo di occhiale',
    sottotitolo: 'Che utilizzo avrà questo paio?',
    tipo: 'scelta',
    opzioni: [
      { value: 'principale', label: 'Occhiale principale' },
      { value: 'secondo_paio', label: 'Secondo paio' },
      { value: 'sole', label: 'Occhiale da sole' },
    ],
    default: 'principale',
    skippable: false,
  },
  {
    id: 'q2',
    titolo: 'Vita digitale',
    sottotitolo: 'Quanto tempo passa davanti a schermi digitali?',
    tipo: 'slider',
    min: 0,
    max: 3,
    labels: ['Poco', 'Moderato', 'Molto', 'Intensivo'],
    default: 1,
    skippable: true,
  },
  {
    id: 'q3',
    titolo: 'Guida',
    sottotitolo: 'Il paziente guida regolarmente?',
    tipo: 'scelta',
    opzioni: [
      { value: true, label: 'Sì, guida regolarmente' },
      { value: false, label: 'No, non guida' },
    ],
    default: false,
    skippable: true,
  },
  {
    id: 'q4',
    titolo: 'Lettura e lavoro da vicino',
    sottotitolo: 'Quanto tempo dedica alla lettura o lavori da vicino?',
    tipo: 'slider',
    min: 0,
    max: 3,
    labels: ['Poco', 'Moderato', 'Molto', 'Intensivo'],
    default: 1,
    skippable: true,
  },
  {
    id: 'q5',
    titolo: 'Lente office / occupazionale',
    sottotitolo: 'Il paziente lavora prevalentemente in ufficio?',
    tipo: 'scelta',
    opzioni: [
      { value: 'attivo', label: 'Sì, lavoro da ufficio prevalente' },
      { value: 'non_attivo', label: 'No, attività variegate' },
    ],
    default: null,
    skippable: true,
  },
  {
    id: 'q6',
    titolo: 'Fastidi visivi',
    sottotitolo: 'Il paziente lamenta disturbi visivi?',
    tipo: 'scelta',
    opzioni: [
      { value: 'nessuno', label: 'Nessun fastidio' },
      { value: 'signal', label: 'Qualche fastidio saltuario' },
      { value: 'combined', label: 'Fastidi multipli frequenti' },
      { value: 'luci_fari', label: 'Problemi con luci e fari' },
    ],
    default: 'nessuno',
    skippable: true,
  },
  {
    id: 'q7',
    titolo: 'Esperienza con progressive',
    sottotitolo: 'Ha già portato lenti progressive?',
    tipo: 'scelta',
    opzioni: [
      { value: 'prima_volta', label: 'Prima volta in assoluto' },
      { value: 'da_poco', label: 'Da poco tempo' },
      { value: 'da_anni', label: 'Da anni, con esperienza' },
    ],
    default: 'da_anni',
    skippable: true,
  },
  {
    id: 'q8',
    titolo: 'Caratteristica più importante',
    sottotitolo: 'Cosa conta di più per il paziente?',
    tipo: 'scelta',
    opzioni: [
      { value: 'comfort', label: 'Comfort visivo' },
      { value: 'sottili', label: 'Lenti sottili e leggere' },
      { value: 'protezione', label: 'Protezione e durabilità' },
      { value: 'riflessi', label: 'Eliminare i riflessi' },
      { value: 'prezzo', label: 'Miglior rapporto qualità/prezzo' },
    ],
    default: 'comfort',
    skippable: true,
  },
  {
    id: 'q9',
    titolo: 'Protezione aggiuntiva',
    sottotitolo: 'Interesse per protezioni specifiche?',
    tipo: 'scelta',
    opzioni: [
      { value: 'nessuna', label: 'Nessuna in particolare' },
      { value: 'luce_blu', label: 'Filtro luce blu' },
      { value: 'fotocromatico', label: 'Lente fotocromatica' },
      { value: 'uv', label: 'Protezione UV avanzata' },
    ],
    default: 'nessuna',
    skippable: true,
  },
];

export default function StepQuestionario({ data, onUpdate, onNext, onBack }) {
  const [currentQ, setCurrentQ] = useState(0);
  const domanda = DOMANDE[currentQ];
  const totalQ = DOMANDE.length;

  function answer(value) {
    onUpdate({ ...data, [domanda.id]: value });
    if (currentQ < totalQ - 1) {
      setCurrentQ(currentQ + 1);
    } else {
      onNext();
    }
  }

  function skip() {
    onUpdate({ ...data, [domanda.id]: null });
    if (currentQ < totalQ - 1) {
      setCurrentQ(currentQ + 1);
    } else {
      onNext();
    }
  }

  function goBack() {
    if (currentQ > 0) {
      setCurrentQ(currentQ - 1);
    } else {
      onBack();
    }
  }

  return (
    <div className="question-page">
      {/* Progress dots */}
      <div className="q-progress">
        {DOMANDE.map((_, i) => (
          <div
            key={i}
            className={`q-progress-dot ${i < currentQ ? 'done' : ''} ${i === currentQ ? 'current' : ''}`}
          />
        ))}
      </div>

      <h2>{domanda.titolo}</h2>
      <p className="q-subtitle">{domanda.sottotitolo}</p>

      {/* Number input (Q0P) */}
      {domanda.tipo === 'number' && (
        <NumberQuestion
          domanda={domanda}
          value={data[domanda.id] ?? domanda.default}
          onChange={v => onUpdate({ ...data, [domanda.id]: v })}
          onConfirm={() => answer(data[domanda.id] ?? domanda.default)}
        />
      )}

      {/* Choice options */}
      {domanda.tipo === 'scelta' && (
        <div className="q-options">
          {domanda.opzioni.map(opt => (
            <div
              key={String(opt.value)}
              className={`q-option ${data[domanda.id] === opt.value ? 'selected' : ''}`}
              onClick={() => answer(opt.value)}
            >
              {opt.label}
            </div>
          ))}
        </div>
      )}

      {/* Slider */}
      {domanda.tipo === 'slider' && (
        <SliderQuestion
          domanda={domanda}
          value={data[domanda.id] ?? domanda.default}
          onChange={v => onUpdate({ ...data, [domanda.id]: v })}
          onConfirm={() => answer(data[domanda.id] ?? domanda.default)}
        />
      )}

      <div className="btn-bar" style={{ justifyContent: 'center', gap: 16 }}>
        <button className="btn btn-outline" onClick={goBack}>
          Indietro
        </button>
        {domanda.skippable && (
          <button className="btn btn-skip" onClick={skip}>
            Salta
          </button>
        )}
        {(domanda.tipo === 'number' || domanda.tipo === 'slider') && (
          <button
            className="btn btn-primary"
            onClick={() => answer(data[domanda.id] ?? domanda.default)}
          >
            Conferma
          </button>
        )}
      </div>
    </div>
  );
}

function NumberQuestion({ domanda, value, onChange, onConfirm }) {
  return (
    <div className="q-slider-container">
      <div className="slider-value">{value}</div>
      <input
        type="range"
        min={domanda.min}
        max={domanda.max}
        value={value}
        onChange={e => onChange(parseInt(e.target.value))}
      />
      <div className="slider-labels">
        <span>{domanda.min}</span>
        <span>{domanda.max}</span>
      </div>
    </div>
  );
}

function SliderQuestion({ domanda, value, onChange }) {
  return (
    <div className="q-slider-container">
      <div className="slider-value">{domanda.labels[value]}</div>
      <input
        type="range"
        min={domanda.min}
        max={domanda.max}
        value={value}
        onChange={e => onChange(parseInt(e.target.value))}
      />
      <div className="slider-labels">
        <span>{domanda.labels[0]}</span>
        <span>{domanda.labels[domanda.labels.length - 1]}</span>
      </div>
    </div>
  );
}
