# Deploy Apps on Tailnet with Ansible

Generate secrets locally:

```bash
task generate-secrets
```

Deploy the app for updates:

```bash
uv run ansible-playbook playbook.yaml --tags karakeep
```

## Update ansible dependencies

```bash
uv run ansible-galaxy install -r requirements.yml --force
```

## Rebuilding Caddy

As of 26-APR-2025, the `caddy-dns/namecheap` extension does not support Caddy >=2.10 due to a change in the libdns used by Caddy. This is causing the ansible playbook to fail. To rebuild Caddy on the server:

```bash
ssh root@karakeep.forest-catfish.ts.net
```

Then on the remote:

```bash
cd /caddy
xcaddy --with "github.com/caddy-dns/namecheap" v2.9.1
mv ./caddy /usr/local/bin/caddy
systemctl restart caddy.service
```

If the machine has rebooted, the UDP memory size needs to be configured according to the [quic-go wiki](https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes):

```bash
sysctl -w net.core.rmem_max=7500000
sysctl -w net.core.wmem_max=7500000
```

Then reset and restart the Caddy service:

```bash
systemctl reset-failed caddy.service
systemctl restart caddy.service
```

[This post](https://code.google.com/archive/p/u1o9/wikis/Tuning.wiki) says to edit `/etc/sysctl.conf` to include these values so they survive reboot, but I didn't try that yet. [This page](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10-beta/html/network_troubleshooting_and_performance_tuning/tuning-udp-connections#increasing-the-system-wide-udp-socket-buffers) in the Red Hat docs suggests something similar. In a file called `/etc/sysctl.d/10-udp-socket-buffers.conf`, set

```
net.core.rmem_max=7500000
net.core.wmem_max=7500000
```

Then run `sysctl -p /etc/sysctl.d/10-udp-socket-buffers.conf`.
