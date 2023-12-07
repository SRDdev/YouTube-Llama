# 🦙 YouTube Llama

![llama_image](https://github.com/SRDdev/YouTube-Llama/assets/84516626/2e5e3c73-6224-492f-8884-a1df9601ec5c)


A question-answering chatbot for any YouTube video using Local Llama2 & Retrival Augmented 
Generation

https://github.com/SRDdev/YouTube-Llama/assets/84516626/aa463492-c3c5-4b32-90ec-5e9ea48cc3eb


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)
- [Llama 2 RAG](#llama-2-rag)

## Features

- Learns information from YouTube videos.
- Provides a natural language interface for asking questions about video content.
- Utilizes Local Llama2 for efficient question-answering capabilities.

## Installation

Follow these steps to set up the project:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SRDdev/YouTube-Llama.git
    cd YouTube-Llama
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. Installing `Llama-cpp-Python`

The installation process for llama-cpp-python is a bit complex. But I have combined all the required information below.

a. **Requirements**
    - git
    - python
    - cmake
    - Visual Studio Community (make sure you install this with the following settings)
        a. Desktop development with C++
        b. Python development
        c. Linux embedded development with C++

4. **Install Llama-cpp-Python:**

   Follow the installation process for Llama-cpp-Python:

    ```bash
    # Clone git repository recursively to get llama.cpp submodule as well
    git clone --recursive -j8 https://github.com/abetlen/llama-cpp-python.git
    ```

    Open up the command prompt (or Anaconda prompt if you have it installed), set up environment variables to install. Follow this if you do not have a GPU; you must set both of the following variables.

    You can ignore the second environment variable if you have an `NVIDIA GPU`.

    ```bash
    set FORCE_CMAKE=1
    set CMAKE_ARGS=-DLLAMA_CUBLAS=OFF
    ```

    ```bash
    pip install llama-cpp-python -q
    ```

## Usage

How to use 🦙 YouTube Llama:

1. **Run the application:**

    ```bash
    streamlit run app.py
    ```

2. Access the chatbot through a web interface or API endpoint.

3. Input questions related to a specific YouTube video

4. Receive answers based on the content of the video as well as general purpose information.

## Contributing

We welcome contributions! Follow these steps to contribute to the project:

1. **Fork the project.**

2. **Create a new branch (`git checkout -b feature/awesome-feature`).**

3. **Commit your changes (`git commit -am 'Add awesome feature'`).**

4. **Push to the branch (`git push origin feature/awesome-feature`).**

5. **Open a pull request.**

Refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license.) - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

We would like to express our gratitude to the creators of Local Llama2 for providing a powerful tool for question-answering tasks.


