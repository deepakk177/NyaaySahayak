# ============================================================
# NyaySahayak — Dockerfile (Render / single-container)
# External PostgreSQL is provided via DATABASE_URL env var.
# ============================================================

FROM python:3.10-slim

WORKDIR /app

# ── System dependencies ──────────────────────────────────────
# Tesseract OCR (English + Hindi), OpenCV runtime libs,
# poppler-utils for pdf2image
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ──────────────────────────────────────
# Copy requirements first → Docker caches this layer separately,
# so re-builds after source-only changes skip pip install.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Application source ───────────────────────────────────────
COPY . /app

# ── Ensure writable runtime dirs exist ───────────────────────
RUN mkdir -p /app/data/uploads \
    /app/data/temp \
    /app/data/faiss_index \
    /app/logs

# ── Streamlit port (Render auto-detects EXPOSE) ─────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Entrypoint ───────────────────────────────────────────────
# DATABASE_URL must be set as an environment variable in Render's
# dashboard (Settings → Environment).  No DB credentials are
# baked into this image.
CMD ["streamlit", "run", "ui/streamlit_app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
