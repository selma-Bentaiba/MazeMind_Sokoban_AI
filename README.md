# **🧩 Sokoban Solver AI**  
### **Master 1 - Visual Computing, USTHB (2024/2025)**  

**Course:** Problem Solving - TP by *Dr. SEBAI Meriem*  
<br>  

📄 **[Project Support (PDF)](./📄_sokoban_project.pdf)**  
<br>  

![Sokoban Game Example](https://upload.wikimedia.org/wikipedia/commons/4/4b/Sokoban_ani.gif)  
<br>  

---

## **📌 About**  
Sokoban is a classic puzzle game where the player pushes boxes onto target locations. This project models Sokoban as a search problem and implements **BFS** and **A\*** algorithms to solve it. The goal is to find **efficient solutions** and visualize them using **Pygame**.  

---

## **✨ Features**  
- ✅ **AI Solver**: Uses **Breadth-First Search (BFS)** and **A\*** with heuristics.  
- ✅ **Custom Heuristics**: Implements Manhattan Distance-based heuristics.  
- ✅ **Deadlock Detection**: Prevents impossible moves.  
- ✅ **Graphical Interface**: Visualize solutions using **Pygame**.  

---

## **⚙️ How It Works**  
### **1. Modeling the Sokoban Game**  
- The game is represented as a **grid** with walls, targets, boxes, and the player.  
- The game state is stored as a **class** with movement logic.  

### **2. AI Search Algorithms**  
- **BFS**: Explores paths level by level.  
- **A\***: Uses heuristics to find optimal paths.  

### **3. Graphical Simulation**  
- Uses **Pygame** to **animate** the solution.  

---

## **📦 Installation**  
1️⃣ Clone the repository:  
```bash  
git clone https://github.com/selma-Bentaiba/MazeMind_Sokoban_AI.git  
```  

2️⃣ Install dependencies:  
```bash  
pip install pygame  
```  

3️⃣ Run the solver:  
```bash  
python main.py  
```  

---

## **📊 AI Algorithms for Sokoban**  
This project implements **AI search algorithms** to solve the **Sokoban puzzle**, focusing on **Breadth-First Search (BFS)** and **A\***.  

### **1️⃣ Breadth-First Search (BFS)**  
BFS is a **uniform-cost search** that explores all possible moves **level by level**, ensuring the **shortest path** is found. However, it has high memory usage because it stores all visited states.  

**Steps of BFS in Sokoban:**  
1. Start from the initial state.  
2. Expand all possible next moves and store them in a queue.  
3. Check for deadlocks before proceeding.  
4. Continue exploring until a solution is found or all states are exhausted.  

---

### **2️⃣ A\* Algorithm (A-star)**  
A\* is an **informed search algorithm** that finds the optimal path efficiently by combining:  
- **G(n):** Cost from the start to the current state.  
- **H(n):** Estimated cost from the current state to the goal.  

\[
F(n) = G(n) + H(n)
\]  

It uses **heuristics** to improve performance:  

#### **Heuristic Functions in Sokoban**  
- **h1(n) - Misplaced Boxes Heuristic:**  
  - Counts the number of boxes not on target positions.  
  - Faster but less accurate.  

- **h2(n) - Manhattan Distance Heuristic:**  
  - Measures the total Manhattan distance from each box to its nearest target.  
  - More precise but computationally expensive.  

- **h3(n) - Combined Heuristic:**  
  - Uses `h2(n)` plus the player's distance to the nearest box to ensure efficiency.  
  - Provides a balance between speed and accuracy.  

---

## **📜 Code Overview**  
### **🔹 `main.py`**  
- Runs the Sokoban solver.  
- Allows users to choose an algorithm (BFS or A\*).  
- Displays the solution and execution time.  

### **🔹 `Search.py`**  
- Implements BFS and A\* search algorithms.  
- Handles heuristic calculations.  
- Checks for deadlocks before expanding states.  

### **🔹 `Node.py`**  
- Represents a single Sokoban state in the search tree.  
- Stores parent nodes for reconstructing the solution path.  

### **🔹 `State.py`**  
- Defines the Sokoban grid and movement rules.  
- Manages player movement and box pushing.  
- Checks if the goal state is reached.  

---

## **🤖 Future Improvements**  
- 🔹 **Better GUI**: Enhance the graphical user interface for a more intuitive experience.  
- 🔹 **Deep Learning**: Implement deep learning techniques for smarter heuristics.  
- 🔹 **More Levels**: Add additional Sokoban levels for extended gameplay.  
- 🔹 **Performance Optimization**: Improve the efficiency of the algorithms for faster solutions.  

---
