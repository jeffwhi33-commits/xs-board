# DNS for xstips.com

At your registrar (Cloudflare / Namecheap), set:

## Apex `xstips.com` — A records
Host `@` → `185.199.108.153`
Host `@` → `185.199.109.153`
Host `@` → `185.199.110.153`
Host `@` → `185.199.111.153`

## Optional www
CNAME `www` → `jeffwhi33-commits.github.io`

Then wait for DNS (often 5–30 min). GitHub will issue HTTPS automatically.
