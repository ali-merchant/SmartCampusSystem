CAMPUS_GRAPH = {
    "Hostel": {"Cafeteria": 2, "Library": 3},
    "Cafeteria": {"Hostel": 2, "Science_Block": 2, "Auditorium": 3},
    "Science_Block": {"Cafeteria": 2, "AI_Lab": 2, "Library": 3},
    "AI_Lab": {"Science_Block": 2},
    "Library": {"Hostel": 3, "Science_Block": 3},
    "Auditorium": {"Cafeteria": 3},
}

COORDS = {
    "Hostel": (0, 0),
    "Cafeteria": (2, 0),
    "Science_Block": (4, 0),
    "AI_Lab": (6, 0),
    "Library": (0, 3),
    "Auditorium": (2, 3),
}

KNOWN_LOCATIONS = set(CAMPUS_GRAPH.keys())

GRAPH_TYPE = "weighted"
HEURISTIC_AVAILABLE = True
