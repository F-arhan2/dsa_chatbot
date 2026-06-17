# DSA Desktop Workspace & Voice Chatbot

A professional Python-based Data Structures and Algorithms (DSA) desktop management workspace and interactive chatbot. It answers technical queries regarding sorting algorithms, arrays, linked lists, and tree structures using an indexed, multi-tier JSON knowledge dataset. 

The application features a sleek, human-centric engineering GUI, real-time audio input capture via Automatic Speech Recognition (ASR), and natural verbal playback using Text-to-Speech (TTS).

## Features

* **Engineering Workspace UI:** Built with a clean, professional CustomTkinter dashboard layout using a dark matte slate and solarized amber color scheme—completely moving away from generic, loud AI design tropes.
* **Dual-Input Modality:** * Traditional command line execution via a keyboard input field.
    * Hands-free operation utilizing a calibrated Microphone input button running Speech Recognition algorithms.
* **Full Text-to-Speech (TTS) Engine:** Verbalizes responses dynamically using `pyttsx3` with adjustable performance controls and hot-swappable Male/Female voice profile configurations.
* **Hierarchical Knowledge Database:** High-speed token lookup mapping inputs into highly structured algorithmic data blocks stored in a customized local JSON dataset.
* **Index Macro Monitor:** A dedicated right-hand side panel containing instant click-to-trigger macro shortcut cards to easily extract complex formatting like code execution samples, time complexities, or interview questions.
* **System Commands Integration:** Native OS/Browser pipeline execution to dynamically launch any website by providing the parameter `open "website_name"`.

## Topics Covered

### Data Structures & Linear Formations
* **Arrays:** Structural Definitions, Dynamic Facts, Memory Allocations, Application Scenarios, Multi-Dimensional Matrix Examples (2D Arrays).
* **Linked Lists:** Memory Nodes, Linear Operations, Structural Disadvantages/Advantages.
    * *Types Supported:* Singly Linked, Doubly Linked, Circular, and Circular Doubly Linked Lists.
* **Stacks & Queues:** Execution profiles mapped through arrays or linked nodes including Simple Queues, Circular Queues, Priority Queues, and Double-Ended Queues (Deques).
* **Trees:** Non-linear structural analysis covering Binary Trees, Binary Search Trees (BST), and Min/Max Heap allocations.

### Sorting & Searching Algorithms
* **Searching:** Sequential Analysis (Linear Search) and Logarithmic Interval Matching (Binary Search).
* **Sorting Mechanics:** Execution, time/space complexity matrix tracking, and Java source representations for:
    * Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort.

### Common Operations
* Algorithmic steps for Data Structure **Traversal**, **Insertion**, **Deletion**, and **Searching**.

---

## Technologies Used

* **Python 3.x** - Core Platform Runtime
* **CustomTkinter** - Modernized Flat-UI Graphical Engine wrapper for Tkinter
* **SpeechRecognition** - Engine wrapper utilized for processing Google Web Speech API microphone arrays
* **PyAudio** - Mandatory low-level I/O binding audio library for Microphone captures
* **pyttsx3** - Offline Native Multi-Platform Text-to-Speech synthesis Engine
* **JSON** - Data storage blueprint format used for structural knowledge mapping

---

## Project Structure

```text
DSA-Chatbot/
│
├── dsabot.py                 # Core Graphical Workspace and Application Entrypoint
├── datasets/
│   └── dsa_data.json         # Structured Multi-Tier Knowledge Base JSON Dataset
│
├── README.md                 # System Documentation 