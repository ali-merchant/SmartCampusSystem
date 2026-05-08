# SmartCampusSystem

Structured, CLI-driven smart campus request system that routes each request through the
correct pipeline (ANN, Logic/KB, CSP, Search) and returns a standardized response.

## Features
- Strict, structured CLI input (no free-form paragraph input).
- Standard request and response object formats.
- Router-driven pipelines based on request type.
- Modular ANN, Logic/KB, CSP, and Search components.
- Validation, normalization, and exception handling to prevent crashes.

## Project Structure
- main.py: Entry point and console output.
- cli.py: Structured CLI input collection and strict validation.
- preprocessing.py: Normalization and validation; prepares module inputs.
- router.py: Determines which modules run for each request type.
- pipeline.py: Orchestrates module execution and builds final response.
- response_generator.py: Merges module outputs into the standard response.
- campus_map.py: Campus graph, coordinates, and graph policy.
- models/: Request and response templates and validation.
- modules/: ANN, Logic/KB, CSP, and Search modules.

## How To Run
From the SmartCampusSystem folder:

python main.py

## Supported Request Types
1. Navigation_Only
	- Modules: Search
2. Eligibility_Check
	- Modules: Logic/KB
3. Booking_or_Scheduling
	- Modules: Logic/KB -> CSP -> optional Search
4. Urgent_Service_Request
	- Modules: ANN -> Logic/KB -> CSP -> optional Search
5. Full_Service_Request
	- Modules: ANN -> Logic/KB -> CSP -> Search

## Input Rules (Strict)
- Category must be one of:
  AI_Lab_Support, Viva_Scheduling, Access_Request, Maintenance, Emergency_Help
- Locations must match known campus nodes from campus_map.py.
- Severity, time sensitivity, and crowd level must be 1-10.
- Preferred slot must be 1-4.

## Output Format
The final response always follows the standard schema:

{
  "request_id": "REQ101",
  "decision": "",
  "priority": {},
  "eligibility": {},
  "assignment": {},
  "route": {},
  "message": ""
}

## Notes
- The ANN module currently uses a simple scoring heuristic and can be replaced
  with a trained Perceptron/MLP model.
- The Search module follows the operational policy: BFS for unweighted graphs,
  A* for weighted graphs (UCS fallback).