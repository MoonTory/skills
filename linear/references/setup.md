# Linear MCP setup

Read this reference only for configuration, authentication, identity isolation, delegation, or connection troubleshooting. Runtime issue work belongs in the main skill.

## Identity model

Use one private Linear OAuth application for each workflow role:

- Orchestrator.
- Planner.
- Builder.
- Reviewer.

Use generic app actors rather than accounts named after a shell, model, or product. The AI client is the harness; it does not determine the role or Linear identity.

Give each app only the required team access. Keep client IDs, client secrets, and access tokens in the user's secret manager. Never store a token in the skill, repository, shared `.mcp.json`, shell history, or a committed environment file.

## Required token scopes

Mint every role token with:

```text
read,write,app:assignable
```

`app:assignable` allows an app actor to become the issue delegate. It does not make the app a normal human assignee.

Linear OAuth applications mint client-credentials tokens through the Linear API endpoint, not through the MCP OAuth issuer:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  https://api.linear.app/oauth/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'scope=read,write,app:assignable' \
  --data-urlencode "client_id=${PROJECT_LINEAR_ROLE_CLIENT_ID}" \
  --data-urlencode "client_secret=${PROJECT_LINEAR_ROLE_CLIENT_SECRET}"
```

Store the returned `access_token` under one role-specific environment variable:

```text
PROJECT_LINEAR_ORCHESTRATOR_ACCESS_TOKEN
PROJECT_LINEAR_PLANNER_ACCESS_TOKEN
PROJECT_LINEAR_BUILDER_ACCESS_TOKEN
PROJECT_LINEAR_REVIEWER_ACCESS_TOKEN
```

Client-credentials access tokens last about 30 days. This setup uses manual renewal unless the user chooses a separate token helper.

Do not configure `grantType: client_credentials` as MCP OAuth against `https://mcp.linear.app/mcp`. That server discovers `https://mcp.linear.app/token`, which does not accept the client ID of a Linear API OAuth application. Mint through `https://api.linear.app/oauth/token`, then pass the result to MCP as a bearer token.

## Token replacement

Requesting a different client-credentials scope set invalidates the app's previous token. Replace roles one at a time:

1. Mint the replacement token with `read,write,app:assignable`.
2. Replace that role's secret immediately.
3. Restart or reconnect only that role's MCP session.
4. Make read-only identity and workspace checks.
5. Confirm the old token no longer drives an active session.
6. Continue with the next role.

Stop if the actor is wrong or the new token cannot see the intended team. Do not fall back to a human OAuth connection.

## Four-profile connection matrix

Each session exposes exactly one role-bearing server named `linear`:

| Profile | Normal harness | Bearer-token environment variable | Linear responsibility |
| --- | --- | --- | --- |
| Orchestrator | Codex or Claude | `PROJECT_LINEAR_ORCHESTRATOR_ACCESS_TOKEN` | Metadata, status, delegation, coordination, and landing |
| Planner | Pi or another isolated worker | `PROJECT_LINEAR_PLANNER_ACCESS_TOKEN` | Exploration, Plan, and Plan ready |
| Builder | Pi or another isolated worker | `PROJECT_LINEAR_BUILDER_ACCESS_TOKEN` | Builder handoff and validation evidence |
| Reviewer | Pi or another isolated worker | `PROJECT_LINEAR_REVIEWER_ACCESS_TOKEN` | Review document and verdict |

Keep the runtime server name `linear`. The selected profile determines identity. Do not expose several role tokens in one session or use role-suffixed server names that let an agent select the wrong identity.

## Human assignee and app delegate

Keep the human owner as the issue assignee. App actors use Linear's delegate field:

| Phase          | Assignee    | Delegate     |
| -------------- | ----------- | ------------ |
| Scoping        | Human owner | Planner      |
| Implementation | Human owner | Builder      |
| Review         | Human owner | Reviewer     |
| Owner input    | Human owner | None         |
| Landing        | Human owner | Orchestrator |

Only Orchestrator changes the delegate. Planner, Builder, and Reviewer publish their phase output, then return control. Orchestrator reads that output, changes status and delegate together, and reads the issue back.

If the MCP issue-update tool does not expose `delegate`, `delegateId`, or the equivalent agent field, treat it as a tool limitation. Do not put the app in the human assignee field. Use an authorized Linear API or UI path for delegation, or stop the pilot until the tool supports it.

## Role-isolated Pi MCP profiles

Keep one local MCP identity profile per Pi publishing role:

```text
.pi/mcp-profiles/planner.json
.pi/mcp-profiles/builder.json
.pi/mcp-profiles/reviewer.json
```

