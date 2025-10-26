#!/bin/bash

# Email Automation App - Quick Deployment Script
echo "🚀 Email Automation App Deployment Script"
echo "========================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists git; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Function for Streamlit Cloud deployment
deploy_streamlit_cloud() {
    echo "🌟 Deploying to Streamlit Cloud..."
    
    # Initialize git if not already done
    if [ ! -d ".git" ]; then
        git init
    fi
    
    # Add all files
    git add .
    git commit -m "Deploy email automation app"
    
    echo "📝 Next steps for Streamlit Cloud:"
    echo "1. Push to GitHub: git remote add origin <your-github-repo-url>"
    echo "2. Push: git push -u origin main"
    echo "3. Go to https://share.streamlit.io"
    echo "4. Connect your GitHub repository"
    echo "5. Set main file path to: app.py"
    echo "6. Click Deploy!"
}

# Function for Heroku deployment
deploy_heroku() {
    echo "🟣 Deploying to Heroku..."
    
    if ! command_exists heroku; then
        echo "❌ Heroku CLI is not installed."
        echo "Please install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Login to Heroku
    heroku login
    
    # Create app
    read -p "Enter your Heroku app name: " app_name
    heroku create $app_name
    
    # Deploy
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    echo "✅ Deployed to Heroku!"
    echo "🌐 Your app: https://$app_name.herokuapp.com"
}

# Function for Docker deployment
deploy_docker() {
    echo "🐳 Deploying with Docker..."
    
    if ! command_exists docker; then
        echo "❌ Docker is not installed."
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Build image
    docker build -t email-automation .
    
    # Run container
    docker run -d -p 8501:8501 --name email-automation-app email-automation
    
    echo "✅ Docker deployment complete!"
    echo "🌐 Your app: http://localhost:8501"
    echo "📊 View logs: docker logs email-automation-app"
}

# Function for local deployment
deploy_local() {
    echo "💻 Starting local deployment..."
    
    # Install requirements
    pip3 install -r requirements.txt
    
    # Start the app
    echo "🚀 Starting Streamlit app..."
    streamlit run app.py
}

# Main menu
echo ""
echo "Choose deployment option:"
echo "1) Streamlit Cloud (Free, Easy)"
echo "2) Heroku (Easy, Limited Free)"
echo "3) Docker (Local/Cloud)"
echo "4) Local Development"
echo "5) Show all options"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        deploy_streamlit_cloud
        ;;
    2)
        deploy_heroku
        ;;
    3)
        deploy_docker
        ;;
    4)
        deploy_local
        ;;
    5)
        echo ""
        echo "📚 All Deployment Options:"
        echo "========================"
        echo ""
        echo "🌟 Streamlit Cloud (Recommended):"
        echo "   - Free hosting"
        echo "   - Automatic deployments"
        echo "   - No server management"
        echo "   - Steps: Push to GitHub → Connect to share.streamlit.io"
        echo ""
        echo "🟣 Heroku:"
        echo "   - Easy deployment"
        echo "   - Limited free tier"
        echo "   - Steps: heroku create → git push heroku main"
        echo ""
        echo "🐳 Docker:"
        echo "   - Containerized deployment"
        echo "   - Works anywhere"
        echo "   - Steps: docker build → docker run"
        echo ""
        echo "☁️ Cloud Platforms:"
        echo "   - AWS EC2/ECS"
        echo "   - Google Cloud Run"
        echo "   - Azure Container Instances"
        echo "   - DigitalOcean Droplets"
        echo ""
        echo "💻 Local Development:"
        echo "   - streamlit run app.py"
        echo "   - Perfect for testing"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
