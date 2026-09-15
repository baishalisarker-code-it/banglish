const fs = require('fs');
const path = require('path');

let backendUrl = process.env.BACKEND_URL || '';

// If not in process.env, try reading .env file if it exists
const envPath = path.join(__dirname, '.env');
if (!backendUrl && fs.existsSync(envPath)) {
  const content = fs.readFileSync(envPath, 'utf8');
  const match = content.match(/^BACKEND_URL\s*=\s*['"]?([^'"\r\n]+)['"]?/m);
  if (match) {
    backendUrl = match[1].trim();
  }
}

const configContent = `// Auto-generated configuration from .env and deployment environment variables
window.APP_CONFIG = {
  BACKEND_URL: "${backendUrl}"
};
`;

fs.writeFileSync(path.join(__dirname, 'frontend', 'config.js'), configContent);
fs.writeFileSync(path.join(__dirname, 'config.js'), configContent);
console.log(`Generated config.js with BACKEND_URL: '${backendUrl}'`);
