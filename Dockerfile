FROM python:3.11-slim

# Create the same UID (1000) that Spaces uses when running your container
RUN useradd -m -u 1000 user

# Install Python dependencies before copying the entire source tree
WORKDIR /home/user/app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app and switch to the non-root user
COPY --chown=user . .
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH

EXPOSE 7860

ENV MY_SETTING=default_value

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]