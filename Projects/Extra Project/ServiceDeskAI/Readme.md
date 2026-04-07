# Project Setup

This project uses **Poetry** for dependency management within a local virtual environment.

---

## 🚀 Quick Start

Follow these steps to set up the environment and install the necessary dependencies.

### 1. Create and Activate Virtual Environment

Run the following commands to isolate your project dependencies:

```powershell
# Create the virtual environment folder
python -m venv .venv

# Activate the environment (Windows)
.\.venv\Scripts\activate

# Run the following command to run to set poetry
pip install poetry

# Add the required package
poetry add pandas
poetry add numpy
poetry add Django

# Add .env file
.env
```

---

## 👩‍🏫 Project Setup Guide for consumer of this repo

This project uses **Poetry** for dependency management. Follow these steps to set up your local environment.

### 🚀 Installation

1. **Clone the repository** and navigate to the project folder.

2. **Configure Poetry** to create a local virtual environment:

```powershell
# Create the virtual environment folder
python -m venv .venv

# Activate the environment (Windows)
.\.venv\Scripts\activate

# Run the following command to run to set poetry
pip install poetry

# Run the following command to install all package from 
poetry install
```

---

## Others Links

- [ChatGPT share link](https://chatgpt.com/share/69d5619b-ac44-83a7-a6c0-5f1214624496)