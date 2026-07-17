import './HeroSection.css';

export default function HeroSection({ onCTAClick }) {
  return (
    <section className="hero">
      {/* Ambient blobs */}
      <div className="hero__blob hero__blob--1" aria-hidden />
      <div className="hero__blob hero__blob--2" aria-hidden />
      <div className="hero__blob hero__blob--3" aria-hidden />

      <div className="hero__content">
        {/* Badge */}
        <div className="hero__badge">
          <span className="hero__badge-dot" />
          🇱🇰 &nbsp; Sri Lanka Edition &nbsp;·&nbsp; AI Powered
        </div>

        {/* Headline */}
        <h1 className="hero__title">
          <span className="hero__title-line1">AutoOracle</span>
          <span className="hero__title-line2 gradient-text">AI</span>
        </h1>

        <p className="hero__subtitle">
          Enterprise-grade machine learning that reveals the true market<br />
          value of any vehicle in the Sri Lankan automotive market —<br />
          <strong>instantly and accurately.</strong>
        </p>

        {/* Stats row */}
        <div className="hero__stats">
          {[
            { value: '~85%', label: 'Model Accuracy' },
            { value: '300+', label: 'Training Records' },
            { value: '3',    label: 'ML Algorithms'  },
            { value: '15×',  label: 'LK Market Scale' },
          ].map(s => (
            <div key={s.label} className="hero__stat">
              <span className="hero__stat-value">{s.value}</span>
              <span className="hero__stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        {/* CTA */}
        <button className="hero__cta" onClick={onCTAClick}>
          <span>Get Your Valuation</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Decorative card */}
      <div className="hero__visual" aria-hidden>
        <div className="hero__card glass">
          <div className="hero__card-label">AI VALUATION ENGINE</div>
          <div className="hero__card-value">Rs. 87.5L</div>
          <div className="hero__card-range">
            <span>Range: Rs. 78.8L – Rs. 96.3L</span>
          </div>
          <div className="hero__card-bar">
            <div className="hero__card-bar-fill" />
          </div>
          <div className="hero__card-tags">
            <span className="tag tag--green">✓ Diesel</span>
            <span className="tag tag--blue">✓ Automatic</span>
            <span className="tag tag--purple">✓ 2019 Model</span>
          </div>
        </div>
      </div>
    </section>
  );
}
