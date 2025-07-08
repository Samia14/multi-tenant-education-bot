FROM python:3.13-slim

############################
# 2. Create a non-root user (good security practice)
############################

WORKDIR /home/Educationbot

############################
# 3. Copy python dependencies first and install them —
#    this lets Docker cache the layer if code changes
############################
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

############################
# 4. Copy the rest of your application code
############################
COPY . .

############################
# 5. Expose Streamlit’s default port and
#    tell Streamlit to listen on all interfaces
############################
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

############################
# 6. Run the Streamlit app!
############################
CMD ["streamlit", "run", "app.py"]
