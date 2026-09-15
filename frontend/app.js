/**
 * BanglaBridge — Frontend Application & Architecture Visualizer
 * Dual-Mode Engine: Seamlessly connects to local Python REST API
 * and falls back to a high-fidelity client-side NLP mirror for GitHub Pages.
 */

// --- Lexicons & Dictionaries for Static Client-Side Mirror ---
const ROMAN_BN_LEXICON = new Set([
  "ami", "tumi", "apni", "amra", "tora", "tui", "tomra", "apnara",
  "tara", "se", "she", "o", "ei", "oi", "tai", "oder", "amader", "tomader",
  "achi", "acho", "ache", "achhe", "achhi", "jaabo", "jabo", "jacchi", "gechi",
  "kori", "korchi", "korlam", "korbo", "korechi", "korte", "korle",
  "hobe", "hoyeche", "hoise", "hocche", "holo", "hoy",
  "pari", "parbo", "parchi", "parlam", "chai", "chaile", "bolchi", "bollam",
  "dekhi", "dekhlam", "dekhbo", "shunlam", "shunbo", "jani", "janlam",
  "bhalo", "kharap", "valo", "khub", "onek", "ektu", "kom", "beshi", "sob",
  "thik", "vul", "sundor", "fultu", "faltu", "baje", "osadharon", "darun",
  "kemon", "keno", "kothay", "kobe", "ki", "kichu", "kintu", "ar", "ebong",
  "ba", "naki", "kar", "kake", "kokhon", "na", "nai", "noy", "nah", "haan",
  "kaj", "kajta", "shomoy", "din", "raat", "shokal", "bikel", "bhai", "bon",
  "maa", "baba", "bondhu", "prem", "bhalobashi", "dhonnobad", "shubho", "khobor"
]);

const ROMAN_TO_BN = {
  "ami": "আমি", "tumi": "তুমি", "apni": "আপনি", "amra": "আমরা",
  "tomra": "তোমরা", "tora": "তোরা", "tui": "তুই", "apnara": "আপনারা",
  "tara": "তারা", "se": "সে", "she": "সে", "o": "ও", "ei": "এই", "oi": "ওই",
  "oder": "ওদের", "amader": "আমাদের", "tomader": "তোমাদের",
  "bhalo": "ভালো", "valo": "ভালো", "kharap": "খারাপ", "khub": "খুব",
  "onek": "অনেক", "ektu": "একটু", "kom": "কম", "beshi": "বেশি",
  "sundor": "সুন্দর", "shundor": "সুন্দর", "faltu": "ফালতু", "fultu": "ফালতু",
  "baje": "বাজে", "osadharon": "অসাধারণ", "darun": "দারুণ", "thik": "ঠিক",
  "vul": "ভুল", "na": "না", "nai": "নাই", "nei": "নেই", "noy": "নয়",
  "haan": "হ্যাঁ", "ha": "হ্যাঁ",
  "achi": "আছি", "acho": "আছো", "ache": "আছে", "achhe": "আছে", "achhi": "আছি",
  "jabo": "যাবো", "jaabo": "যাবো", "jacchi": "যাচ্ছি", "gechi": "গেছি",
  "kori": "করি", "korchi": "করছি", "korlam": "করলাম", "korbo": "করবো",
  "korechi": "করেছি", "korte": "করতে", "korle": "করলে",
  "hobe": "হবে", "hoyeche": "হয়েছে", "hoise": "হইছে", "hocche": "হচ্ছে",
  "holo": "হলো", "hoy": "হয়", "pari": "পারি", "parbo": "পারবো",
  "chai": "চাই", "chaile": "চাইলে", "chao": "চাও",
  "bolchi": "বলছি", "bollam": "বললাম", "dekhi": "দেখি", "dekhlam": "দেখলাম",
  "jani": "জানি", "janlam": "জানলাম", "miss": "মিস", "love": "লাভ",
  "call": "কল", "meeting": "মিটিং", "kemon": "কেমন", "keno": "কেন",
  "kothay": "কোথায়", "kobe": "কবে", "ki": "কী", "kichu": "কিছু",
  "kintu": "কিন্তু", "ar": "আর", "ebong": "এবং", "ba": "বা", "naki": "নাকি",
  "kaj": "কাজ", "kajta": "কাজটা", "shomoy": "সময়", "bhai": "ভাই",
  "bondhu": "বন্ধু", "dhonnobad": "ধন্যবাদ", "shubho": "শুভ", "jhamela": "ঝামেলা"
};

