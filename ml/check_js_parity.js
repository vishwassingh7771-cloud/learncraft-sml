// Checks that shared/readability_ml.js reproduces the Python predictions.
// Run from the project root:  node ml/check_js_parity.js
const path = require('path');
const ml = require('../shared/readability_ml');
const model = require('../models/ridge_features.json');
const samples = require(path.join(__dirname, '..', 'results', 'parity_samples.json'));

let worst = 0;
for (const s of samples) {
  const diff = Math.abs(ml.predictEasiness(s.text, model).easiness - s.pred);
  worst = Math.max(worst, diff);
}
console.log(`Checked ${samples.length} passages, largest |JS - Python| = ${worst.toExponential(2)}`);
process.exit(worst < 1e-6 ? 0 : 1);
