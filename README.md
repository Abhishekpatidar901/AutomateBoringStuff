![image](https://github.com/Abhishekpatidar901/TaskForger/assets/46681150/37ffe08b-02a8-438e-ad5b-a1ee8db04e80)



# TaskForge - Unified AI and Automation Solutions with Django 

This automation platform is developed using Django and features several advanced functionalities including CSV data import/export, bulk email sending with tracking, image compression using PIL, a large language model (LLM)-powered PDF reader, and an AI-based quiz generator using OpenAI.

## Features

### CSV Data Import/Export
- Supports importing and exporting large CSV files.
- Provides an intuitive interface for handling bulk data operations efficiently.

### Bulk Email Sending with Tracking
- Enables sending bulk emails with tracking capabilities.
- Tracks delivery status, open rates, and click-through rates for email campaigns.

### Image Compression Using PIL
- Optimizes images before storage or delivery.
- Reduces bandwidth usage and improves loading times for image-heavy content.

### LLM-powered PDF Reader
- Utilizes PyPDF2 for text extraction.
- Integrates OpenAI’s API with LangChain and FAISS for advanced query handling and similarity searches.
- Allows users to query PDF documents and receive relevant answers or extract information based on context.

### AI-based Quiz Generator
- Uses OpenAI to create customized quizzes based on input data.
- Generates questions and answers, ensuring quizzes are both challenging and educational.

## Technical Implementation

### Asynchronous Operations with Celery and Redis
- Manages large file operations and bulk email sending efficiently using Celery and Redis.
- Handles tasks in the background, ensuring the main application remains responsive.

### PDF Reader with LLM Integration
- Extracts text from PDF documents using PyPDF2.
- Enhances functionality with OpenAI’s API, LangChain, and FAISS for query responses and similarity searches.

### Image Compression with PIL
- Reduces the size of images by adjusting quality and dimensions.
- Optimizes images for web use and storage.

### AI-based Quiz Generation with OpenAI
- Processes input data using OpenAI to generate relevant quiz content.
- Automates quiz creation, ensuring high-quality content.

### Deployment and Scalability
- Deployed on an AWS EC2 instance.
- Uses Waitress as the WSGI server and Nginx as the reverse proxy.
- Ensures optimized performance and scalability.

## Technology Stack
- **Python**: Primary programming language.
- **Django**: Web framework.
- **Celery**: Asynchronous task management.
- **Redis**: Message broker for Celery.
- **OpenAI**: Provides LLM capabilities.
- **LangChain**: Manages language model interactions.
- **FAISS**: Used for similarity searches.
- **PyPDF2**: PDF text extraction.
- **PIL**: Image compression.
- **Waitress**: WSGI server.
- **Nginx**: Reverse proxy and load balancer.