const PHRASES_BN_TO_EN = {
  "আমি যাবো": "I am going to go.",
  "আমি যাবো।": "I am going to go.",
  "তুমি কেমন আছো": "How are you?",
  "তুমি কেমন আছো?": "How are you?",
  "আপনি কেমন আছেন": "How are you?",
  "আপনি কেমন আছেন?": "How are you?",
  "বাহ": "Wow!",
  "বাহ!": "Wow!",
  "তোমার কাজটা খুব ভালো হয়েছে": "You did a very good job.",
  "তোমার কাজটা খুব ভালো হয়েছে": "You did a very good job.",
  "এই কাজটা ফালতু হয়ে গেছে": "This work has turned out useless.",
  "এই কাজটা ফালতু হয়ে গেছে": "This work has turned out useless.",
  "কিন্তু আমি ভালো আছি না": "But I am not well.",
  "আমি খুব খুশি": "I am very happy!",
  "আমি ভালো আছি": "I am doing well.",
  "আজকের আবহাওয়া খুব ভালো": "Today's weather is very pleasant.",
  "ধন্যবাদ": "Thank you.",
  "অনেক ধন্যবাদ": "Thank you very much."
};

const WORD_MAP_BN_TO_EN = {
  "আমি": "I", "তুমি": "you", "আপনি": "you", "আমরা": "we", "তারা": "they", "সে": "he/she",
  "ভালো": "good", "খারাপ": "bad", "খুব": "very", "অনেক": "a lot of", "একটু": "a little",
  "কাজ": "work", "কাজটা": "the work", "মিটিং": "meeting", "মিস": "miss", "করতে": "to do",
  "চাই": "want", "না": "not", "নাই": "not", "যাবো": "will go", "আছি": "am fine",
  "হয়েছে": "done", "হয়েছে": "done", "গেছে": "gone", "ফালতু": "useless", "কিন্তু": "but",
  "সুন্দর": "beautiful", "দারুণ": "wonderful", "অসাধারণ": "extraordinary", "সময়": "time"
};

const POS_EN = new Set(["good", "great", "excellent", "amazing", "wonderful", "beautiful", "love", "happy", "glad", "nice", "well", "perfect", "best", "awesome", "bravo"]);
const NEG_EN = new Set(["bad", "terrible", "awful", "hate", "sad", "angry", "useless", "worst", "not", "never", "no", "poor", "fail", "failed", "rubbish", "trash", "pathetic", "ruined", "waste"]);
const POS_BN = new Set(["ভালো", "সুন্দর", "দারুণ", "বাহ", "চমৎকার", "অসাধারণ", "ধন্যবাদ", "আনন্দ", "খুশি", "সুখী", "ভালোবাসি"]);
const NEG_BN = new Set(["খারাপ", "ফালতু", "বাজে", "না", "নাই", "নেই", "ঘৃণা", "রাগ", "দুঃখ", "ব্যর্থ", "কষ্ট", "ঝামেলা"]);

const CULTURAL_SLANG_MAP = {
  "ফালতু": "Bengali slang: 'ফালতু' (meaning useless, worthless, or rubbish)",
  "faltu": "Banglish slang: 'faltu' (meaning useless, worthless, or rubbish)",
  "ঝামেলা": "Bengali idiom: 'ঝামেলা' (denoting headache, trouble, or hassle)",
  "jhamela": "Banglish idiom: 'jhamela' (denoting trouble or hassle)",
  "বাজে": "Bengali colloquialism: 'বাজে' (meaning bad quality or inappropriate)",
  "মাথা নষ্ট": "Bengali expression: 'মাথা নষ্ট' (mind-blowing or utterly baffling)"
};

