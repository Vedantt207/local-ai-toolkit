# Local AI Data Toolkit

A self-hosted AI assistant stack using **Ollama**, **Open WebUI**, and **SearXNG**, with Python tools for automated data analysis and log file processing. Everything runs locally — no data leaves your machine.

---

## Contents

| File | Description |
|------|-------------|
| `docker-compose.yml` | Docker setup for Open WebUI and SearXNG |
| `Modelfile` | Ollama model configuration (LLaMA 3.1 8B, 64K context) |
| `settings.yml` | SearXNG configuration |
| `data_tool.py` | Standalone EDA script for Excel and CSV files |
| `data_analysis_tool.py` | Open WebUI tool — EDA and log file conversion |
| `web_search.py` | CLI web search via local SearXNG instance |
| `web_search_tool.py` | Open WebUI tool — web search via SearXNG |
| `sample_data.xlsx` | Sample Excel file for testing |
| `sample.log` | Sample log file for testing |

---

## Architecture

```
                    Browser
               localhost:3000
                     |
               Open WebUI
        (Chat interface + Tools)
               /           \
          Ollama          SearXNG
       LLaMA 3.1        localhost:8080
      (local LLM)      (private search)
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/) installed and running locally

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Set the SearXNG secret key

Open `settings.yml` and replace the placeholder value:

```yaml
server:
  secret_key: "your-own-random-secret-key-here"
```

To generate a strong key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the Docker services

```bash
docker compose up -d
```

This starts:
- Open WebUI at `http://localhost:3000`
- SearXNG at `http://localhost:8080`

### 4. Pull the AI model

```bash
ollama create mymodel -f Modelfile
```

Or pull the base model directly:

```bash
ollama pull llama3.1:8b-instruct-q4_K_M
```

### 5. Open the interface

Navigate to `http://localhost:3000`, create an account, and start chatting.

---

## Tools

### Data Analysis — `data_tool.py`

Runs a full Exploratory Data Analysis on any Excel or CSV file and produces a structured multi-sheet Excel report.

**Usage:**

```bash
python data_tool.py your_data.xlsx
```

**Output sheets:**

| Sheet | Contents |
|-------|----------|
| `Original` | Raw imported data |
| `Info` | Column types, missing counts, unique value counts |
| `Statistics` | Descriptive statistics for numeric columns |
| `Cleaned` | Missing values filled, duplicate rows removed |
| `Summary` | High-level dataset overview |
| `<col>_Top15` | Top 15 value counts for categorical columns |

### Web Search — `web_search.py`

Queries the local SearXNG instance from the command line.

**Usage:**

```bash
python web_search.py "your search query"
```

### Open WebUI Tools

`data_analysis_tool.py` and `web_search_tool.py` are designed to be loaded as tools inside Open WebUI, allowing the model to invoke them automatically during a conversation.

**To register a tool:**
1. Open WebUI > Settings > Tools
2. Upload or paste the tool file
3. Enable the tool in your chat session

---

## Configuration

### Docker Compose

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` | Ollama API endpoint |
| `RAG_TOP_K` | `10` | Number of top results used for retrieval |
| `CHUNK_SIZE` | `1000` | Document chunk size for RAG |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |

### Modelfile

| Setting | Value | Description |
|---------|-------|-------------|
| Base model | `llama3.1:8b-instruct-q4_K_M` | Quantized 8B instruct model |
| `num_ctx` | `65536` | Context window size (64K tokens) |

### Output Directory

By default, generated files are saved to `D:/stage1/output/`. To change this, update the `output_dir` variable in `data_tool.py` and `data_analysis_tool.py`.

---

## Security

- Do not commit a real `settings.yml` secret key to a public repository. Use environment variables or add the file to `.gitignore` for production use.
- SearXNG runs entirely on localhost — searches are not routed through any external tracking service.
- Ollama runs fully offline — no prompts or data are sent to external servers.

Recommended `.gitignore` entries:

```
settings.yml
.env
__pycache__/
*.pyc
```

---

## Troubleshooting

**Open WebUI cannot connect to Ollama**
Ensure Ollama is running with `ollama serve`. On Linux, replace `host.docker.internal` with `172.17.0.1` in `docker-compose.yml`.

**SearXNG returns no results**
Confirm it is reachable at `http://localhost:8080`. Verify that `json` is listed under `formats` in `settings.yml`.

**Port conflict on 8080**
Change the host port in `docker-compose.yml` from `"8080:8080"` to `"8081:8080"` (or any free port).

---

## License

MIT License — free to use, modify, and distribute.

---

## Built With

- [Ollama](https://ollama.com/)
- [Open WebUI](https://github.com/open-webui/open-webui)
- [SearXNG](https://github.com/searxng/searxng)
- [pandas](https://pandas.pydata.org/)
