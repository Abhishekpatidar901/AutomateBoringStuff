# pdfapp/views.py
import os
import tempfile
import base64
from dotenv import load_dotenv
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from .forms import PDFUploadForm

load_dotenv()

def ask_pdf(request):
    response = ""
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        return HttpResponse("OpenAI API key not found. Please set it in the .env file.", status=500)

    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if 'pdf' in request.FILES:
                pdf = request.FILES['pdf']
                pdf_data = pdf.read()
                encoded_pdf_data = base64.b64encode(pdf_data).decode('utf-8')
                with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
                    temp_file.write(pdf_data)
                    temp_file_path = temp_file.name
                pdf_reader = PdfReader(temp_file_path)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text)

                # Store the chunks in cache
                cache_key = f'chunks_{request.session.session_key}'
                cache.set(cache_key, chunks, timeout=3600)  # Cache for 1 hour
                request.session['pdf_data'] = encoded_pdf_data
                request.session['pdf_name'] = pdf.name
                request.session.modified = True
            else:
                # Load the chunks from the cache
                cache_key = f'chunks_{request.session.session_key}'
                chunks = cache.get(cache_key)
                if not chunks:
                    return HttpResponse("No PDF processed. Please upload a PDF first.", status=400)

                encoded_pdf_data = request.session.get('pdf_data')
                if encoded_pdf_data:
                    pdf_data = base64.b64decode(encoded_pdf_data)
                    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
                        temp_file.write(pdf_data)
                        temp_file_path = temp_file.name
                    pdf_reader = PdfReader(temp_file_path)

            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            knowledge_base = FAISS.from_texts(chunks, embeddings)

            user_question = form.cleaned_data['question']
            if user_question:
                docs = knowledge_base.similarity_search(user_question)

                llm = OpenAI(api_key=openai_api_key)
                chain = load_qa_chain(llm, chain_type="stuff")
                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=user_question)
                    print(cb)

    else:
        form = PDFUploadForm()

    return render(request, 'pdfapp/ask_pdf.html', {'form': form, 'response': response, 'pdf_name': request.session.get('pdf_name')})