Each exposes one generic server and differs only in the bearer-token variable:

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp",
      "auth": "bearer",
      "bearerTokenEnv": "PROJECT_LINEAR_BUILDER_ACCESS_TOKEN",
      "lifecycle": "lazy"
    }
  }
}
```

Launch Pi with exactly one MCP identity profile and the matching isolated skill profile. These are separate controls:
`--skill-profile` selects the instruction catalog, while `--mcp-config` selects the Linear actor. These examples assume
the local skill catalog defines `linear-plan`, `linear-build`, and `linear-review` profiles:

```bash
pi --no-skills --skill-profile linear-plan --mcp-config .pi/mcp-profiles/planner.json
pi --no-skills --skill-profile linear-build --mcp-config .pi/mcp-profiles/builder.json
pi --no-skills --skill-profile linear-review --mcp-config .pi/mcp-profiles/reviewer.json
```

An Explorer does not publish Linear evidence. Start it with the plain `explore` skill profile and no role-bearing
`--mcp-config`.

`--mcp-config` participates in the adapter's config merge; it does not replace the project root `.mcp.json`. Keep role identities out of the root `.mcp.json`, or they may appear in every role session and override the generic `linear` entry. A normal Pi session without a role profile should have no role-bearing Linear connection.

Keep personal profiles local. Prefer `.git/info/exclude` for a private per-clone setup:

```gitignore
/.mcp.json
/.pi/mcp.json
/.pi/mcp-profiles/
/.pi/mcp-traces/
```

Use the repository `.gitignore` only when the whole project has adopted these local files as a shared convention.

## Codex Orchestrator profile

Keep the Orchestrator connection project-local in `.codex/config.toml`:

```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
bearer_token_env_var = "PROJECT_LINEAR_ORCHESTRATOR_ACCESS_TOKEN"
required = true
```

Remove or disable the inherited personal `linear` OAuth connection for that project and clear its stored Linear MCP OAuth. Keep the normal OpenAI account login. A configured bearer token is tried before OAuth, so leaving personal OAuth available can hide a missing environment variable by reconnecting as the human.

The Codex desktop app must inherit `PROJECT_LINEAR_ORCHESTRATOR_ACCESS_TOKEN`. A variable visible in an interactive shell is not proof that an app launched from the desktop sees it. Use the user's secret manager or app-launch environment, fully restart Codex, and start a fresh task after changing the profile.

## Claude Orchestrator profile

Keep the Orchestrator connection in Claude's project-local scope rather than the repository's shared `.mcp.json`. Clear the existing Linear MCP OAuth, remove the old local connection, and add a bearer header with a literal environment placeholder:

```bash
claude mcp remove linear --scope local
claude mcp add-json --scope local linear \
  '{"type":"http","url":"https://mcp.linear.app/mcp","headers":{"Authorization":"Bearer ${PROJECT_LINEAR_ORCHESTRATOR_ACCESS_TOKEN}"}}'
```

The single quotes keep the token out of the stored command and shell expansion. Launch Claude from an environment that receives the token, then start a fresh session. Keep the normal Anthropic account login; only the Linear MCP authentication changes.

## Identity verification

Bearer authentication has no interactive OAuth step. Reconnect or restart the client, then make read-only calls that prove:

1. Authenticated app actor.
2. Workspace.
3. Team.
4. Project.
5. One known issue.

Before the first workflow write, verify that:

- The actor name matches the selected profile.
- The session exposes only one role-bearing `linear` connection.
- The human-owned Codex or Claude OAuth connection cannot be selected.
- The token can see only the intended team scope.

Use a dedicated pilot issue for the first delegation and write-attribution checks. Do not add test comments to completed production issues.

The full write gate checks:

- Human assignee remains unchanged.
- Orchestrator can set and clear each app delegate.
- Each role's comment or document shows the correct author.
- Orchestrator makes every metadata and status change.
- Read-back confirms the actor, delegate, fields, and status after each write.

## Useful failures

- `Client not found`: client credentials were sent to the MCP OAuth issuer instead of the Linear API token endpoint, or the client ID is wrong.
- `Client does not support the client_credentials grant type`: enable client-credentials tokens on the OAuth app.
- App cannot be delegated: remint with `app:assignable` and confirm the MCP tool exposes the delegate field.
- Bearer reconnect fails after working previously: check token expiry and mint a new role token.
- Human name appears: stop writes, clear cached OAuth, check config precedence, and confirm the token environment variable reaches the process.
- Wrong app appears: stop writes and check the selected profile, merged configs, and injected token name.
- Several role servers appear: stop the session and remove merged shared or root role entries before reconnecting.
