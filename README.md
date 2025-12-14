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
1. Add the host IP address from Hetzner to Namecheap API access: <https://ap.www.namecheap.com/settings/tools/apiaccess/>
1. Configure Tailscale ACLs to allow access to the new node. Set the node to have the `login-node` tag, and make sure the ACLs are configred so `bweber` and `github-actions` can login, for example:

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

1. Update the sudoers file so apps-deploy can start/restart the systemctl service. Run `visudo` and add:

   ```
   Cmnd_Alias APPS_DEPLOY_CMD = /usr/bin/systemctl start apps-deploy.service, /usr/bin/systemctl restart apps-deploy.service, /usr/bin/systemctl stop apps-deploy.service
   apps-deploy ALL=(ALL) NOPASSWD: APPS_DEPLOY_CMD
   ```

1. Clone the repo as the `apps-deploy` user:

   ```bash
   su - apps-deploy
   git clone https://github.com/bryanwweber/apps-deploy
   ```

1. Copy the Calibre library from the laptop to the remote, somehow, probably rsync
1. Set up credentials for the applications. These need to go in `.env` files in each of the sub-folders of the repo
   1. Atuin

      ```shell
      ATUIN_DB_NAME=atuin
      ATUIN_DB_USERNAME=atuin
      # Choose your own secure password. Stick to [A-Za-z0-9.~_-]
      ATUIN_DB_PASSWORD=
      TS_AUTHKEY=
      ```

   1. Caddy

      ```shell
      PUBLIC_CLIENT_IP=

      NAMECHEAP_API_KEY=
      NAMECHEAP_API_USER=
      TS_AUTHKEY=
      ```

   1. Calibre

      ```shell
      CALIBRE_LIBRARY="/root/Calibre Library"
      TS_AUTHKEY=
      ```

   1. Karakeep

      ```shell
      NEXTAUTH_URL="http://localhost:3000"

      DISABLE_SIGNUPS=true
      CRAWLER_FULL_PAGE_ARCHIVE=true

      NEXTAUTH_SECRET=
      MEILI_MASTER_KEY=
      OPENAI_API_KEY=
      TS_AUTHKEY=
      ```

   1. kosyncserver

       ```shell
       TS_AUTHKEY=
       ```

1. Create the external volumes for the services as root

   ```bash
   docker volume create atuin_postgres \
   && docker volume create karakeep_meilisearch \
   && docker volume create karakeep_data \
   && docker volume create kosyncserver_data
   ```

1. Create the `systemd` service with the script in the repo. This needs to run as root, not the `apps-deploy` user. This will also start the services, so monitor for startup.

   ```bash
   cd /home/apps-deploy/apps-deploy
   ./compose-service.sh
   systemctl status apps-deploy
   ```

1. Disable SSH for the root user. Make sure that the `bweber` user has `sudo` permissions

   ```bash
   echo "PermitRootLogin no" >> /etc/ssh/sshd_config
   systemctl ssh restart
   ```
