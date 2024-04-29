#!/bin/sh
# Start Uvicorn processes
echo "Starting ax_logger producer."

exec faststream run src.server.app:app
