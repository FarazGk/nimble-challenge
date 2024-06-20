# minikube
minikube stop
minikube delete
minikube start

# port forward:
kubectl port-forward service/backend-service 5001:5001

curl http://localhost:5000/hello

# docker build
docker build -t frontend-image:latest -f ./frontend/Dockerfile.client .
docker build -t backend-image:latest -f ./backend/Dockerfile.server ./backend

# docker remove
docker builder prune -a -f
docker container prune -f
docker volume prune -f
docker network prune -f

# Save/Load the image from docker to kubernetes
docker save -o frontend-image.tar frontend-image
docker save -o backend-image.tar backend-image

minikube image load frontend-image.tar
minikube image load backend-image.tar

# pods:
kubectl get pods
kubectl logs <pod name>
kubectl delete pod <pod name>

kubectl apply -f backend-deployment-and-service.yaml
kubectl apply -f frontend-deployment-and-service.yaml
