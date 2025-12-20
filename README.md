# Deploy personal apps to virtual (Hetzner) hosts

This repo has several apps configured with docker-compose for personal use. It relies on the following tools to manage deployment:

1. Docker compose + buildx
2. Tailscale
3. GitHub Actions

Additionally, zizmor is used to monitor the workflows for security.

## Updating an application version

For caddy and calibre, edit the version in `docker-bake.hcl`. For the other applications, edit the `versions.sh`. When the commit is pushed to `main`, GitHub Actions will automatically update the containers on the host.

## Setting up a new host

1. After creating the host, log in with `ssh` to the root account, update the operating system, restart and SSH back as the root:

   ```bash
   ssh root@<ip address>
   ```

1. Install Docker and Tailscale (the latter for SSH access after setup)
   1. <https://docs.docker.com/engine/install>
   1. <https://tailscale.com/kb/1031/install-linux>
1. Login with Tailscale: `tailscale up --ssh --advertise-exit-node`
1. Add the host IP address from the hosting company to Namecheap API access: <https://ap.www.namecheap.com/settings/tools/apiaccess/>
1. Configure Tailscale ACLs to allow access to the new node. Set the node to have the `login-node` tag, and make sure the ACLs are configured so `bweber` and `github-actions` can login, for example:

   ```json
		{
			"src":    ["autogroup:member"],
			"dst":    ["tag:login-host"],
			"users":  ["bweber"],
			"action": "accept",
		},
		{
			"src":    ["tag:github-actions"],
			"dst":    ["tag:login-host"],
			"users":  ["apps-deploy"],
			"action": "accept",
		},
    ```

1. Create a system user to run Docker compose and a regular user for SSH login:

   ```bash
   # The group number is for the docker group created by the Docker installer
   getent group
   useradd --create-home --system --gid 988 apps-deploy
   adduser bweber
   usermod -aG sudo bweber # For Ubuntu. I think the group is wheel on Fedora
   ```

1. Disable SSH for the root user. Make sure that the `bweber` user has `sudo` permissions

   ```bash
   echo "PermitRootLogin no" >> /etc/ssh/sshd_config
   systemctl ssh restart
   ```

1. Copy the Calibre library from the local machine to the remote, somehow, probably rsync
1. Create a Docker context on the local machine using the Tailscale SSH connection. This lets you run any Docker commands locally and they will be run on the remote host.

   ```bash
   docker context create hetzner-host --docker "host=ssh://apps-deploy@hetzner-host.<Magic DNS hostname>.ts.net"
   docker context use hetzner-host
   ```

1. Create the external volumes for the services

   ```bash
   docker volume create atuin_postgres \
   && docker volume create karakeep_meilisearch \
   && docker volume create karakeep_data \
   && docker volume create kosyncserver_data \
   && docker volume create forgejo_postgres \
   && docker volume create forgejo_data
   ```

1. Start the deployment from the local machine:

   ```bash
   source versions.sh
   export CADDY_CONFIG_ROOT=/tmp/caddy/conf
   export PUBLIC_CLIENT_IP=<Public IP address of the host>
   rsync -vzR ./caddy/conf/Caddyfile apps-deploy@hetzner-host<Magic DNS hostname>.ts.net:/tmp/
   op run --env-file=.env.tpl -- docker compose up --detach --wait --wait-timeout 30
   ```
 
1. Add the known host string for the remote host to a secret in the GitHub `deploy` environment in this repo. Add the Tailscale name of the host and the `apps-deploy` user to the GitHub variables for the environment. Add the public IP address of the host to a secret in the environment.

## Adding a new application

1. Create a new directory for the application and add a suitable `docker-compose.yml` file. Double check that the tag assigned for the Tailscale configuration is correct.
1. Add the application `docker-compose.yml` to the root `docker-compose.yml` file
1. Add the application version to the `versions.sh` file
1. Add a tag for the application to the Tailscale configuration, making sure the owners are `autogroup:owner` and `tag:apps-deploy`
1. If the new application needs a persistent volume, add it to the step above to create the volume, and then create the volume on the remote host using the Docker context.
1. Add the application to the Caddyfile
