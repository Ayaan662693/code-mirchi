# Production Deployment, Custom Domain & DNS Setup Guide

This comprehensive guide walks you through connecting a custom domain, configuring DNS records, enforcing SSL/HTTPS certificates, verifying SEO indexing, and scheduling automated database backups for **CODE MIRCHI**.

---

## 1. Custom Domain & DNS Configuration

Deploying to generic subdomains (e.g. `your-app.lovable.app` or `your-app.onrender.com`) harms search rankings and brand credibility. Here is how to configure a custom domain (e.g. `codemirchi.dev` or `yourdomain.com`).

### Step 1: Purchase Your Domain
- Recommended: **Cloudflare Registrar** (at-cost pricing with no markups) or Namecheap / GoDaddy.

### Step 2: Use Cloudflare for DNS Management
Using Cloudflare provides free enterprise-grade DNS, DDoS protection, edge caching, and automated SSL:
1. Add your domain to Cloudflare.
2. Update your domain registrar's nameservers to the two Cloudflare nameservers provided (e.g., `aria.ns.cloudflare.com` and `noah.ns.cloudflare.com`).

### Step 3: Add Production DNS Records
In your Cloudflare DNS dashboard, add the following standard records pointing to your hosting server (VPS, Render, Railway, or Fly.io):

| Type | Name | Content / Target | Proxy Status | TTL |
| :--- | :--- | :--- | :--- | :--- |
| `A` | `@` | `<YOUR_SERVER_IPV4>` | Proxied (Orange Cloud) | Auto |
| `AAAA` | `@` | `<YOUR_SERVER_IPV6>` (if available) | Proxied (Orange Cloud) | Auto |
| `CNAME` | `www` | `@` | Proxied (Orange Cloud) | Auto |

> [!TIP]
> Always enable Cloudflare Proxy (`Proxied` status) to activate free DDoS mitigation, HTTP/3, and automatic TLS edge termination.

---

## 2. HTTPS & SSL Enforcement

Unencrypted HTTP connections trigger browser warnings ("Not Secure") and hurt search rankings. CODE MIRCHI implements multi-layered HTTPS enforcement:

### 1. Reverse Proxy / Cloudflare Layer
In Cloudflare:
- Go to **SSL/TLS -> Overview** -> Set encryption mode to **Full (Strict)**.
- Go to **SSL/TLS -> Edge Certificates** -> Turn ON **Always Use HTTPS**.
- Enable **Automatic HTTPS Rewrites** to upgrade insecure asset references.

### 2. Application Layer Redirection (`app.py`)
In `app.py`, CODE MIRCHI automatically inspects the `X-Forwarded-Proto` header sent by reverse proxies and redirects unencrypted HTTP traffic to HTTPS with a `301 Moved Permanently` status code.

### 3. Strict-Transport-Security (HSTS)
To guarantee browsers only ever contact the domain via HTTPS, the following security response headers are returned on all production responses:
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 3. SEO & Indexing Verification

CODE MIRCHI includes pre-configured SEO metadata and structured schemas:

### Metadata Checklist Included:
- [x] Primary `<title>`: `CODE MIRCHI | 4-Year Engineering Roadmaps, Semesters & Hackathons`
- [x] Canonical URL tag: `<link rel="canonical" href="https://codemirchi.dev/" />`
- [x] Open Graph (Facebook, LinkedIn, Discord previews): `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name`
- [x] Twitter Card (X previews): `twitter:card`, `twitter:title`, `twitter:description`
- [x] JSON-LD Structured Data Schema (`schema.org`):
  - `WebSite` schema with internal search action
  - `EducationalOrganization`
  - `EducationalOccupationalProgram` (representing 4-year / 8-semester curricula)
  - `ItemList` (for live hackathons)
- [x] Search crawler directives: `/robots.txt`
- [x] Search index catalog: `/sitemap.xml`

### How to Verify:
1. **Google Search Console**:
   - Add your custom domain property via DNS verification (TXT record in Cloudflare).
   - Go to **Sitemaps** and submit: `https://yourdomain.com/sitemap.xml`.
2. **Rich Results Test**:
   - Visit [Google Rich Results Test](https://search.google.com/test/rich-results) and enter your URL to verify structured schemas.
3. **Social Share Previews**:
   - Test preview cards on [OpenGraph.xyz](https://www.opengraph.xyz/) or [Twitter Card Validator](https://cards-dev.twitter.com/validator).

---

## 4. Automated Database Backups & Disaster Recovery

Launchpad India stores student roadmap progress, degree selections, and hackathons in `launchpad.db`. To prevent data loss:

### 1. Online Non-Blocking Backups (`backup.py`)
Uses the official SQLite Online Backup API (`sqlite3.Connection.backup()`), which creates an atomic, consistent copy of the database without locking the tables or interrupting active users.

### 2. Running Manual & Automated Backups:
- **Command-line backup**:
  ```bash
  ./venv/bin/python3 backup.py --backup
  ```
- **List all saved backups**:
  ```bash
  ./venv/bin/python3 backup.py --list
  ```
- **Restore from a snapshot**:
  ```bash
  ./venv/bin/python3 backup.py --restore backups/launchpad_backup_YYYYMMDD_HHMMSS.db
  ```
- **On-demand via API**:
  ```bash
  curl -X POST http://localhost:5050/api/admin/backup
  ```

### 3. Automated Backup Rotation
The system retains the latest **10 snapshots** in `backups/` and automatically purges older snapshots to optimize disk space.

### 4. Offsite Cloud Backup (Recommended for Production)
For complete peace of mind, sync the `backups/` folder to an S3 or Cloudflare R2 bucket daily using rclone or a simple cron job:
```bash
# Example cron job running daily at 3 AM:
0 3 * * * rclone sync /path/to/backups remote-s3:my-launchpad-backups
```
