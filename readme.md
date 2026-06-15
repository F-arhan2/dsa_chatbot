# DSA Voice Chatbot

A Python-based Data Structures and Algorithms (DSA) chatbot that answers questions about sorting algorithms, arrays, linked lists, and other DSA concepts using a custom JSON dataset. The chatbot also supports voice output through Text-to-Speech (TTS).

## Features

* Interactive command-line chatbot
* Text-to-Speech responses using `pyttsx3`
* JSON-based knowledge dataset
* Intent detection using keyword matching
* Support for multiple DSA topics
* Randomized responses for natural conversations
* Greeting system with multiple response variations
* YOU can open any  website just by telling 'open "website_name"'

## Topics Covered

### Sorting Algorithms

* Sorting Basics
* Bubble Sort
* Selection Sort
* Insertion Sort
* Merge Sort
* Quick Sort

### Arrays

* Definition
* Facts
* Applications
* Examples

### Linked Lists

* Definition
* Facts
* Applications
* Advantages
* Disadvantages
* Types of Linked Lists

#### Linked List Types

* Singly Linked List
* Doubly Linked List
* Circular Linked List
* Circular Doubly Linked List

### Operations

* Insertion
* Deletion
* Traversal
* Searching

### Greetings

* Hello
* Good Morning
* Good Afternoon
* Good Evening

## Technologies Used

* Python 3
* JSON
* pyttsx3

## Project Structure

```text
DSA-Chatbot/
│
├── main.py
├── datasets/
│   └── dsa_data.json
│
├── README.md
└── requirements.txt
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/F-arhan2/dsa-chatbot.git
cd dsa-chatbot
```

### Install Dependencies

```bash
pip install pyttsx3
```

## Running the Bot

```bash
python main.py
```

Example:

```text
You: What is sorting?

Bot: Sorting is the process of arranging data in a specific order such as ascending or descending.
```

## Example Questions

### Sorting

```text
What is sorting?
Explain sorting
Types of sorting
```

### Bubble Sort

```text
Explain bubble sort
Bubble sort time complexity
Show bubble sort code
```

### Arrays

```text
What is array?
Array facts
Array applications
Array examples
```

### Linked Lists

```text
What is linked list?
Linked list advantages
Linked list applications
Types of linked list
```

### Greetings

```text
Hi
Hello
Good morning
Good evening
```

## Future Improvements

* Speech Recognition
* NLP-based Intent Detection
* Stack and Queue Support
* Trees and Graphs Support
* Machine Learning-based Chatbot
* Flask/FastAPI Web Version
* Chat History and Memory
