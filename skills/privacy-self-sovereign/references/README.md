# References — Skill Pack S12 (Privacy / Self-Sovereign Stack)

The technical foundations of the framework's sovereignty-first track.

## Primary tooling

1. **4thtech project** — on-chain dMail / dChat / file transfer. Wallet-as-identity. https://github.com/4thtech / https://wiki.4thtech.io/quickstart/index. Quickstart: https://wiki.4thtech.io/quickstart/index.

2. **PollinationX** — decentralised storage with NFT-based capacity. https://wiki.pollinationx.io/introduction/start-here.

3. **The Curator project** — Brain implementation. Cloud-LLM ingest in Gen 1; local-LLM ingest = Gen 2 roadmap. https://github.com/talirezun/the-curator.

4. **LM Studio** — local LLM runner with native MCP support (≥0.3.17). https://lmstudio.ai/. MCP docs: https://lmstudio.ai/docs/local-server/mcp.

5. **`haris-musa/excel-mcp-server`** — MIT-licensed Excel MCP server. https://github.com/haris-musa/excel-mcp-server.

6. **Desktop Commander MCP** — local filesystem MCP server. https://github.com/wonderwhy-er/DesktopCommanderMCP.

7. **GitHub MCP** — cross-machine sync. https://github.com/modelcontextprotocol/servers/tree/main/src/github.

## Hardware

8. **Trezor Suite** — open-source hardware wallet firmware. https://trezor.io/. Per-partner cost: ~€80.

9. **Yubikey** — hardware security key for org-admin 2FA. https://yubico.com/.

10. **Mac mini M4 Pro / Intel NUC / Raspberry Pi 5** — the always-on machine options. The framework's authors test on Mac mini M4 Pro 32GB primarily.

11. **CyberPower / APC UPS** — recommended 1500-3000VA range. The §4.2 always-on-machine guidance.

## Standards

12. **Model Context Protocol (MCP)** — open standard. https://modelcontextprotocol.io/. Governed by Linux Foundation Agentic AI Foundation.

13. **Linux Foundation Agentic AI Foundation (AAIF)** — December 2025 governance hand-off. https://lfaidata.foundation/.

## Adjacent

14. **Tailscale / WireGuard** — for remote access to the always-on machine. https://tailscale.com/. The framework's authors use Tailscale.

15. **Ollama** — alternative to LM Studio for local model hosting. https://ollama.com/. Functional substitute for LM Studio in the privacy track; the framework treats them as interchangeable.

16. **Open WebUI** — open-source alternative front-end for local models. https://github.com/open-webui/open-webui.

## Cross-references inside ØØT

- ØØT [`MANIFESTO.md`](../../../MANIFESTO.md), Thesis 5 — Composable Lego (the privacy track is the framework's commitment to vendor-neutrality).
- ØØT [`governance/SECRETS-POLICY.md`](../../../governance/SECRETS-POLICY.md) — the two-layer Bitwarden + Trezor + Yubikey discipline.
- ØØT [`routines/SPEC.md`](../../../routines/SPEC.md) — privacy-track Routine prompts (R1-R8 cloud + privacy parity).
- ØØT [`templates/excel/SPEC.md`](../../../templates/excel/SPEC.md) — all 9 templates the privacy track reads/writes via Excel MCP.
- ØØT [`templates/brain/FIRM-ONTOLOGY.md`](../../../templates/brain/FIRM-ONTOLOGY.md) — the `firm/privacy-track/` slug convention.
