FROM python:3.11-slim

LABEL maintainer="BookCart Automation Team"
LABEL description="Playwright test automation framework for BookCart"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and dependencies
RUN playwright install --with-deps chromium firefox webkit

# Copy project files
COPY . .

# Create directories for test results
RUN mkdir -p allure-results test-results/screenshots logs

# Set environment variables
ENV HEADLESS=true
ENV PYTHONUNBUFFERED=1
ENV PATH="/app:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from config import get_settings; get_settings()" || exit 1

# Default command to run tests
ENTRYPOINT ["pytest"]
CMD ["tests/", "-v", "--tb=short", "--alluredir=allure-results"]
