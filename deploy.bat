@echo off
echo 🚀 Email Automation App Deployment Script
echo ========================================

echo 📋 Checking prerequisites...

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

echo.
echo Choose deployment option:
echo 1) Streamlit Cloud (Free, Easy)
echo 2) Heroku (Easy, Limited Free)
echo 3) Docker (Local/Cloud)
echo 4) Local Development
echo 5) Show all options
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto streamlit_cloud
if "%choice%"=="2" goto heroku
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto local
if "%choice%"=="5" goto show_options
goto invalid_choice

:streamlit_cloud
echo 🌟 Deploying to Streamlit Cloud...
echo.
echo 📝 Next steps for Streamlit Cloud:
echo 1. Push to GitHub: git remote add origin ^<your-github-repo-url^>
echo 2. Push: git push -u origin main
echo 3. Go to https://share.streamlit.io
echo 4. Connect your GitHub repository
echo 5. Set main file path to: app.py
echo 6. Click Deploy!
echo.
echo Your app will be live at: https://your-app-name.streamlit.app
goto end

:heroku
echo 🟣 Deploying to Heroku...
where heroku >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI is not installed.
    echo Please install from: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)
echo Please follow these steps:
echo 1. heroku login
echo 2. heroku create your-app-name
echo 3. git add .
echo 4. git commit -m "Deploy to Heroku"
echo 5. git push heroku main
goto end

:docker
echo 🐳 Deploying with Docker...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed.
    echo Please install Docker from: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)
echo Building Docker image...
docker build -t email-automation .
echo Running container...
docker run -d -p 8501:8501 --name email-automation-app email-automation
echo ✅ Docker deployment complete!
echo 🌐 Your app: http://localhost:8501
goto end

:local
echo 💻 Starting local deployment...
echo Installing requirements...
pip install -r requirements.txt
echo 🚀 Starting Streamlit app...
streamlit run app.py
goto end

:show_options
echo.
echo 📚 All Deployment Options:
echo ========================
echo.
echo 🌟 Streamlit Cloud (Recommended):
echo    - Free hosting
echo    - Automatic deployments
echo    - No server management
echo    - Steps: Push to GitHub → Connect to share.streamlit.io
echo.
echo 🟣 Heroku:
echo    - Easy deployment
echo    - Limited free tier
echo    - Steps: heroku create → git push heroku main
echo.
echo 🐳 Docker:
echo    - Containerized deployment
echo    - Works anywhere
echo    - Steps: docker build → docker run
echo.
echo ☁️ Cloud Platforms:
echo    - AWS EC2/ECS
echo    - Google Cloud Run
echo    - Azure Container Instances
echo    - DigitalOcean Droplets
echo.
echo 💻 Local Development:
echo    - streamlit run app.py
echo    - Perfect for testing
goto end

:invalid_choice
echo ❌ Invalid choice. Please run the script again.
pause
exit /b 1

:end
echo.
echo 🎉 Deployment process completed!
echo 📖 For detailed instructions, see DEPLOYMENT_GUIDE.md
pause
