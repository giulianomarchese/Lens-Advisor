import { useState } from 'react';

const sphOptions = [];
for (let v = -12; v <= 12; v += 0.25) {
  sphOptions.push(v);
}

const cylOptions = [];
for (let v = -6; v <= 0; v += 0.25) {
  cylOptions.push(v);
}

const addOptions = [];
for (let v = 0; v <= 4; v += 0.25) {
  addOptions.push(v);
}

function fmt(v) {
  if (v === 0) return '0.00';
  return (v > 0 ? '+' : '') + v.toFixed(2);
}

export default function StepPrescrizione({ data, onUpdate, onNext }) {
  const [showAxOd, setShowAxOd] = useState(data.cyl_od !== 0);
  const [showAxOs, setShowAxOs] = useState(data.cyl_os !== 0);

  function set(field, value) {
    const num = parseFloat(value) || 0;
    const updated = { ...data, [field]: num };
    // Show axis when cylinder is set
    if (field === 'cyl_od') {
      setShowAxOd(num !== 0);
      if (num === 0) updated.ax_od = null;
    }
    if (field === 'cyl_os') {
      setShowAxOs(num !== 0);
      if (num === 0) updated.ax_os = null;
    }
    onUpdate(updated);
  }

  function setAxis(field, value) {
    const num = parseInt(value) || 0;
    onUpdate({ ...data, [field]: num });
  }

  function setPd(value) {
    const num = parseFloat(value) || null;
    onUpdate({ ...data, pd: num });
  }

  return (
    <div>
      <div className="card" style={{ maxWidth: 800, margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', color: 'var(--primary)', marginBottom: 20 }}>
          Inserimento Prescrizione
        </h2>

        <div className="rx-table">
          {/* Header */}
          <div className="rx-row header">
            <div></div>
            <div className="field-group"><label>Sfera (SPH)</label></div>
            <div className="field-group"><label>Cilindro (CYL)</label></div>
            <div className="field-group"><label>Asse (AX)</label></div>
            <div className="field-group"><label>Addizione (ADD)</label></div>
            <div className="field-group"><label>PD</label></div>
          </div>

          {/* OD */}
          <div className="rx-row">
            <div className="label">OD</div>
            <div className="field-group">
              <select value={data.sph_od} onChange={e => set('sph_od', e.target.value)}>
                {sphOptions.map(v => (
                  <option key={v} value={v}>{fmt(v)}</option>
                ))}
              </select>
            </div>
            <div className="field-group">
              <select value={data.cyl_od} onChange={e => set('cyl_od', e.target.value)}>
                {cylOptions.map(v => (
                  <option key={v} value={v}>{fmt(v)}</option>
                ))}
              </select>
            </div>
            <div className="field-group">
              {showAxOd ? (
                <input
                  type="number"
                  min="1"
                  max="180"
                  value={data.ax_od || ''}
                  placeholder="1-180"
                  onChange={e => setAxis('ax_od', e.target.value)}
                />
              ) : (
                <input disabled placeholder="—" />
              )}
            </div>
            <div className="field-group" style={{ gridColumn: 'span 2' }}></div>
          </div>

          {/* OS */}
          <div className="rx-row">
            <div className="label">OS</div>
            <div className="field-group">
              <select value={data.sph_os} onChange={e => set('sph_os', e.target.value)}>
                {sphOptions.map(v => (
                  <option key={v} value={v}>{fmt(v)}</option>
                ))}
              </select>
            </div>
            <div className="field-group">
              <select value={data.cyl_os} onChange={e => set('cyl_os', e.target.value)}>
                {cylOptions.map(v => (
                  <option key={v} value={v}>{fmt(v)}</option>
                ))}
              </select>
            </div>
            <div className="field-group">
              {showAxOs ? (
                <input
                  type="number"
                  min="1"
                  max="180"
                  value={data.ax_os || ''}
                  placeholder="1-180"
                  onChange={e => setAxis('ax_os', e.target.value)}
                />
              ) : (
                <input disabled placeholder="—" />
              )}
            </div>
            <div className="field-group" style={{ gridColumn: 'span 2' }}></div>
          </div>
        </div>

        {/* ADD + PD */}
        <div className="pd-add-row">
          <div className="field-group">
            <label>Addizione (ADD)</label>
            <select value={data.add} onChange={e => set('add', e.target.value)}>
              {addOptions.map(v => (
                <option key={v} value={v}>{v === 0 ? '—' : fmt(v)}</option>
              ))}
            </select>
          </div>
          <div className="field-group">
            <label>PD (mm)</label>
            <input
              type="number"
              min="50"
              max="80"
              step="0.5"
              value={data.pd || ''}
              placeholder="es. 64"
              onChange={e => setPd(e.target.value)}
            />
          </div>
        </div>

        {/* Video centratore toggle */}
        <div className="toggle-row">
          <span style={{ fontWeight: 600, fontSize: 14 }}>Video centratore disponibile</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={data.video_centratore || false}
              onChange={e => onUpdate({ ...data, video_centratore: e.target.checked })}
            />
            <span className="toggle-slider"></span>
          </label>
          <span style={{ fontSize: 13, color: 'var(--text-light)' }}>
            {data.video_centratore ? 'Attivo' : 'Non attivo'}
          </span>
        </div>
      </div>

      <div className="btn-bar" style={{ maxWidth: 800, margin: '20px auto 0' }}>
        <div></div>
        <button className="btn btn-primary" onClick={onNext}>
          Avanti — Questionario
        </button>
      </div>
    </div>
  );
}
