import { useRef, useState } from 'react';
import ParticleBackground from './components/ParticleBackground';
import HeroSection        from './components/HeroSection';
import InputForm          from './components/InputForm';
import ResultsDashboard   from './components/ResultsDashboard';
import './App.css';

export default function App() {
  const formRef    = useRef(null);
  const [result, setResult] = useState(null);

  const scrollToForm = () =>
    formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });

  return (
    <div className="app">
      <ParticleBackground />

      {/* Nav */}
      <nav className="nav glass">
        <div className="nav__brand">
          AutoOracle <span>AI</span>
        </div>
        <div className="nav__links">
          <span className="nav__pill">🇱🇰 Sri Lanka</span>
          <span className="nav__pill nav__pill--dim">ML-Powered</span>
        </div>
      </nav>

      {/* Hero */}
      {!result && <HeroSection onCTAClick={scrollToForm} />}

      {/* Form */}
      {!result && (
        <div ref={formRef}>
          <InputForm onResult={setResult} />
        </div>
      )}

      {/* Results */}
      {result && (
        <ResultsDashboard
          data={result}
          onReset={() => setResult(null)}
        />
      )}

      {/* Footer */}
      <footer className="footer">
        <p>AutoOracle AI · Sri Lanka Car Valuation · Powered by Random Forest ML</p>
      </footer>
    </div>
  );
}
