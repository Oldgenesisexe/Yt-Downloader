# YouTube Downloader Web App

## Overview
A Flask-based web application that allows users to download YouTube videos in MP4 format or extract audio as MP3.

## Project Structure
- `app.py` - Main Flask application with download routes
- `templates/index.html` - Frontend HTML template
- `requirements.txt` - Python dependencies
- `downloads/` - Folder where downloaded files are temporarily stored

## Dependencies
- Flask - Web framework
- yt-dlp - YouTube download library
- gunicorn - Production WSGI server
- ffmpeg - System dependency for audio extraction

## Running the App
The app runs on port 5000 with `python app.py` or `gunicorn app:app --bind 0.0.0.0:5000` for production.

## Features
- Download YouTube videos as MP4
- Extract and download audio as MP3
- Simple web interface