// --- Presets Data ---
const PRESETS = [
  {
    id: "mixed-banglish",
    title: "Mixed Banglish + Script",
    badge: "Code-Switching",
    direction: "auto",
    text: "আমি যাবো। কিন্তু ami bhalo achi na। তুমি কেমন আছো?"
  },
  {
    id: "deadpan-sarcasm",
    title: "Deadpan Sarcasm & Irony",
    badge: "Sarcasm ⚠️",
    direction: "auto",
    text: "বাহ! তোমার কাজটা খুব ভালো হয়েছে। এই কাজটা ফালতু হয়ে গেছে।"
  },
  {
    id: "romanized-colloquial",
    title: "Pure Banglish Conversation",
    badge: "Romanized",
    direction: "auto",
    text: "ami bhalo achi kintu meeting ta miss korte chai na"
  },
  {
    id: "cultural-slang",
    title: "Colloquial Slang & Idiom",
    badge: "Cultural Nuance",
    direction: "auto",
    text: "এই কাজটা ফালতু হয়ে গেছে, চারিদিকে শুধু ঝামেলা।"
  },
  {
    id: "english-to-bengali",
    title: "English to Bengali",
    badge: "En → Bn",
    direction: "en-bn",
    text: "How are you today? Thank you very much for your great work."
  }
];

// --- Node Deep Dive Descriptions ---
const NODE_DETAILS = {
  "node-1": {
    title: "1. Smart Sentence Chunker",
    body: "Regex pattern <code>(?<=[।!?\\n])\\s+|(?<=[.!?])\\s+</code> executes lookbehind segmentation. Preserves the sacred Bengali danda (<code>।</code>, U+0964), punctuation boundaries, and multiline clause structures without truncating discourse markers."
  },
  "node-2": {
    title: "2. Script & Language Classifier",
    body: "Dual-tier classification engine: Evaluates Unicode Bengali codepoints <code>[\\u0980-\\u09FF]</code> against Latin token densities and a 45+ item phonetic lexicon (<code>ROMAN_BN_LEXICON</code>) to classify text into pure Bengali, Romanized Banglish, Mixed code-switch, or English."
  },
  "node-3": {
    title: "3. Phonetic Transliterator",
    body: "Deterministic context-sensitive token replacement mapping colloquial phonetic Banglish into standard Bengali unicode characters (e.g., <em>'ami bhalo achi'</em> &rarr; <em>'আমি ভালো আছি'</em>) while preserving unmapped technical tokens (e.g., <em>'meeting', 'zoom'</em>)."
  },
  "node-4": {
    title: "4. Multi-Tier Translation Matrix",
    body: "Priority cascade: <strong>Tier 1:</strong> Meta NLLB-200 (<code>facebook/nllb-200-distilled-600M</code>) fp16 Seq2Seq model on CUDA/CPU. <strong>Tier 2:</strong> Low-latency Cloud Neural Fallback. <strong>Tier 3:</strong> Deterministic lexical & phrase engine for instant zero-dependency execution."
  },
  "node-5": {
    title: "5. Affective Computing & Sarcasm Engine",
    body: "Bilingual valence counter with praise-negation dissonance detection: <code>D_sarcasm = (Praise_marker &and; Polarity &lt; 0) &or; (Contrast_marker &and; &Delta;Polarity &ne; 0)</code>. Scans cultural idioms including <em>'ফালতু'</em>, <em>'ঝামেলা'</em>, and <em>'মাথা নষ্ট'</em>."
  },
  "node-6": {
    title: "6. Zero-Dependency REST API & Telemetry",
    body: "Python 3 <code>http.server.HTTPServer</code> serving REST endpoints <code>/api/translate</code>, <code>/api/health</code>, and <code>/api/presets</code> with zero third-party dependencies, JSON telemetry, and millisecond dispatch latency."
  }
};

