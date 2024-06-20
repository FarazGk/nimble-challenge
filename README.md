# Nimble Challenge Submission

## Overview
This project is a submission for the Nimble Challenge, demonstrating a simple client-server application using Kubernetes, Docker, and Python's aiohttp and asyncio. The client and server communicate over a Kubernetes network, with the server set up to use aiortc for WebRTC communication.

## Project Structure
```
.
├── backend
│   ├── ball.py
│   ├── debugPrint.py
│   ├── Dockerfile.server
│   └── server.py
├── backend-deployment-and-service.yaml
├── frontend
│   ├── client.py
│   ├── debugPrint.py
│   ├── displayFrame.py
│   ├── Dockerfile.client
│   └── recognition.py
├── frontend-deployment-and-service.yaml
└── README.md
```

## Requirements
- Docker
- Minikube
- Kubernetes CLI (kubectl)
- Python 3.10+

## Setting Up the Environment

### 1. Building Docker Images
```sh
docker build -t frontend-image:latest -f ./frontend/Dockerfile.client .
docker build -t backend-image:latest -f ./backend/Dockerfile.server ./backend
```

### 2. Saving Docker Images
```sh
docker save -o frontend-image.tar frontend-image
docker save -o backend-image.tar backend-image
```

### 3. Loading Docker Images into Minikube
```sh
minikube image load frontend-image.tar
minikube image load backend-image.tar
```

### 4. Deploying to Kubernetes
```sh
kubectl apply -f backend-deployment-and-service.yaml
kubectl apply -f frontend-deployment-and-service.yaml
```

### 5. Managing Kubernetes Pods
```sh
kubectl get pods
kubectl logs <pod-name>
kubectl delete pod <pod-name>
kubectl logs <pod-name> --follow
```

## Minikube Commands
### Starting Minikube
```sh
minikube start
```

### Stopping Minikube
```sh
minikube stop
```

### Deleting Minikube
```sh
minikube delete
```

## Port Forwarding
To access the backend service locally:
```sh
kubectl port-forward service/backend-service 5001:5001
curl http://localhost:5001
```

## Docker Cleanup
### Removing Docker Build Cache and Resources
```sh
docker builder prune -a -f
docker container prune -f
docker volume prune -f
docker network prune -f
```


## Environment Variables
### Frontend Configuration
Set the backend URL and signaling:
```python
backend_url = os.getenv('BACKEND_URL', 'http://backend-service:5001')
signaling = TcpSocketSignaling("backend-service", 5001)
```

### Backend Configuration
Configure signaling and run the app:
```python
signaling = TcpSocketSignaling("0.0.0.0", 5001)
web.run_app(app, host='0.0.0.0', port=5001)
```

## Summary of Findings
- **Kubernetes**: Debugging Kubernetes took a significant amount of time due to limited experience and the need for a cloud-based environment.
- **aiortc**: Limited documentation on "aiortc built-in TcpSocketSignaling" posed challenges.
- **cv2 in Kubernetes**: Displaying with `cv2` was not feasible in a headless Kubernetes environment without a remote connection such as VNC.
- **Progress**: Successfully set up a simple "hello world" communication between client and server using `aiohttp` and `asyncio` on Kubernetes.
- **Related Work**: Found a related project that solves a similar challenge without implementing Kubernetes. The repository can be found [here](https://github.com/tempest2023/PythonCVDetection.git).

## Attachments
- `latest_attempt.tar`: Contains the latest attempt at the challenge.
- `hello_world.tar`: Contains a simple "hello world" client-server program.

Thank you for the opportunity to participate in this challenge. Please feel free to reach out with any questions or feedback.