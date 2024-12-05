# DNS

## Table of Contents

- [DNS](#dns)
  - [Table of Contents](#table-of-contents)
  - [Flush DNS Cache](#flush-dns-cache)
  - [systemctl](#systemctl)
  - [dig](#dig)
  - [nslookup](#nslookup)

## Flush DNS Cache

- Clear the DNS cache to ensure that the system resolves domain names with the most up-to-date information.

```bash
resolvectl flush-caches
systemd-resolve --flush-caches
```

- Use `resolvectl` for newer systems or `systemd-resolve` for older systems (pre-2020).

## systemctl

- This command enables the `systemd-resolved` service if it is not already running, ensuring DNS resolution through `systemd`.

```bash
systemctl enable systemd-resolved.service
```

**Explanation of the command:**

- `systemd-resolve --flush-caches`: This command clears the DNS cache maintained by `systemd-resolved`, which can help resolve issues with outdated or incorrect DNS entries.
- After flushing the cache, it may be necessary to restart the `systemd-resolved` service to ensure proper operation.

```bash
systemctl restart systemd-resolved
service systemd-resolved restart
```

- To restart the service, use `systemctl restart systemd-resolved` (preferred). The `service` command is available but is considered legacy.

## dig

```bash
dig domain.com
dig +short NS domain.com
```

## nslookup

- `nslookup` is a legacy tool but still useful for querying DNS. You can also specify custom DNS servers, such as `1.1.1.1` (Cloudflare) or `8.8.8.8` (Google), to query DNS directly without using the system’s default resolver.

```bash
nslookup domain.com
nslookup -q=cname domain.com
nslookup -q=cname domain.com 1.1.1.1
nslookup -q=cname domain.com 8.8.8.8
```

```bash
nslookup -q=mx domain.com
nslookup -q=txt domain.com
```
