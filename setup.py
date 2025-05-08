# setup.py - Run this script to set up your Django project
import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a shell command and print output"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_project_structure():
    """Create the Django project structure"""
    print("Creating Django project structure...")
    
    # Create main project
    if not os.path.exists("ecommerce_project"):
        run_command("django-admin startproject ecommerce_project .")
    
    # Create apps
    apps = ["core", "products", "users", "orders", "cart"]
    for app in apps:
        if not os.path.exists(app):
            run_command(f"python manage.py startapp {app}")
    
    # Create additional directories
    directories = ["media", "static", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("Project structure created successfully!")

def setup_environment():
    """Set up the virtual environment and install dependencies"""
    print("Setting up virtual environment...")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        run_command("python -m venv venv")
    
    # Determine the activate script path based on OS
    if sys.platform == "win32":
        activate_script = ".\\venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    # Install requirements
    print("Installing requirements...")
    run_command(f"{activate_script} && pip install -r requirements.txt")
    
    print("Environment setup completed!")

def initialize_database():
    """Initialize the database with migrations"""
    print("Initializing database...")
    
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")
    
    print("Database initialized!")
    
    # Create superuser prompt
    create_super = input("Do you want to create a superuser? (y/n): ")
    if create_super.lower() == 'y':
        run_command("python manage.py createsuperuser")

def main():
    """Main setup function"""
    print("Starting Django E-commerce project setup...")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found. Please create it first.")
        return
    
    # Setup steps
    setup_environment()
    create_project_structure()
    initialize_database()
    
    print("\nSetup complete! You can now run the development server with:")
    print("python manage.py runserver")
    
    # Run server prompt
    run_server = input("Do you want to run the server now? (y/n): ")
    if run_server.lower() == 'y':
        run_command("python manage.py runserver")

if __name__ == "__main__":
    main()