# 🤖 RAG with Mistral - Local LLM Question Answering System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)

A powerful Retrieval-Augmented Generation (RAG) system built with Mistral LLM, offering local document processing and intelligent question answering capabilities.

## 📑 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Learning Resources](#-learning-resources)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [Contact](#-contact)
- [License](#-license)

## ✨ Features

- 📚 Local document processing (PDF, TXT, DOCX)
- 🔍 Intelligent text chunking and embedding
- 💡 Context-aware question answering
- 🎯 Customizable response parameters
- 🖥️ User-friendly Streamlit interface

## 🔧 Prerequisites

- Python 3.8 or higher
- Git
- [Ollama](https://ollama.ai/) with Mistral model installed

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/cloaky233/RAG_Opensrc.git
cd RAG_Opensrc
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Mistral model in Ollama:
```bash
ollama pull mistral
```

## 🚀 Usage

1. Start the Streamlit application:
```bash
streamlit run stmain.py
```

2. Access the web interface at `http://localhost:8501`

3. Upload documents and start asking questions!

### Basic Workflow:
1. Navigate to the "Documents" tab
2. Upload your documents
3. Process the documents
4. Switch to the "Chat" tab
5. Start asking questions about your documents

## 📁 Project Structure

```
RAG_Opensrc/
    ├── pysrc/
    │   ├── document_processor.py
    │   ├── embeddings_manager.py
    │   └── rag_engine.py
    ├── stmain.py
    ├── Info.md
    ├── LearnWithPrompts.md
    ├── requirements.txt
    └── README.md
```

## 📚 Documentation

For detailed information about the project architecture and implementation details, please refer to:
- [Info.md](Info.md) - Technical documentation and system architecture
- [LearnWithPrompts.md](LearnWithPrompts.md) - Interactive learning guide with examples

## 📖 Learning Resources

New to RAG systems? Check out our learning resources:
1. Review [LearnWithPrompts.md](LearnWithPrompts.md) for step-by-step tutorials
2. Explore the [Info.md](Info.md) for technical insights
3. Try the example prompts provided in the documentation

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## ❗ Troubleshooting

Common issues and solutions:

1. **Ollama Connection Error**
   - Ensure Ollama is running locally
   - Verify Mistral model is installed

2. **Document Processing Issues**
   - Check file formats (PDF, TXT, DOCX only)
   - Ensure files are not corrupted

For more issues, please check our [Issues](https://github.com/cloaky233/RAG_Opensrc/issues) page.

## 📫 Contact



Project Link: [https://github.com/cloaky233/RAG_Opensrc](https://github.com/cloaky233/RAG_Opensrc)

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

⭐ Star this repo if you find it helpful!
