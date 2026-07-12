import { useEffect, useState, useRef } from 'react';
import './ResultsDashboard.css';

/* Animated counter */
function CountUp({ target, prefix = '', suffix = '', decimals = 1 }) {
  const [val, setVal] = useState(0);
  useEffect(() => {
    const dur   = 1400;
    const start = performance.now();
    const tick  = (now) => {
      const t = Math.min((now - start) / dur, 1);
      const ease = 1 - Math.pow(1 - t, 4);
      setVal(target * ease);
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [target]);
  return <>{prefix}{val.toFixed(decimals)}{suffix}</>;
}

/* SVG Gauge */
function Gauge({ value, max }) {
  const pct   = Math.min(value / max, 1);
  const R     = 80;
  const cx    = 110; const cy = 110;
  const sweep = Math.PI * 1.5;             // 270°
  const startAngle = Math.PI + Math.PI * 0.25;
  const endAngle   = startAngle + sweep;
  const angle      = startAngle + pct * sweep;

  const polarToCart = (ang, r = R) => ({
    x: cx + r * Math.cos(ang),
    y: cy + r * Math.sin(ang),
  });

  const arcPath = (r, a1, a2) => {
    const s = polarToCart(a1, r);
    const e = polarToCart(a2, r);
    const large = a2 - a1 > Math.PI ? 1 : 0;
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
  };

  const needle = polarToCart(angle, R - 12);

  return (
    <svg viewBox="0 0 220 150" className="gauge-svg">
      {/* Track */}
      <path d={arcPath(R, startAngle, endAngle)} stroke="rgba(255,255,255,0.06)" strokeWidth="16" fill="none" strokeLinecap="round" />
      {/* Red zone */}
      <path d={arcPath(R, startAngle, startAngle + sweep * 0.4)} stroke="rgba(244,63,94,0.35)" strokeWidth="16" fill="none" strokeLinecap="round" />
      {/* Amber zone */}
      <path d={arcPath(R, startAngle + sweep * 0.4, startAngle + sweep * 0.75)} stroke="rgba(245,158,11,0.35)" strokeWidth="16" fill="none" strokeLinecap="round" />
      {/* Green zone */}
      <path d={arcPath(R, startAngle + sweep * 0.75, endAngle)} stroke="rgba(16,185,129,0.35)" strokeWidth="16" fill="none" strokeLinecap="round" />
      {/* Fill */}
      <path d={arcPath(R, startAngle, angle)} stroke="url(#gaugeGrad)" strokeWidth="16" fill="none" strokeLinecap="round" />
      {/* Needle dot */}
      <circle cx={needle.x} cy={needle.y} r="5" fill="#38bdf8" />
      <circle cx={cx} cy={cy} r="6" fill="#38bdf8" opacity="0.3" />
      <circle cx={cx} cy={cy} r="3" fill="#38bdf8" />
      <defs>
        <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%"   stopColor="#f43f5e" />
          <stop offset="50%"  stopColor="#f59e0b" />
          <stop offset="100%" stopColor="#10b981" />
        </linearGradient>
      </defs>
    </svg>
  );
}

function FactorPill({ label, type }) {
  return <span className={`factor-pill factor-pill--${type}`}>{label}</span>;
}

export default function ResultsDashboard({ data, onReset }) {
  const dashRef = useRef(null);
  const { predicted_price, depreciation, depreciation_pct, retention_rate, lower_estimate, upper_estimate, input } = data;
  const car_age = 2024 - input.year;

  useEffect(() => {
    dashRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  /* Build factor pills */
  const factors = [];
  if (car_age <= 2)         factors.push({ label: '🟢 Near-new — minimal depreciation',   type: 'positive' });
  else if (car_age <= 5)    factors.push({ label: '🟡 Relatively new — good resale',       type: 'neutral'  });
  else if (car_age <= 10)   factors.push({ label: '🟠 Moderate age — avg value',           type: 'neutral'  });
  else                      factors.push({ label: '🔴 High age — heavy depreciation',      type: 'negative' });

  if (input.kms_driven < 30000)       factors.push({ label: '🟢 Low mileage — value boost',        type: 'positive' });
  else if (input.kms_driven < 80000)  factors.push({ label: '🟡 Average mileage',                   type: 'neutral'  });
  else                                factors.push({ label: '🔴 High mileage — value drop',         type: 'negative' });

  if (input.transmission === 'Automatic') factors.push({ label: '🟢 Automatic — premium tag',       type: 'positive' });
  if (input.fuel_type === 'Diesel')       factors.push({ label: '🟢 Diesel — economy preferred',    type: 'positive' });
  else if (input.fuel_type === 'Petrol')  factors.push({ label: '🟡 Petrol — standard',             type: 'neutral'  });
  if (input.owner === 0)                  factors.push({ label: '🟢 First owner — premium',         type: 'positive' });
  else if (input.owner >= 2)             factors.push({ label: '🔴 Multiple owners — reduced',      type: 'negative' });

  return (
    <section className="results" ref={dashRef}>
      {/* Blobs */}
      <div className="results__blob results__blob--1" aria-hidden />
      <div className="results__blob results__blob--2" aria-hidden />

      {/* Header */}
      <div className="results__header">
        <div className="results__badge">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
          AI Valuation Complete
        </div>
        <h2 className="results__title">Your Vehicle Report</h2>
        <p className="results__sub">Based on {input.year} · {input.fuel_type} · {input.transmission} · {input.kms_driven.toLocaleString()} km</p>
      </div>

      {/* KPI row */}
      <div className="kpi-row">
        <div className="kpi kpi--green">
          <div className="kpi__icon">💰</div>
          <div className="kpi__label">Estimated Selling Price</div>
          <div className="kpi__val kpi__val--green">
            Rs.&nbsp;<CountUp target={predicted_price} decimals={1} />L
          </div>
          <div className="kpi__sub">AI-predicted fair market value</div>
        </div>

        <div className="kpi kpi--blue">
          <div className="kpi__icon">🏷️</div>
          <div className="kpi__label">Original Showroom Price</div>
          <div className="kpi__val kpi__val--blue">
            Rs.&nbsp;<CountUp target={input.present_price} decimals={1} />L
          </div>
          <div className="kpi__sub">Ex-showroom brand-new value</div>
        </div>

        <div className="kpi kpi--red">
          <div className="kpi__icon">📉</div>
          <div className="kpi__label">Total Depreciation</div>
          <div className="kpi__val kpi__val--red">
            Rs.&nbsp;<CountUp target={depreciation} decimals={1} />L
          </div>
          <div className="kpi__sub">↓ {depreciation_pct}% · {retention_rate}% retained</div>
        </div>
      </div>

      {/* Analysis section */}
      <div className="analysis-grid">
        {/* Left: Gauge + range */}
        <div className="analysis-gauge glass">
          <div className="analysis-gauge__label">VALUE POSITION</div>
          <Gauge value={predicted_price} max={input.present_price * 1.1} />
          <div className="analysis-gauge__center-val">
            Rs. {predicted_price.toFixed(1)}L
          </div>
          <div className="analysis-range">
            <div className="analysis-range__label">Expected Market Range</div>
            <div className="analysis-range__val">Rs. {lower_estimate}L — Rs. {upper_estimate}L</div>
            <div className="analysis-range__bar">
              <div className="analysis-range__fill" style={{ width: `${retention_rate}%` }} />
            </div>
            <div className="analysis-range__ends">
              <span>Rs. {lower_estimate}L</span>
              <span>Rs. {upper_estimate}L</span>
            </div>
          </div>
        </div>

        {/* Right: Factors + bar */}
        <div className="analysis-factors glass">
          <div className="analysis-factors__label">VALUE FACTORS</div>
          <div className="factors-list">
            {factors.map((f, i) => <FactorPill key={i} {...f} />)}
          </div>

          <div className="depr-bar-section">
            <div className="depr-bar-section__label">Depreciation Breakdown</div>
            <div className="depr-bars">
              <div className="depr-bar__row">
                <span className="depr-bar__name">Current Value</span>
                <div className="depr-bar__track">
                  <div className="depr-bar__fill depr-bar__fill--green" style={{ width: `${retention_rate}%` }} />
                </div>
                <span className="depr-bar__num">Rs. {predicted_price.toFixed(1)}L</span>
              </div>
              <div className="depr-bar__row">
                <span className="depr-bar__name">Depreciation</span>
                <div className="depr-bar__track">
                  <div className="depr-bar__fill depr-bar__fill--red" style={{ width: `${depreciation_pct}%` }} />
                </div>
                <span className="depr-bar__num">Rs. {depreciation.toFixed(1)}L</span>
              </div>
            </div>
          </div>

          {/* Summary table */}
          <div className="summary-table">
            {[
              ['Year', input.year],
              ['Car Age', `${car_age} years`],
              ['Mileage', `${input.kms_driven.toLocaleString()} km`],
              ['Fuel', input.fuel_type],
              ['Transmission', input.transmission],
              ['Seller', input.seller_type],
              ['Owners', input.owner === 0 ? 'First Owner' : `${input.owner} previous`],
            ].map(([k, v]) => (
              <div key={k} className="summary-row">
                <span className="summary-key">{k}</span>
                <span className="summary-val">{v}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Reset */}
      <button className="results__reset" onClick={onReset}>
        ← Evaluate Another Vehicle
      </button>
    </section>
  );
}
