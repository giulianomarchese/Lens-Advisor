import { useState } from 'react';
import StepPrescrizione from './steps/StepPrescrizione';
import StepQuestionario from './steps/StepQuestionario';
import StepRisultato from './steps/StepRisultato';

const INITIAL_RX = {
  sph_od: 0, sph_os: 0,
  cyl_od: 0, cyl_os: 0,
  ax_od: null, ax_os: null,
  add: 0, pd: null,
  video_centratore: false,
};

const INITIAL_Q = {
  q0p: 45, q1: 'principale', q2: 1, q3: false, q4: 1,
  q5: null, q6: 'nessuno', q7: 'da_anni', q8: 'comfort', q9: 'nessuna',
};

const STEPS = [
  { num: 3, label: 'Prescrizione' },
  { num: 4, label: 'Questionario' },
  { num: 5, label: 'Risultato' },
];

export default function App() {
  const [step, setStep] = useState(0); // 0=prescrizione, 1=questionario, 2=risultato
  const [rx, setRx] = useState(INITIAL_RX);
  const [questionario, setQuestionario] = useState(INITIAL_Q);
  const [risultato, setRisultato] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function calcola() {
    setLoading(true);
    setError(null);
    try {
      const body = {
        rx: {
          sph_od: rx.sph_od,
          sph_os: rx.sph_os,
          cyl_od: rx.cyl_od,
          cyl_os: rx.cyl_os,
          ax_od: rx.ax_od,
          ax_os: rx.ax_os,
          add: rx.add,
          pd: rx.pd,
        },
        questionario: questionario,
        video_centratore: rx.video_centratore || false,
      };
      const res = await fetch('/api/calcola', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`Errore server: ${res.status}`);
      const data = await res.json();
      setRisultato(data);
      setStep(2);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function restart() {
    setStep(0);
    setRx(INITIAL_RX);
    setQuestionario(INITIAL_Q);
    setRisultato(null);
    setError(null);
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Lens Advisor</h1>
        <div className="step-indicator">
          {STEPS.map((s, i) => (
            <div
              key={s.num}
              className={`step-dot ${i === step ? 'active' : ''} ${i < step ? 'completed' : ''}`}
              title={s.label}
            >
              {s.num}
            </div>
          ))}
        </div>
      </header>

      <div className="app-content">
        {error && (
          <div style={{
            background: '#fdedec', color: '#c0392b', padding: '12px 16px',
            borderRadius: 8, marginBottom: 16, textAlign: 'center'
          }}>
            {error}
          </div>
        )}

        {loading && (
          <div style={{ textAlign: 'center', padding: 40, color: 'var(--primary)' }}>
            <p style={{ fontSize: 18, fontWeight: 600 }}>Analisi in corso...</p>
          </div>
        )}

        {!loading && step === 0 && (
          <StepPrescrizione
            data={rx}
            onUpdate={setRx}
            onNext={() => setStep(1)}
          />
        )}

        {!loading && step === 1 && (
          <StepQuestionario
            data={questionario}
            onUpdate={setQuestionario}
            onNext={calcola}
            onBack={() => setStep(0)}
          />
        )}

        {!loading && step === 2 && (
          <StepRisultato
            risultato={risultato}
            onRestart={restart}
          />
        )}
      </div>
    </div>
  );
}