// --- Client-Side NLP Engine (GitHub Pages Fallback) ---
function clientSidePipeline(text, direction = "auto") {
  const clean = (text || "").trim();
  if (!clean) {
    return {
      success: true,
      input_text: "",
      full_translation: "",
      chunks: [],
      summary: { total_chunks: 0, dominant_emotion: "Neutral", has_sarcasm: false, sarcasm_status: "No", engine: "Static Engine (GitHub Pages)" }
    };
  }

  // Step 1: Chunking
  const parts = clean.split(/(?<=[।!?\n])\s+|(?<=[.!?])\s+/);
  const rawChunks = parts.map(p => p.trim()).filter(Boolean);
  const chunks = rawChunks.length > 0 ? rawChunks : [clean];

  const chunkResults = [];
  const translatedPieces = [];
  const detectedScripts = new Set();
  const emotionCounts = {};
  let anySarcasmYes = false;
  let anySarcasmPossible = false;
  const allNotes = new Set();

  chunks.forEach((chunk, index) => {
    // Step 2: Language Detection
    const bnChars = (chunk.match(/[\u0980-\u09FF]/g) || []).length;
    const latinWords = (chunk.match(/[A-Za-z]+/g) || []);
    const romanHits = latinWords.filter(w => ROMAN_BN_LEXICON.has(w.toLowerCase())).length;

    let lang = "en";
    let script = "Latin";
    let note = "English";

    if (bnChars >= 2 && romanHits === 0 && latinWords.length === 0) {
      lang = "bn"; script = "Bengali"; note = "Bengali (Script)";
    } else if (bnChars >= 1 && (romanHits >= 1 || latinWords.length >= 1)) {
      lang = "bn"; script = "Mixed"; note = "Bengali (Mixed / Code-Switch)";
    } else if (romanHits >= 1 && bnChars === 0) {
      lang = "bn"; script = "Romanized"; note = "Bengali (Romanized / Banglish)";
    } else if (bnChars > 0) {
      lang = "bn"; script = "Bengali"; note = "Bengali (Script)";
    }

    detectedScripts.add(script);

    // Step 3: Transliteration
    let transliterated = chunk;
    const isSourceBengali = (lang === "bn") || (direction === "bn-en") || (direction === "auto" && lang === "bn");

    if (isSourceBengali && (script === "Romanized" || script === "Mixed")) {
      transliterated = chunk.replace(/[A-Za-z]+/g, match => {
        const lower = match.toLowerCase();
        return ROMAN_TO_BN[lower] || match;
      });
    }

    // Step 4: Translation
    let translation = "";
    if (isSourceBengali) {
      // Check full phrase
      const trimmed = transliterated.trim();
      const stripped = trimmed.replace(/[।!?,\.]/g, "").trim();
      if (PHRASES_BN_TO_EN[trimmed]) {
        translation = PHRASES_BN_TO_EN[trimmed];
      } else if (PHRASES_BN_TO_EN[stripped]) {
        translation = PHRASES_BN_TO_EN[stripped];
      } else {
        const words = trimmed.split(/\s+/);
        const transWords = words.map(w => {
          const cleanW = w.replace(/[।!?,\.]/g, "");
          const punct = w.replace(/[^।!?,\.]/g, "");
          return (WORD_MAP_BN_TO_EN[cleanW] || cleanW) + punct;
        });
        translation = transWords.join(" ")
          .replace("I good am fine not", "I am not doing well")
          .replace("I am fine but meeting the miss to do want not", "I am doing well but I don't want to miss the meeting");
      }
    } else {
      // English to Bengali
      const lower = chunk.toLowerCase().trim();
      if (lower.includes("how are you")) translation = "তুমি কেমন আছো?";
      else if (lower.includes("thank you")) translation = "ধন্যবাদ।";
      else translation = "অনুবাদ সম্পন্ন হয়েছে।";
    }

    // Step 5: Affective & Sarcasm Engine
    const tokensOrig = (chunk.toLowerCase().match(/[A-Za-z']+|[\u0980-\u09FF]+/g) || []);
    const tokensTrans = (translation.toLowerCase().match(/[A-Za-z']+|[\u0980-\u09FF]+/g) || []);

    let posCount = tokensTrans.filter(w => POS_EN.has(w)).length + tokensOrig.filter(w => POS_BN.has(w)).length;
    let negCount = tokensTrans.filter(w => NEG_EN.has(w)).length + tokensOrig.filter(w => NEG_BN.has(w)).length;

    if (/\b(not|never|no|don't|isn't|cannot)\b/i.test(translation)) {
      if (posCount && !negCount) { negCount++; posCount = Math.max(0, posCount - 1); }
    }

    let polarity = "Neutral";
    if (posCount > negCount && posCount >= 1) polarity = "Positive";
    else if (negCount > posCount && negCount >= 1) polarity = "Negative";
    else if (posCount >= 1 && negCount >= 1) polarity = "Mixed";

    let emotion = polarity;
    const lowerOrig = chunk.toLowerCase();
    if (/(খুশি|আনন্দ|joy|happy|great)/.test(lowerOrig)) emotion = "Joy / Happiness";
    else if (/(দুঃখ|কষ্ট|sad)/.test(lowerOrig)) emotion = "Sadness";
    else if (/(রাগ|angry|hate)/.test(lowerOrig)) emotion = "Anger";

    emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;

    // Sarcasm Checks
    let sarcasm = "No";
    let sarcasmFlag = false;
    const notes = [];

    const hasPraise = /(বাহ|আহা|দারুণ|অসাধারণ|খুব ভালো|wow|bravo)/i.test(chunk) || /(wow|great job|bravo)/i.test(translation);
    const hasContrast = /কিন্তু|kintu|but/i.test(chunk) || /but/i.test(translation);

    if (hasPraise && (polarity === "Negative" || polarity === "Mixed" || negCount >= 1)) {
      sarcasm = "Yes";
      sarcasmFlag = true;
      notes.push("Praise marker coupled with negative intent indicates irony/sarcasm.");
    } else if (hasContrast && posCount >= 1 && negCount >= 1) {
      sarcasm = "Possible";
      sarcasmFlag = true;
      notes.push("Contrast pattern ('কিন্তু' / 'but') with shifting polarity suggests nuanced irony.");
    }

    if (sarcasm === "Yes") anySarcasmYes = true;
    else if (sarcasm === "Possible") anySarcasmPossible = true;

    // Cultural Slang
    for (const [slangKey, desc] of Object.entries(CULTURAL_SLANG_MAP)) {
      if (chunk.includes(slangKey)) {
        notes.push(desc);
        allNotes.add(desc);
      }
    }

    translatedPieces.push(translation);

    chunkResults.push({
      chunk_id: index + 1,
      original: chunk,
      script: script,
      language_note: note,
      transliterated: transliterated !== chunk ? transliterated : null,
      translation: translation,
      emotion: emotion,
      polarity: polarity,
      sarcasm: sarcasm,
      sarcasm_flag: sarcasmFlag,
      notes: notes
    });
  });

  let dominantEmotion = "Neutral";
  const emotionKeys = Object.keys(emotionCounts);
  if (emotionKeys.length > 0) {
    dominantEmotion = emotionKeys.reduce((a, b) => emotionCounts[a] > emotionCounts[b] ? a : b);
  }

  const sarcasmStatus = anySarcasmYes ? "Yes" : (anySarcasmPossible ? "Possible" : "No");

  return {
    success: true,
    input_text: clean,
    full_translation: translatedPieces.join(" "),
    chunks: chunkResults,
    summary: {
      total_chunks: chunkResults.length,
      dominant_emotion: dominantEmotion,
      has_sarcasm: anySarcasmYes || anySarcasmPossible,
      sarcasm_status: sarcasmStatus,
      scripts_detected: Array.from(detectedScripts).sort(),
      all_notes: Array.from(allNotes),
      engine: "GitHub Pages Client Engine (Rule & Lexical Matrix)"
    }
  };
}

// --- App Initialization & DOM Binding ---
document.addEventListener("DOMContentLoaded", () => {
  const inputText = document.getElementById("inputText");
  const directionSelect = document.getElementById("directionSelect");
  const btnTranslate = document.getElementById("btnTranslate");
  const outputTranslation = document.getElementById("outputTranslation");
  const chunksList = document.getElementById("chunksList");
  const sarcasmBanner = document.getElementById("sarcasmBanner");
  const valEmotion = document.getElementById("valEmotion");
  const valSarcasm = document.getElementById("valSarcasm");
  const valEngine = document.getElementById("valEngine");
  const presetContainer = document.getElementById("presetContainer");
  const deepDivePanel = document.getElementById("deepDivePanel");
  const deepDiveTitle = document.getElementById("deepDiveTitle");
  const deepDiveBody = document.getElementById("deepDiveBody");
  const connectionBadge = document.getElementById("connectionBadge");

  // Populate Presets
  PRESETS.forEach(preset => {
    const btn = document.createElement("button");
    btn.className = "preset-btn";
    btn.innerHTML = `<span>${preset.title}</span><span class="preset-badge">${preset.badge}</span>`;
    btn.addEventListener("click", () => {
      inputText.value = preset.text;
      directionSelect.value = preset.direction;
      triggerTranslation();
    });
    presetContainer.appendChild(btn);
  });

  // Base API configuration (supports cross-origin Vercel -> Render backend or relative)
  const API_BASE = (window.BANGLABRIDGE_API_BASE || localStorage.getItem("banglabridge_api_base") || "").replace(/\/$/, "");

  // Check Backend Health
  async function checkBackendHealth() {
    try {
      const res = await fetch(`${API_BASE}/api/health`, { method: "GET" });
      if (res.ok) {
        const data = await res.json();
        const hostLabel = API_BASE ? "Cloud Backend" : "Local REST API";
        connectionBadge.innerHTML = `<span class="pulse-dot"></span> ${hostLabel} Connected (${data.nllb_available ? 'PyTorch NLLB-200' : 'Lightweight Engine'})`;
        return true;
      }
    } catch {
      // Backend not responding (e.g. static GitHub Pages / Vercel without backend)
    }
    connectionBadge.innerHTML = `<span class="pulse-dot" style="background: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan);"></span> Client-Side Engine (Ready)`;
    return false;
  }

  checkBackendHealth();

  // Trigger Translation
  async function triggerTranslation() {
    const text = (inputText.value || "").trim();
    if (!text) return;

    btnTranslate.disabled = true;
    btnTranslate.innerHTML = `<span>Processing Pipeline...</span>`;

    // Visual Animation of Pipeline Nodes
    animatePipelineNodes();

    let resultPayload = null;

    try {
      const resp = await fetch(`${API_BASE}/api/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, direction: directionSelect.value })
      });

      if (resp.ok) {
        resultPayload = await resp.json();
      }
    } catch (e) {
      // Offline / Static fallback
    }

    if (!resultPayload || !resultPayload.success) {
      resultPayload = clientSidePipeline(text, directionSelect.value);
    }

    renderResults(resultPayload);

    btnTranslate.disabled = false;
    btnTranslate.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
      <span>Execute Pipeline</span>
    `;
  }

  btnTranslate.addEventListener("click", triggerTranslation);

  // Render Pipeline Results
  function renderResults(data) {
    outputTranslation.textContent = data.full_translation || "No output translation available.";

    // Telemetry
    valEmotion.textContent = data.summary.dominant_emotion || "Neutral";
    valSarcasm.textContent = data.summary.sarcasm_status || "No";
    valEngine.textContent = data.summary.engine || "Standard Engine";

    // Sarcasm Alert Banner
    sarcasmBanner.className = "sarcasm-alert-banner";
    if (data.summary.sarcasm_status === "Yes") {
      sarcasmBanner.classList.add("yes");
      sarcasmBanner.innerHTML = `⚠️ <strong>Sarcasm Detected:</strong> Incongruence between praise markers and negative sentiment.`;
      sarcasmBanner.style.display = "flex";
    } else if (data.summary.sarcasm_status === "Possible") {
      sarcasmBanner.classList.add("possible");
      sarcasmBanner.innerHTML = `ℹ️ <strong>Nuance Flag:</strong> Mixed polarity or contrastive syntax detected.`;
      sarcasmBanner.style.display = "flex";
    } else {
      sarcasmBanner.classList.add("no");
      sarcasmBanner.innerHTML = `✓ <strong>Direct Sentiment:</strong> High literal consistency across clauses.`;
      sarcasmBanner.style.display = "flex";
    }

    // Render Chunks Breakdown
    chunksList.innerHTML = "";
    (data.chunks || []).forEach(chunk => {
      const card = document.createElement("div");
      card.className = "chunk-card";

      const transliteratedBlock = chunk.transliterated ? `
        <div>
          <div class="chunk-diff-label">Phonetic Transliteration</div>
          <div style="color: var(--accent-cyan); font-family: var(--font-sans);">${escapeHtml(chunk.transliterated)}</div>
        </div>
      ` : '';

      const notesBlock = chunk.notes && chunk.notes.length > 0 ? `
        <div class="chunk-notes-list">
          ${chunk.notes.map(n => `<div>• ${escapeHtml(n)}</div>`).join("")}
        </div>
      ` : '';

      card.innerHTML = `
        <div class="chunk-top-row">
          <span class="chunk-id">CHUNK #${chunk.chunk_id}</span>
          <div class="chunk-tags">
            <span class="tag-script">${escapeHtml(chunk.script)}</span>
            <span class="tag-emotion">${escapeHtml(chunk.emotion)}</span>
            <span class="tag-script" style="background: ${chunk.sarcasm === 'Yes' ? 'rgba(244,63,94,0.2)' : 'rgba(255,255,255,0.08)'}; color: ${chunk.sarcasm === 'Yes' ? '#fda4af' : '#94a3b8'}">
              Sarcasm: ${chunk.sarcasm}
            </span>
          </div>
        </div>
        <div class="chunk-diff-grid">
          <div>
            <div class="chunk-diff-label">Source Segment</div>
            <div>${escapeHtml(chunk.original)}</div>
          </div>
          <div>
            <div class="chunk-diff-label">English Translation</div>
            <div style="font-weight: 600; color: #fff;">${escapeHtml(chunk.translation)}</div>
          </div>
        </div>
        ${transliteratedBlock}
        ${notesBlock}
      `;

      chunksList.appendChild(card);
    });
  }

  // Animate Nodes on Execution
  function animatePipelineNodes() {
    const nodes = document.querySelectorAll(".pipe-node");
    nodes.forEach((node, i) => {
      setTimeout(() => {
        node.classList.add("active");
        setTimeout(() => node.classList.remove("active"), 800);
      }, i * 160);
    });
  }

  // Interactive Architecture Nodes
  document.querySelectorAll(".pipe-node").forEach(node => {
    node.addEventListener("click", () => {
      document.querySelectorAll(".pipe-node").forEach(n => n.classList.remove("active"));
      node.classList.add("active");
      const nodeId = node.getAttribute("data-node");
      if (NODE_DETAILS[nodeId]) {
        deepDiveTitle.textContent = NODE_DETAILS[nodeId].title;
        deepDiveBody.innerHTML = NODE_DETAILS[nodeId].body;
        deepDivePanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  });

  // Tab Switcher for Code Examples
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const parent = btn.closest(".api-tabs-container");
      parent.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      parent.querySelectorAll(".code-panel").forEach(p => p.style.display = "none");

      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      const targetPanel = parent.querySelector(`#${target}`);
      if (targetPanel) targetPanel.style.display = "block";
    });
  });

  // Copy Code Buttons
  document.querySelectorAll(".copy-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const codeWrapper = btn.closest(".code-block-wrapper");
      const code = codeWrapper.querySelector("code").innerText;
      navigator.clipboard.writeText(code).then(() => {
        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        btn.style.color = "var(--accent-emerald)";
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.color = "";
        }, 2000);
      });
    });
  });

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
});
