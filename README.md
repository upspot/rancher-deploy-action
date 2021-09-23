# Action for Github to deploy image in Rancher using Rancher API

## Envs

### `RANCHER_ACCESS_KEY`

**Required** API Access key created in Rancher.

### `RANCHER_SECRET_KEY`

**Required** API Secret key created in Rancher.

### `RANCHER_URL_API`

**Required** API Url of your rancher project workload.

### `SERVICE_NAME`

**Required** NAME OF YOUR SERVICE ON RANCHER CLUSTER WHAT YOU WANT DEPLOY.

### `NAMESPACE`

**Required** NAME OF YOUR NAMESPACE ON RANCHER CLUSTER WHERE YOU WANT DEPLOY.

### `DOCKER_IMAGE`

**Required** URL TO YOUR DOCKER IMAGE (Ex: AWS or DOCKER REGISTRY).

##INFO:
If you deploy a image with "ghcr.io/organization/example/imageName:**latest**" only active deployments with latest will be updatet. 
If you deploy a image with "ghcr.io/organization/example/imageName:**x.x.x**" only active deployment with version number will be updated
## Example usage
`````
  
- name: Rancher Deploy
  uses: upspot/rancher-deploy-action@v0.0.4
  env:
    RANCHER_ACCESS_KEY: ${{ secrets.RANCHER_ACCESS_KEY }}
    RANCHER_SECRET_KEY: ${{ secrets.RANCHER_SECRET_KEY }}
    RANCHER_URL_API: 'https://rancher.YOUR-DOMAIN.COM/v3'
    SERVICE_NAME: 'myProject'
    NAMESPACE: 'test'
    DOCKER_IMAGE: 'ghcr.io/organization/example/imageName:latest'
