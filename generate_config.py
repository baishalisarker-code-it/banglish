"""
Generates frontend/config.js from .env and environment variables.
Runs during local startup and as a Vercel Build Step.
"""

import os

def load_env():
    env_vars = {}
    env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

def main():
    file_vars = load_env()
    backend_url = os.environ.get("BACKEND_URL", file_vars.get("BACKEND_URL", ""))
    
    config_content = f"""// Auto-generated configuration from .env and deployment environment variables
window.APP_CONFIG = {{
  BACKEND_URL: "{backend_url}"
}};
"""
    frontend_config_path = os.path.join(os.path.dirname(__file__), "frontend", "config.js")
    root_config_path = os.path.join(os.path.dirname(__file__), "config.js")

    with open(frontend_config_path, "w", encoding="utf-8") as f:
        f.write(config_content)

    with open(root_config_path, "w", encoding="utf-8") as f:
        f.write(config_content)

    print(f"Generated config.js with BACKEND_URL: '{backend_url}'")

if __name__ == "__main__":
    main()
