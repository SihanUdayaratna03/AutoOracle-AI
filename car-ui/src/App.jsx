import React, { useState } from 'react';
import ValuationResult from './components/ValuationResult';
import { Car, Zap, Settings2 } from 'lucide-react';

function App() {
  const [formData, setFormData] = useState({
    year: 2015,
    present_price: 75.0,
    kms_driven: 50000,
    fuel_type: 'Petrol',
    seller_type: 'Dealer',
    transmission: 'Manual',
    owner: 0
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: isNaN(value) ? value : Number(value) }));
  };

  const handleStringChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error('Failed to fetch valuation');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-title">AutoOracle <span>AI</span></div>
          <div className="brand-subtitle">Sri Lanka Vehicle Valuation</div>
        </div>
        
        <div className="divider" style={{ margin: '0.5rem 0' }} />

        <form onSubmit={handleSubmit} className="form-section">
          <div className="section-label">
            <Car size={14} /> Basic Details
          </div>
          
          <div className="input-group">
            <label>Manufacturing Year</label>
            <input type="number" name="year" value={formData.year} onChange={handleChange} min="2000" max="2024" className="input-field" />
          </div>

          <div className="input-group">
            <label>Ex-Showroom Price (Rs. Lakhs)</label>
            <input type="number" name="present_price" value={formData.present_price} onChange={handleChange} step="0.1" className="input-field" />
          </div>

          <div className="input-group">
            <label>Kilometers Driven</label>
            <input type="number" name="kms_driven" value={formData.kms_driven} onChange={handleChange} className="input-field" />
          </div>

          <div className="divider" style={{ margin: '0.5rem 0' }} />

          <div className="section-label">
            <Settings2 size={14} /> Specifications
          </div>

          <div className="input-group">
            <label>Fuel Type</label>
            <select name="fuel_type" value={formData.fuel_type} onChange={handleStringChange} className="input-field">
              <option value="Petrol">Petrol</option>
              <option value="Diesel">Diesel</option>
              <option value="CNG">CNG</option>
            </select>
          </div>

          <div className="input-group">
            <label>Seller Type</label>
            <select name="seller_type" value={formData.seller_type} onChange={handleStringChange} className="input-field">
              <option value="Dealer">Dealer</option>
              <option value="Individual">Individual</option>
            </select>
          </div>

          <div className="input-group">
            <label>Transmission</label>
            <select name="transmission" value={formData.transmission} onChange={handleStringChange} className="input-field">
              <option value="Manual">Manual</option>
              <option value="Automatic">Automatic</option>
            </select>
          </div>

          <div className="input-group">
            <label>Previous Owners</label>
            <select name="owner" value={formData.owner} onChange={handleChange} className="input-field">
              <option value="0">0 (First Owner)</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
            </select>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            <Zap size={18} /> {loading ? 'Analyzing...' : 'Get AI Valuation'}
          </button>
        </form>
      </aside>

      <main className="main-content">
        {!result && (
          <div className="hero">
            <div className="hero-badge">🇱🇰 Sri Lanka Edition · AI Powered</div>
            <h1 className="hero-title">AutoOracle AI</h1>
            <p className="hero-subtitle">
              Enterprise-grade machine learning that predicts the true market value of your vehicle in seconds — tailored for the Sri Lankan automotive market.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-val">~85%</span>
                <span className="stat-label">Model Accuracy</span>
              </div>
              <div className="stat">
                <span className="stat-val">300+</span>
                <span className="stat-label">Data Points</span>
              </div>
              <div className="stat">
                <span className="stat-val">3</span>
                <span className="stat-label">ML Algorithms</span>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div style={{ padding: '1rem', background: 'rgba(244,63,94,0.1)', border: '1px solid #f43f5e', borderRadius: '12px', color: '#f43f5e' }}>
            Error: {error}
          </div>
        )}

        {result && <ValuationResult result={result} formData={formData} />}
      </main>
    </div>
  );
}

export default App;
