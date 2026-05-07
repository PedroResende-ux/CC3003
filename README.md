# CC3003 - Surveillance of Rectangular Partitions (Vigilância de Partições Retangulares)

## Course
Métodos de Apoio à Decisão (Decision Support Methods) - FCUP 2025/2026

## Project Overview
This project addresses the problem of guarding rectangular partitions. Given a partition Π, we need to determine optimal guard placements that can cover all rectangles (or a subset Π' ⊂ Π).

## Project Tasks

### 1. Greedy Strategies
- Evaluate greedy algorithms for guard placement
- Ensure coverage of required rectangles

### 2. Integer Programming & Constraint Programming
- Define mathematical model of the problem
- Implement constraint propagation using MAC (Maintaining Arc-Consistency) with AC-3
- Solve using:
  - SWI Prolog (with clpfd library)
  - Google OR-Tools

### 3. Dynamic Programming
- Evaluate dynamic programming approaches for the problem

### 4. Problem Extensions
- **Colored Guards**: Guards must have distinct colors if they can see the same rectangle. Find minimum guards and minimum colors needed.
- **Extended Reach Guards**: Allow guards at vertices to cover not only incident rectangles but also neighbors within distance D in the graph.

## Deliverables
- Implementation code
- PDF report with:
  - Method descriptions
  - Experimental results
  - Implementation details
- Oral presentation

## Deadline
29 May 2026

## Group
2-3 members

## Files
- `partsRects.py` - Python implementation
- `PartsRectangulares/` - C implementation with headers and examples
- `MAD2526_trab.pdf` - Full project specification