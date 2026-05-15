# Secrets Policy

The two-layer architecture for storing credentials in an ØØT organisation. Software credentials in Bitwarden (or 1Password). Crypto signing keys in Trezor (or Ledger). Org-level admin in Yubikey-protected accounts. No credentials in plaintext anywhere — not in `.env` files, not in `claude_desktop_config.json`, not in shell history.

This document is normative for both Cloud and Privacy tracks. The privacy track adds 4thtech wallet keys to the Trezor layer; otherwise the architecture is identical.

---

## Why two layers

The two layers solve different problems:

- **Software credentials** (API keys, OAuth tokens, recovery codes, SaaS passwords): need to be sharable across devices, sharable across partners with appropriate scoping, rotatable, recoverable. A hardware wallet cannot store these — it is designed for cryptographic signing operations, not arbitrary string storage.
- **Crypto signing keys** (treasury wallet, payroll wallet — Gen 2, 4thtech identity wallets): must never leave the device they were generated on. Software password managers can store seed phrases but doing so defeats the purpose of self-custody. Hardware wallets sign on-device without ever exposing the private key.

A single tool cannot do both well. The framework specifies both.

---

## Layer 1 — Bitwarden (software credentials)

### Why Bitwarden as the default recommendation

Open source. Self-hostable for orgs that want full sovereignty (Vaultwarden is the lightweight server). Supports organisation accounts with shared vaults, role-based access, and per-vault permissions. Strong client encryption. End-to-end encrypted at rest.

### Alternative: 1Password

Commercial. Polished. Excellent UX. Supports the same organisational features. Reasonable choice for orgs that prefer a commercial vendor with a support contract. The framework treats Bitwarden and 1Password as functionally equivalent for ØØT purposes; pick based on your team's preference.

### What goes in Bitwarden

- API keys (Anthropic, OpenAI, Google, GitHub, Stripe, Slack, etc.).
- OAuth tokens and refresh tokens.
- SaaS account passwords.
- Recovery codes for 2FA-protected accounts.
- SSH private keys (encrypted in Bitwarden Secure Notes or via Bitwarden SSH agent).
- TOTP secrets where the partner cannot use a hardware key.
- Database passwords, internal service credentials.
- **Curator Shared Brain `admin_token`** — 32+ random characters; gates the `POST /api/sharedbrain/:id/revoke` endpoint that performs GDPR Article 17 erasure on the Firm Brain. **Founders collection only.** Rotate on suspected compromise.
- **GitHub fine-grained PATs for the Firm Brain** (one per partner; Contents read/write on the `<firm>-brain` repo) — used by each partner's Curator instance to Push their opted-in domain. **Per-partner collection.** Revoke on contributor exit; the corresponding Firm Brain revoke endpoint (see [EU-AI-ACT.md](EU-AI-ACT.md) Article 17) removes their contributions.
- **GitHub fine-grained PATs for the Ledger** (one per Routine bot identity; Contents read/write on the `<firm>-ledger` repo, signed-commits enabled) — used by Routines per [ADR-001](../docs/internal/ADR-001-cloud-routine-excel-writeback.md). **Shared-services collection.**

### What does NOT go in Bitwarden

- Crypto wallet seed phrases (never).
- Crypto wallet private keys (never).
- The Trezor recovery seed (never).
- Any credential whose loss does not have a recovery path (use the appropriate hardware-backed mechanism instead).

### Vault structure

The framework recommends one organisation in Bitwarden, with the following collections:

- **founders** — accessible only to founders. Stripe master keys, Anthropic admin tokens, GitHub org admin tokens, banking credentials.
- **all-partners** — accessible to every full-time partner. Slack credentials, Google Workspace seats, Claude Desktop seat, GitHub repo access tokens.
- **specialists** — accessible to project specialists, scoped to the project. Just enough to do their work.
- **advisors** — accessible to advisors, scoped narrowly.
- **per-partner** — each full-time partner has their own collection for their personal-but-firm-related credentials (their personal Anthropic Pro, etc.).
- **shared-services** — credentials for services that all partners might need: a CI runner token, a shared monitoring dashboard.

