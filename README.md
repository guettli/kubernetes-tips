# Kubernetes Tips

Use the nice starship command line prompt, which supports Kubernetes: https://starship.rs/config/#kubernetes
This needs te be activated in ~/.config/starship.toml.

## kubectl

### Create a simple service

```
k create deployment mynginx --image=nginx 

k expose deployment mynginx --port 8080 --target-port 80


k port-forward services/mynginx 8080

# keep above command running and open a second shell

open http://localhost:8080
```


### Get external IP of a control plane

```
kubectl get nodes -o jsonpath="{.items[*].status.addresses[?(@.type=='ExternalIP')].address}" -l node-role.kubernetes.io/control-plane |  cut -d' ' -f1
```

## Not solved yet

### How to get all pods of a deployment.

https://stackoverflow.com/questions/52957227/kubectl-command-to-list-pods-of-a-deployment-in-kubernetes

Ugly shell scripts.
