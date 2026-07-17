import React from 'react';

const ValuationResult = ({ result, formData }) => {
  const carAge = new Date().getFullYear() - formData.year;

  return (
    <div>
      <div className="results-header">
        <div className="results-dot"></div>
        <h3 className="results-title">Valuation Results</h3>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card green">
          <span className="kpi-icon">💰</span>
          <div className="kpi-label">Estimated Selling Price</div>
          <div className="kpi-value green">Rs. {result.predicted_price.toFixed(1)}L</div>
          <div className="kpi-subtext">AI-predicted fair market value</div>
        </div>

        <div className="kpi-card blue">
          <span className="kpi-icon">🏷️</span>
          <div className="kpi-label">Original Showroom Price</div>
          <div className="kpi-value blue">Rs. {formData.present_price.toFixed(1)}L</div>
          <div className="kpi-subtext">Brand-new ex-showroom value</div>
        </div>

        <div className="kpi-card red">
          <span className="kpi-icon">📉</span>
          <div className="kpi-label">Total Depreciation</div>
          <div className="kpi-value red">Rs. {result.depreciation.toFixed(1)}L</div>
          <div className="kpi-subtext">↓ {result.depreciation_pct.toFixed(1)}% value lost</div>
        </div>
      </div>

      <div className="market-analysis">
        <div className="price-range-banner">
          <div className="range-label">✅ Expected Price Range</div>
          <div className="range-value">
            Rs. {result.lower_estimate.toFixed(1)}L — Rs. {result.upper_estimate.toFixed(1)}L
          </div>
          <div className="kpi-subtext" style={{ marginTop: '0.25rem' }}>
            Typical negotiation range for similar vehicles in the Sri Lankan used-car market.
          </div>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <div className="kpi-label">Value Factors</div>
          <div className="pill-container">
            {carAge <= 2 ? (
              <span className="factor-pill positive">🟢 Near-new · Low depreciation</span>
            ) : carAge <= 5 ? (
              <span className="factor-pill positive">🟡 Relatively new · Good resale</span>
            ) : carAge <= 10 ? (
              <span className="factor-pill neutral">🟠 Moderate age · Avg value</span>
            ) : (
              <span className="factor-pill negative">🔴 High age · Heavy depreciation</span>
            )}

            {formData.kms_driven < 30000 ? (
              <span className="factor-pill positive">🟢 Low mileage · Value boost</span>
            ) : formData.kms_driven < 80000 ? (
              <span className="factor-pill neutral">🟡 Average mileage</span>
            ) : (
              <span className="factor-pill negative">🔴 High mileage · Value drop</span>
            )}

            {formData.transmission === 'Automatic' && (
              <span className="factor-pill positive">🟢 Automatic · Premium tag</span>
            )}
            
            {formData.fuel_type === 'Diesel' ? (
              <span className="factor-pill positive">🟢 Diesel · Economy preferred</span>
            ) : formData.fuel_type === 'Petrol' && (
              <span className="factor-pill neutral">🟡 Petrol · Standard</span>
            )}
            
            {Number(formData.owner) === 0 ? (
              <span className="factor-pill positive">🟢 First owner · Premium</span>
            ) : Number(formData.owner) >= 2 && (
              <span className="factor-pill negative">🔴 Multiple owners · Reduced</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ValuationResult;