### Onboarding procedure

When a partner is onboarded:

1. Add them to Bitwarden organisation.
2. Provision them into the appropriate collections per their cohort designation.
3. Install Bitwarden CLI on their work machine.
4. Configure Bitwarden as the SSH agent and the system credential store where supported.

### Rotation policy

- API keys with read-only scope: rotate annually.
- API keys with write scope: rotate every 6 months.
- API keys with admin scope: rotate every 3 months.
- Any credential after a partner exit: rotate within 24 hours of exit confirmation.
- Any credential after a suspected compromise: rotate immediately.

The Reporting & Business Review Skill Pack includes a rotation tracker (a simple sheet in the Brain); the Friday BR includes "credential rotations due" as a standing agenda item.

---

## Layer 2 — Trezor (crypto signing keys)

### Why Trezor as the default recommendation

Open source firmware (the framework's authors strongly prefer open-source hardware-wallet firmware for sovereignty reasons). Strong supply-chain integrity. Long track record. Supports the major chains used by 4thtech and Ethereum-family stablecoins. Not the cheapest hardware wallet, but the framework prioritises trust over cost in this layer.

### Alternative: Ledger

Closed-source firmware. Larger device ecosystem. The framework treats Ledger as a workable alternative for orgs that prefer it; the framework's preference is Trezor for the open-source posture.

### What goes on Trezor

- Treasury wallet signing keys (Gen 2+).
- Payroll wallet signing keys, if stablecoin payroll is enabled (Gen 2+).
- 4thtech wallet identity keys (privacy track).
- Smart-contract signing keys for long-tail entitlements (Gen 2+).
- Cotrugli Ledger co-signature keys (Gen 3+).

### What does NOT go on Trezor

- Software credentials (use Bitwarden).
- Recovery information for non-crypto accounts (use Bitwarden).
- Anything whose loss is not catastrophic (Trezor is for high-value, unrecoverable secrets).

### Setup procedure

1. Order the Trezor directly from `trezor.io`. Never accept second-hand or third-party-shipped hardware wallets.
2. On arrival, verify packaging integrity (Trezor ships with tamper-evident seals; check them).
3. Initialise the device offline. Never enter the seed phrase into any computer or phone — write it on the supplied recovery card with a pencil.
4. Store the seed card in a fire-safe location (a fireproof safe at home or in a deposit box). Do not store the seed digitally — not in Bitwarden, not in iCloud, not in a photo.
5. Configure the Trezor with a strong PIN.
6. Optionally configure a passphrase (the "25th word") for additional security; understand that losing this means losing the wallet permanently.

### Per-partner setup (privacy track)

Privacy-track partners need their own Trezor for 4thtech wallet identity. The firm typically covers this as a partner-onboarding cost (~€80 per device). The partner owns the device and the seed; the firm has no access. This is *the point*.

### Recovery procedure

If a Trezor is lost or destroyed:

1. Acquire a replacement Trezor.
2. Initialise it using the seed phrase.
3. The replacement wallet is identical to the original — same addresses, same transaction history.

If a Trezor is lost AND the seed is lost: the wallet's contents are unrecoverable. This is a feature of self-custody, not a bug.

---

## Layer 3 — Yubikey (hardware-key 2FA for org-level admin)

### Why Yubikey

Org-level admin accounts (GitHub organisation admin, Anthropic admin, Google Workspace super-admin) are the highest-value attack targets. SMS 2FA is broken (SIM-swap attacks). TOTP in a software authenticator is acceptable for individual partners but not for org admin. Hardware keys eliminate phishing of 2FA codes.

### What requires Yubikey

- GitHub organisation admin account.
- Anthropic admin account.
- Google Workspace super-admin account.
- Bitwarden organisation owner account.
- Any AWS / Azure / GCP root account if the firm uses cloud infrastructure.
- Any account with the ability to delete the Brain repository or revoke partner access at scale.

### Setup procedure

1. Acquire two Yubikeys per admin (a primary and a backup). Order from `yubico.com` directly.
2. Register both keys to every admin account before configuring any one of them as required.
3. Store the backup key in a separate secure location from the primary (e.g., founder's home safe + bank deposit box).
4. Document the registration in the founders Bitwarden collection.

### Loss procedure

If a Yubikey is lost: use the backup key to sign in; revoke the lost key from all accounts; order a replacement; register the replacement; restore the two-key configuration.

If both Yubikeys are lost: each account's recovery procedure must be invoked individually. This is painful by design — the inconvenience is the price of the security level.

---

## What goes where — the policy summary

| Credential type | Storage | Notes |
|---|---|---|
| API keys, OAuth tokens, SaaS passwords | Bitwarden | Per appropriate collection |
| SSH private keys | Bitwarden Secure Notes or SSH agent | Use the SSH agent if available |
| TOTP secrets | Bitwarden TOTP field | Or hardware key if account supports it |
| **Curator Shared Brain `admin_token`** | **Bitwarden — founders collection** | Gates GDPR Article 17 revoke endpoint; rotate on suspected compromise |
| **Firm Brain GitHub PAT (per partner)** | **Bitwarden — per-partner collection** | Fine-grained; Contents r/w on `<firm>-brain`; revoke on partner exit |
| **Ledger GitHub PAT (Routine bot identity)** | **Bitwarden — shared-services collection** | Fine-grained; Contents r/w on `<firm>-ledger`; signed-commits enabled |
| Crypto wallet seed phrases | Trezor recovery card (paper) | Never digital |
| Crypto signing keys | Trezor (on-device) | Never exported |
| 4thtech wallet identity (privacy track) | Trezor (on-device) | Per-partner |
| Org-admin account access | Yubikey (hardware) | Two keys per admin |
| Daily user 2FA | Bitwarden TOTP or Yubikey | Yubikey preferred for security; TOTP acceptable |

---

## Common violations to refuse

The framework's authors have seen each of the following in practice. Refuse all of them:

- API keys checked into git history. Even if the commit is later removed, the key is in the history. Rotate immediately and check `gh-secret-scanning` alerts.
- API keys in `claude_desktop_config.json` committed to GitHub. Use environment variable references instead (`"env": {"API_KEY": "${BITWARDEN_API_KEY}"}`).
- Crypto seeds in password managers, screenshots, photos, or cloud-synced notes. The seed must be on paper, stored physically.
- Org admin accounts protected by SMS 2FA. Replace with Yubikey within one week of org formation.
- "We'll fix this later" exceptions. Never. The first hour of a security violation is the cheapest hour to fix it.

---

## Privacy track addendum

On the privacy track, the secrets policy adds:

- **4thtech wallet identity** is on Trezor, per-partner, never in Bitwarden.
- **PollinationX storage NFT private keys** are on Trezor.
- **Local LM Studio / Ollama configurations** typically don't have credentials, but if they do, those go in Bitwarden.
- **The always-on machine** (Mac mini / NUC / Pi) running headless LM Studio must have full-disk encryption, a strong login password, and no remote login except via SSH key (no password authentication).

The privacy track's threat model is broader (less perimeter security from Anthropic / Google infrastructure), so the discipline is correspondingly tighter.

---

## Final note

The secrets policy is not glamorous. It is one of the most boring documents in the framework. It is also one of the most important — every other discipline in ØØT (the Brain, the Klarna Test, the variable-pay attribution, the partner trust model) collapses if the firm's credentials are compromised.

The first time a secret leaks, the cost is the rotation. The second time, the cost is the trust. The third time, the cost is the firm.

Read the policy. Implement the policy. Review the policy at every quarterly partner check-in.