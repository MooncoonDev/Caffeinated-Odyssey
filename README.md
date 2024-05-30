## The Caffeinated Odyssey

### Setup Instructions
1. Clone the repository from GitHub
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

The client FastAPI server will run on port 8000, and the worker FastAPI server will run on port 8001.

### Deployment
The provided Dockerfile can be used to build and run the application in a Docker container.

To protect against DoS attacks like the "delusional DDoSer", consider using a tool like nginx to throttle or block excessive requests from a single IP address.