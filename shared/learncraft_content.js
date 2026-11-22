/**
 * LearnCraft AI - content and helpers shared by index.html and the Next.js app.
 *
 * Hand-written sample lessons and quizzes (so the app is useful without the
 * backend), the sample texts for the "Check any text" tab, a safe
 * markdown-to-HTML converter for AI output, and the grade-fit rule.
 * Works as a <script> (window.LearnCraftContent) and as a CommonJS module.
 */
(function (root) {
const esc = (s) => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const tierOf = (g) => g <= 5 ? 'elementary' : g <= 8 ? 'middle' : 'high';

const SAMPLES = {
  'photosynthesis': {
    elementary: { hook: 'Plants cannot go to a shop to buy food. They make their own food, and they use sunlight to do it!',
      points: ['Leaves are green because of <strong>chlorophyll</strong>. It catches sunlight.', 'Roots drink <strong>water</strong> from the soil, and leaves take in <strong>air</strong>.', 'The plant uses light to turn water and air into <strong>sugar</strong>. The sugar is its food.', 'The plant gives out <strong>oxygen</strong>. That is the air we breathe!'],
      example: 'Put one plant near a sunny window and one in a dark cupboard. After a week, the sunny plant looks green and strong. The dark one turns pale.' },
    middle: { hook: 'Every green leaf works like a tiny solar-powered kitchen. It turns light into food the plant can store and use.',
      points: ['Inside leaf cells are <strong>chloroplasts</strong>, which hold the green pigment <strong>chlorophyll</strong>.', 'Chlorophyll absorbs red and blue light and reflects green, which is why leaves look green.', 'The plant combines <strong>carbon dioxide</strong> and <strong>water</strong> to make <strong>glucose</strong>, a sugar.', 'Word equation: carbon dioxide + water → (light) → glucose + oxygen.', 'Tiny pores called <strong>stomata</strong> let carbon dioxide in and oxygen out.'],
      example: 'Farmers grow more crops in greenhouses partly because the glass traps warmth and lets in plenty of light, so photosynthesis runs faster.' },
    high: { hook: 'Photosynthesis converts light energy into chemical energy stored in glucose, powering almost every food chain on Earth.',
      points: ['<strong>Light-dependent reactions</strong> (thylakoid membranes): light splits water, releasing O₂ and producing ATP and NADPH.', 'The <strong>Calvin cycle</strong> (stroma) uses ATP and NADPH to fix CO₂ into sugars, with the enzyme RuBisCO doing the first step.', 'Overall: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂.', 'Rate is limited by light intensity, CO₂ concentration and temperature, whichever is in shortest supply.'],
      example: 'Engineers studying "artificial leaves" try to copy the light-harvesting step to produce clean fuels from sunlight.' }
  },
  'the water cycle': {
    elementary: { hook: 'The water you drink today might once have been part of a cloud, a river, or even the sea!',
      points: ['The sun warms water in seas and lakes. Some of it turns into an invisible gas. This is <strong>evaporation</strong>.', 'High in the sky the gas cools down and makes tiny drops. The drops make <strong>clouds</strong>.', 'When the drops get heavy, they fall as <strong>rain</strong> or snow.', 'Rain flows into rivers and back to the sea. Then it all starts again.'],
      example: 'After rain, puddles on the playground slowly disappear on a sunny day. The water has evaporated into the air.' },
    middle: { hook: 'Earth has had roughly the same amount of water for billions of years. It just keeps moving around in a loop.',
      points: ['<strong>Evaporation</strong>: heat from the sun turns liquid water into water vapour.', '<strong>Transpiration</strong>: plants release water vapour through their leaves.', '<strong>Condensation</strong>: rising vapour cools and forms droplets around dust, making clouds.', '<strong>Precipitation</strong>: droplets join until they are heavy enough to fall as rain, snow or hail.', '<strong>Collection</strong>: water gathers in oceans, lakes and underground as groundwater.'],
      example: 'Drops form on the outside of a cold glass because water vapour in the air condenses when it touches the cool surface.' },
    high: { hook: 'The hydrological cycle moves about 500,000 cubic kilometres of water each year, driven by solar energy and gravity.',
      points: ['Evaporation absorbs latent heat; condensation releases it, which fuels storms and moves energy around the planet.', 'Clouds form when air cools to its dew point, usually through uplift over mountains, fronts or convection.', 'Runoff and infiltration split precipitation between rivers and aquifers, depending on soil and land use.', 'Climate change intensifies the cycle: warmer air holds about 7% more water vapour per °C.'],
      example: 'Paving over land increases runoff and flood risk, which is why cities build rain gardens and permeable pavements.' }
  },
  "ohm's law": {
    elementary: { hook: 'Electricity flowing in a wire is a bit like water flowing in a pipe.',
      points: ['A battery gives a <strong>push</strong> to electricity. We call this push <strong>voltage</strong>.', 'The flow of electricity is called <strong>current</strong>.', 'Some things make it harder for electricity to flow. This is <strong>resistance</strong>.', 'A bigger push makes more electricity flow. More resistance makes less flow.'],
      example: 'A torch with fresh batteries shines brightly. When the batteries are old, the push is weaker and the light is dim.' },
    middle: { hook: 'Ohm\'s law is a simple rule that tells you how much current flows in a circuit.',
      points: ['<strong>Voltage (V)</strong>, in volts, is the push from the battery.', '<strong>Current (I)</strong>, in amperes, is how much charge flows each second.', '<strong>Resistance (R)</strong>, in ohms (Ω), is how much a part resists the flow.', 'The rule: <strong>V = I × R</strong>. So I = V ÷ R.', 'Example: a 6 V battery and a 3 Ω resistor give I = 6 ÷ 3 = 2 A.'],
      example: 'A dimmer switch adds resistance to the circuit, which lowers the current and makes the bulb glow less.' },
    high: { hook: 'Ohm\'s law, V = IR, describes how current depends on voltage for ohmic conductors at constant temperature.',
      points: ['For an ohmic conductor, a V-I graph is a straight line through the origin; its gradient is R.', 'Resistance depends on material, length and area: R = ρL/A.', 'Series resistors add (R = R₁ + R₂); in parallel, 1/R = 1/R₁ + 1/R₂.', 'Filament lamps are non-ohmic: resistance rises as the filament heats up.'],
      example: 'Phone chargers use resistors and control circuits so the battery gets the right current without overheating.' }
  },
  'the roman republic': {
    elementary: { hook: 'Long ago, the people of Rome decided they did not want a king any more.',
      points: ['In 509 BCE the Romans started a <strong>republic</strong>. Citizens chose their leaders.', 'Two leaders called <strong>consuls</strong> ran the city. They only ruled for one year.', 'A group of older men called the <strong>Senate</strong> gave advice.', 'Many countries today still use ideas from Rome, like voting for leaders.'],
      example: 'When your class votes for a class monitor for one term, that is a little like how Romans chose consuls.' },
    middle: { hook: 'The Roman Republic lasted almost 500 years and shaped how many modern governments work.',
      points: ['After overthrowing their last king in 509 BCE, Romans shared power so no single person had too much.', 'Two <strong>consuls</strong> were elected each year and could block each other with a veto.', 'The <strong>Senate</strong>, made up of wealthy patricians, controlled money and foreign policy.', '<strong>Plebeians</strong> (ordinary citizens) won the right to elect tribunes to protect their interests.', 'The Republic ended when Augustus became the first emperor in 27 BCE.'],
      example: 'India\'s Parliament also has two houses and elected representatives, an idea with roots in republics like Rome\'s.' },
    high: { hook: 'The Roman Republic combined elements of monarchy, aristocracy and democracy, a "mixed constitution" that Polybius admired.',
      points: ['Annual, collegial magistracies (consuls, praetors) limited individual power through term limits and veto.', 'The Senate held informal but decisive influence over finance, diplomacy and provincial command.', 'The Conflict of the Orders gradually opened offices to plebeians and created the tribunate.', 'Expansion, private armies and inequality fuelled civil wars that ended the Republic under Augustus.'],
      example: 'The framers of the US Constitution cited Rome when designing checks and balances and a Senate.' }
  },
  'quadratic equations': {
    elementary: { hook: 'Some number puzzles ask: which number, multiplied by itself, gives this answer?',
      points: ['A number times itself is called its <strong>square</strong>. 3 × 3 = 9.', 'If □ × □ = 16, the missing number is 4.', 'Puzzles like this are the first step towards <strong>quadratic equations</strong>.', 'You will learn the full method in later grades.'],
      example: 'A square garden has an area of 25 square metres. Each side must be 5 metres, because 5 × 5 = 25.' },
    middle: { hook: 'When you throw a ball, its path is a curve. Quadratic equations describe curves like that.',
      points: ['A quadratic equation has an x² term, like <strong>x² − 5x + 6 = 0</strong>.', 'One way to solve it is <strong>factorising</strong>: (x − 2)(x − 3) = 0.', 'If two numbers multiply to zero, one of them must be zero. So x = 2 or x = 3.', 'A quadratic can have two, one or no real answers.'],
      example: 'A rectangle is 2 m longer than it is wide and has an area of 15 m². Solving x(x + 2) = 15 gives a width of 3 m.' },
    high: { hook: 'Quadratics, ax² + bx + c = 0, model projectiles, areas and optimisation problems.',
      points: ['Quadratic formula: x = (−b ± √(b² − 4ac)) / 2a.', 'The <strong>discriminant</strong> b² − 4ac tells you the number of real roots: >0 two, =0 one, <0 none.', 'The graph is a parabola with vertex at x = −b/2a.', 'Completing the square rewrites the equation as a(x − h)² + k to read off the vertex.'],
      example: 'A ball thrown upwards follows h = −5t² + 20t + 1. Its highest point is at t = 2 s, where h = 21 m.' }
  }
};
const SAMPLE_QUIZ = {
  'photosynthesis': [
    ['What do plants mainly use to make food?', ['Sunlight, water and carbon dioxide', 'Soil and stones', 'Only oxygen', 'Moonlight'], 0, 'Plants use light energy to turn water and carbon dioxide into sugar.'],
    ['Why are most leaves green?', ['They are painted', 'Chlorophyll reflects green light', 'They are full of water', 'Green light is the strongest'], 1, 'Chlorophyll absorbs red and blue light and reflects green.'],
    ['A plant is kept in the dark for two weeks. What is most likely to happen?', ['It grows faster', 'Nothing changes', 'It gets weaker because it cannot make food', 'It makes more oxygen'], 2, 'Without light, photosynthesis stops, so the plant runs out of food.']],
  'the water cycle': [
    ['What is it called when water turns into vapour?', ['Condensation', 'Evaporation', 'Precipitation', 'Collection'], 1, 'Heat turns liquid water into water vapour: evaporation.'],
    ['How do clouds form?', ['Water vapour cools and condenses into droplets', 'Wind blows smoke upwards', 'The sun makes new water', 'Rain goes back up'], 0, 'Rising vapour cools and condenses into tiny droplets.'],
    ['Why do puddles dry faster on hot, sunny days?', ['Puddles sink into the sky', 'More heat means faster evaporation', 'Cold air holds more water', 'Clouds drink them'], 1, 'Heat speeds up evaporation.']],
  "ohm's law": [
    ['What does voltage measure?', ['How fast a wire is', 'The push that drives current', 'The colour of the wire', 'The length of the circuit'], 1, 'Voltage is the "push" from the battery.'],
    ['If resistance goes up and voltage stays the same, current…', ['goes up', 'goes down', 'stays the same', 'becomes zero always'], 1, 'I = V ÷ R, so a bigger R means a smaller I.'],
    ['A 12 V battery is connected to a 4 Ω resistor. What is the current?', ['48 A', '3 A', '8 A', '0.33 A'], 1, 'I = 12 ÷ 4 = 3 A.']],
  'the roman republic': [
    ['Who ran the Roman Republic each year?', ['A king', 'Two elected consuls', 'The army', 'A single emperor'], 1, 'Two consuls were elected for one year.'],
    ['Why did Romans have two consuls instead of one?', ['To share work and stop one person getting too much power', 'Because one got tired', 'For tradition only', 'To fight two wars'], 0, 'Each consul could block the other, limiting power.'],
    ['Which modern idea comes from the Roman Republic?', ['Electing leaders for fixed terms', 'Kings ruling forever', 'Banning all votes', 'No laws'], 0, 'Fixed terms and elections are Republic ideas still used today.']],
  'quadratic equations': [
    ['Which of these is a quadratic equation?', ['x + 3 = 7', 'x² − 4 = 0', '2x = 10', 'x³ = 8'], 1, 'A quadratic has x² as its highest power.'],
    ['What are the solutions of (x − 2)(x − 5) = 0?', ['x = −2 or −5', 'x = 2 or 5', 'x = 10', 'x = 7'], 1, 'One bracket must be zero, so x = 2 or x = 5.'],
    ['A square has area 49 cm². How long is each side?', ['7 cm', '24.5 cm', '49 cm', '14 cm'], 0, 'x² = 49 gives x = 7 (a length cannot be negative).']]
};
function genericLesson(topic, subject, grade) {
  const t = esc(topic);
  return {
    hook: `This is a sample outline for <strong>${t}</strong>. Start the backend to get a full lesson written for Grade ${grade}.`,
    points: [`Write down what you already know about ${t}.`, `Find the three most important words linked to ${t} in your ${esc(subject)} textbook and look up what they mean.`, `Ask: why does ${t} matter in everyday life?`],
    example: `Explain ${t} to a friend in two sentences. If you can, you understand the main idea.`
  };
}
function genericQuiz(topic) {
  return [
    [`Which is the best first step to learn about "${topic}"?`, ['Learn the key words and what they mean', 'Skip to the hardest problem', 'Memorise random facts', 'Guess'], 0, 'Understanding key vocabulary comes first.'],
    [`How can you check that you really understand "${topic}"?`, ['Explain it in your own words', 'Read it once quickly', 'Copy the textbook', 'Ignore examples'], 0, 'If you can explain it simply, you understand it.'],
    [`Where might "${topic}" show up outside school?`, ['In real-life situations around you', 'Nowhere at all', 'Only in exams', 'Only in other countries'], 0, 'Most school topics connect to everyday life.']
  ];
}

function lessonHtml(c) {
  return `<p class="text-lg">${c.hook}</p>
    <h3>Key ideas</h3><ul>${c.points.map(p => `<li>${p}</li>`).join('')}</ul>
    <h3>In real life</h3><p>${c.example}</p>`;
}
function markdownToHtml(md) {
  const lines = esc(md).split('\n');
  let html = '', inList = false;
  for (let raw of lines) {
    let l = raw.trim().replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>');
    const li = l.match(/^(?:[-*•]|\d+\.)\s+(.*)$/);
    if (li) { if (!inList) { html += '<ul>'; inList = true; } html += `<li>${li[1]}</li>`; continue; }
    if (inList) { html += '</ul>'; inList = false; }
    if (!l || /^-{3,}$/.test(l)) continue;
    if (/^#{1,2}\s/.test(l)) continue;               // title is shown in the card header
    if (/^#{3,}\s/.test(l)) html += `<h3>${l.replace(/^#+\s*/, '')}</h3>`;
    else html += `<p>${l}</p>`;
  }
  return html + (inList ? '</ul>' : '');
}

// How well does a text fit a grade? Same rule the server uses.
function fitFor(diff, grade) {
  const allowed = grade <= 5 ? ['Easy'] : grade <= 8 ? ['Easy', 'Medium'] : ['Easy', 'Medium', 'Hard'];
  if (allowed.includes(diff)) return { ok: true, msg: `Good fit for Grade ${grade}` };
  return { ok: false, msg: `Might be hard for Grade ${grade}` };
}
const SAMPLE_TEXT = {
  easy: 'Plants make their own food using sunlight. Inside each green leaf are tiny parts called chloroplasts. They catch light from the sun and use it to join water from the soil with carbon dioxide from the air. The result is a kind of sugar called glucose, which the plant uses for energy so it can grow new leaves, roots and flowers. Oxygen is left over, and the plant lets it out into the air through small holes in its leaves. That oxygen is what people and animals breathe every day.',
  hard: 'Epigenetic mechanisms modulate gene expression without altering the underlying nucleotide sequence. DNA methylation and post-translational histone modifications dynamically regulate chromatin architecture, thereby governing transcriptional accessibility during cellular differentiation. Consequently, phenotypic heterogeneity can emerge among genetically identical cells, a phenomenon with considerable implications for developmental biology, oncogenesis and the heritability of environmentally induced characteristics. Experimental evidence additionally suggests that nutritional, psychological and toxicological exposures during critical developmental windows may establish persistent epigenetic configurations. Contemporary investigations increasingly integrate high-throughput sequencing with computational modelling to characterise these regulatory networks comprehensively.'
};

// Sample lesson for a topic, shifted one tier for Simpler / Challenge.
// Returns { html, source } where source is 'sample' or 'outline'.
function sampleLesson(topic, subject, grade, level) {
  const pack = SAMPLES[topic.toLowerCase()];
  let t = tierOf(grade);
  if (pack && level === 'Simpler') t = t === 'high' ? 'middle' : 'elementary';
  if (pack && level === 'Challenge') t = t === 'elementary' ? 'middle' : 'high';
  return { html: lessonHtml(pack ? pack[t] : genericLesson(topic, subject, grade)), source: pack ? 'sample' : 'outline' };
}

// Prefer hand-written questions over the backend simulator's generic ones.
function chooseQuiz(topic, apiQuestions) {
  const sample = SAMPLE_QUIZ[topic.toLowerCase()];
  if (sample && (!apiQuestions || /fundamental starting principle/i.test(apiQuestions[0][0]))) return sample;
  return apiQuestions || genericQuiz(topic);
}

// Plain-language tips from the 19 model features.
function readingTips(f) {
  const tips = [];
  if (f.avg_sentence_len > 20) tips.push(`Sentences average ${f.avg_sentence_len.toFixed(0)} words. Try splitting long ones.`);
  if (f.pct_long_words > 0.28) tips.push(`${Math.round(f.pct_long_words * 100)}% of words are long. Swap some for everyday words.`);
  if (f.commas_per_sentence > 2) tips.push('Lots of commas per sentence. Fewer clauses make it easier to follow.');
  return tips;
}

const api = { esc, tierOf, SAMPLES, SAMPLE_QUIZ, SAMPLE_TEXT, lessonHtml, markdownToHtml, fitFor,
  sampleLesson, chooseQuiz, readingTips, genericQuiz };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.LearnCraftContent = api;
})(typeof window !== 'undefined' ? window : globalThis);
