---
title: Providers
description: Choose which AI provider the local game agent uses, from the official ZUKU AI provider to your own API keys and local models.
section: Guide
---

# Providers

A provider is the AI service the local game agent calls while it builds your game. By default, the CLI uses the official **ZUKU AI** provider, `zuku`, with the model `zuku/auto`. Other providers are only used when you select them yourself.

The CLI never switches providers on its own. If the selected provider fails, the run stops with an error. It never falls back to another provider, Codex, or any paid service.

`zuku` and `zukujs` share the same provider settings, secret store and model cache.

## Commands

```sh
zuku provider list                     # all providers, ● marks the current one
zuku provider show <id>
zuku provider use <id>                 # omit <id> in a terminal to pick from a list
zuku provider configure <id> [options]
zuku provider enable <id>
zuku provider disable <id>             # the current provider can't be disabled
zuku provider add [options]            # custom endpoint
zuku provider remove <id> --yes        # custom providers only; also deletes their stored key
```

Every command supports `--json`, and the output never includes credential values. In pipes and CI, the CLI never prompts. If a required value is missing, it exits with `INVALID_INPUT` (exit code 2).

## ZUKU AI

ZUKU AI is the official provider for the local agent. It uses your ZUKU account, signed in with the generation permission:

```sh
zuku login zuku --generate
zuku provider use zuku
```

`zuku/auto` is a routing alias on the server, and the CLI doesn't ship a fixed ZUKU model list. Run `zuku model list --provider zuku` to see what is currently available. See [Models](models.md).

The local CLI can use your own provider credentials or a local model. ZUKU AI availability depends on the server's permissions and model catalog. Hosted web AI and in-app AI aren't publicly open, and their opening date is undecided. An Android app preview is available at [the download page](https://apk.zuzunza.com/).

## Built-in providers

Official provider API keys are a normal, supported way to run the agent. Store a key with `zuku auth login --provider <id>`, or set the provider's standard environment variable.

| ID | Name | Credentials |
| --- | --- | --- |
| `zuku` | ZUKU AI | ZUKU account sign-in (`zuku login zuku --generate`) |
| `openai` | OpenAI | API key, `OPENAI_API_KEY` |
| `anthropic` | Anthropic | API key, `ANTHROPIC_API_KEY` |
| `google` | Google Gemini | API key, `GEMINI_API_KEY` or `GOOGLE_GENERATIVE_AI_API_KEY` |
| `openrouter` | OpenRouter | API key, `OPENROUTER_API_KEY` |
| `amazon-bedrock` | AWS Bedrock | AWS credential chain or `AWS_BEARER_TOKEN_BEDROCK`; region required |
| `google-vertex` | Vertex AI | Google application default credentials; the project option cannot currently be set through CLI Agent Core |
| `azure` | Azure OpenAI | API key, `AZURE_OPENAI_API_KEY` or `AZURE_API_KEY` |
| `mistral` | Mistral | `MISTRAL_API_KEY` |
| `deepseek` | DeepSeek | `DEEPSEEK_API_KEY` |
| `groq` | Groq | `GROQ_API_KEY` |
| `xai` | xAI | `XAI_API_KEY` |
| `alibaba` | Qwen (DashScope) | `DASHSCOPE_API_KEY` or `ALIBABA_API_KEY` |
| `togetherai` | Together AI | `TOGETHER_API_KEY` |
| `fireworks` | Fireworks AI | `FIREWORKS_API_KEY` |
| `cerebras` | Cerebras | `CEREBRAS_API_KEY` |
| `sambanova` | SambaNova | `SAMBANOVA_API_KEY` |
| `huggingface` | Hugging Face | `HF_TOKEN` or `HUGGINGFACE_API_KEY` |
| `vercel` | Vercel AI Gateway | `AI_GATEWAY_API_KEY` |
| `cloudflare-ai-gateway` | Cloudflare AI Gateway | API key; required account and gateway IDs cannot currently be configured through the CLI |
| `ollama` | Ollama | Local, no credentials |
| `lmstudio` | LM Studio | Local, no credentials |
| `codex` | Codex **Experimental** | Codex sign-in, `zuku login codex --experimental` |

The `codex` provider is an **Experimental**, unofficial integration, marked `(exp!)` in CLI output. It is never selected automatically.

### Configure a built-in provider

```sh
zuku provider configure azure --base-url https://<resource>.openai.azure.com/openai/v1
zuku provider configure amazon-bedrock --region us-east-1
zuku provider configure openrouter --model <vendor>/<model> --default-model <vendor>/<model>
```

Official endpoints are fixed and can't be changed (`PROVIDER_ENDPOINT_FIXED`). Configuration supports model additions/removals, `--default-model` and `--api-key-env`. Agent Core currently accepts only `region` and `location` in the options object, subject to each provider's rules.

`--project`, account or gateway ID options, project or catalog options, `--clear-api-key-env`, `--header-env`, `--header-secret` and `--remove-header` remain in the parser but fail with `CORE_PROTOCOL_GAP` before changing settings. Vertex project configuration and Cloudflare gateway configuration therefore aren't usable through these CLI commands yet.

## Custom endpoints **Experimental**

You can add an OpenAI-compatible or Anthropic-compatible endpoint:

```sh
zuku provider add --id local-ai --name "Local AI" --type openai-chat \
  --base-url http://localhost:8000/v1 --model my-model --api-key-env LOCAL_AI_KEY
```

`--type` accepts `openai-chat`, `openai-responses` or `anthropic`. `--base-url` must use `https://`, or `http://` on loopback (`127.0.0.1`, `localhost`, `[::1]`). The first `--model` becomes the default. Custom endpoints are always marked **Experimental** and unofficial, because the CLI can't confirm the service behind them. Running the agent with one requires `--experimental`.

## Storage

On Linux and macOS, provider settings live in `~/.config/zukujs/providers/`. The directory is owner-only (0700), and the files are owner-only (0600). On Windows, they live in `%LOCALAPPDATA%\ZukuJS\providers\`.

- `config.json` holds public settings only, such as provider, model and environment variable names. The CLI refuses to read or write it if it contains a key.
- API keys are kept in a separate protected secret store. See [Authentication](authentication.md).

For agent usage, see [Agent](agent.md). For all commands, see [Commands](commands.md).
