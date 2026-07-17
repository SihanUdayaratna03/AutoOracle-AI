import { useState } from 'react';
import './InputForm.css';

const STEPS = [
  {
    id: 'basics',
    title: 'Basic Details',
    subtitle: 'Tell us about the vehicle',
    icon: '🚗',
  },
  {
    id: 'specs',
    title: 'Specifications',
    subtitle: 'Engine & transmission info',
    icon: '⚙️',
  },
];

export default function InputForm({ onResult }) {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [form, setForm] = useState({
    year: 2015,
    present_price: 75,
    kms_driven: 50000,
    fuel_type: 'Petrol',
    seller_type: 'Dealer',
    transmission: 'Manual',
    owner: 0,
  });

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      onResult({ ...data, input: form });
    } catch (e) {
      setError('Could not connect to the API. Make sure api.py is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="form-section" id="valuate">
      {/* Step indicator */}
      <div className="form-steps">
        {STEPS.map((s, i) => (
          <div
            key={s.id}
            className={`form-step ${i === step ? 'form-step--active' : ''} ${i < step ? 'form-step--done' : ''}`}
            onClick={() => i < step && setStep(i)}
          >
            <div className="form-step__dot">
              {i < step ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              ) : (
                <span>{i + 1}</span>
              )}
            </div>
            <div className="form-step__info">
              <span className="form-step__title">{s.title}</span>
              <span className="form-step__sub">{s.subtitle}</span>
            </div>
          </div>
        ))}
        <div className="form-steps__line" />
      </div>

      {/* Card */}
      <div className="form-card glass">
        <div className="form-card__header">
          <span className="form-card__icon">{STEPS[step].icon}</span>
          <div>
            <h2 className="form-card__title">{STEPS[step].title}</h2>
            <p className="form-card__sub">{STEPS[step].subtitle}</p>
          </div>
        </div>

        {/* STEP 0 */}
        {step === 0 && (
          <div className="form-fields" key="step0">
            <div className="field">
              <label className="field__label">Manufacturing Year</label>
              <div className="field__slider-wrap">
                <input
                  type="range" min={2000} max={2024} value={form.year}
                  onChange={e => set('year', +e.target.value)}
                  className="field__slider"
                />
                <span className="field__slider-val">{form.year}</span>
              </div>
              <div className="field__hint">{2024 - form.year} years old</div>
            </div>

            <div className="field">
              <label className="field__label">Ex-Showroom Price <span className="field__unit">(Rs. Lakhs)</span></label>
              <input
                type="number" min={0} max={1000} step={1}
                value={form.present_price}
                onChange={e => set('present_price', +e.target.value)}
                className="field__input"
              />
            </div>

            <div className="field">
              <label className="field__label">Kilometers Driven</label>
              <input
                type="number" min={0} max={500000} step={1000}
                value={form.kms_driven}
                onChange={e => set('kms_driven', +e.target.value)}
                className="field__input"
              />
              <div className="field__hint">{(form.kms_driven / 1000).toFixed(0)}k km driven</div>
            </div>
          </div>
        )}

        {/* STEP 1 */}
        {step === 1 && (
          <div className="form-fields" key="step1">
            <div className="field">
              <label className="field__label">Fuel Type</label>
              <div className="field__pills">
                {['Petrol', 'Diesel', 'CNG'].map(v => (
                  <button
                    key={v}
                    className={`pill ${form.fuel_type === v ? 'pill--active' : ''}`}
                    onClick={() => set('fuel_type', v)}
                  >{v}</button>
                ))}
              </div>
            </div>

            <div className="field">
              <label className="field__label">Transmission</label>
              <div className="field__pills">
                {['Manual', 'Automatic'].map(v => (
                  <button
                    key={v}
                    className={`pill ${form.transmission === v ? 'pill--active' : ''}`}
                    onClick={() => set('transmission', v)}
                  >{v}</button>
                ))}
              </div>
            </div>

            <div className="field">
              <label className="field__label">Seller Type</label>
              <div className="field__pills">
                {['Dealer', 'Individual'].map(v => (
                  <button
                    key={v}
                    className={`pill ${form.seller_type === v ? 'pill--active' : ''}`}
                    onClick={() => set('seller_type', v)}
                  >{v}</button>
                ))}
              </div>
            </div>

            <div className="field">
              <label className="field__label">Number of Previous Owners</label>
              <div className="field__pills">
                {[0, 1, 2, 3].map(v => (
                  <button
                    key={v}
                    className={`pill ${form.owner === v ? 'pill--active' : ''}`}
                    onClick={() => set('owner', v)}
                  >{v === 0 ? 'First Owner' : `${v} Previous`}</button>
                ))}
              </div>
            </div>
          </div>
        )}

        {error && <div className="form-error">{error}</div>}

        {/* Navigation */}
        <div className="form-nav">
          {step > 0 && (
            <button className="btn btn--ghost" onClick={() => setStep(s => s - 1)}>
              ← Back
            </button>
          )}
          {step < STEPS.length - 1 ? (
            <button className="btn btn--primary" onClick={() => setStep(s => s + 1)}>
              Continue →
            </button>
          ) : (
            <button className="btn btn--primary btn--glow" onClick={handleSubmit} disabled={loading}>
              {loading ? <span className="spinner" /> : '⚡ Get AI Valuation'}
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
