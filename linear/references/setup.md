# Linear MCP setup

Read this reference only for configuration, authentication, identity isolation, or connection troubleshooting. Runtime issue work belongs in the main skill.

## Identity model

Use generic app actors rather than accounts named after a shell or product:

- Planner
- Builder
- Reviewer

The AI client is the harness. Herdr may host the process, but it does not determine the role or Linear identity.

Create one private Linear OAuth application per role and enable client-credentials tokens. Give each app only the team access and scopes it needs. Keep client IDs, client secrets, and access tokens in the user's secrets manager.

## Manual access-token minting

Linear OAuth applications mint client-credentials tokens through the Linear API endpoint, not through the MCP OAuth issuer:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  https://api.linear.app/oauth/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'scope=read,write' \
  --data-urlencode "client_id=${PROJECT_LINEAR_ROLE_CLIENT_ID}" \
  --data-urlencode "client_secret=${PROJECT_LINEAR_ROLE_CLIENT_SECRET}"
```

Store the returned `access_token` under a role-specific environment variable such as:

```text
PROJECT_LINEAR_PLANNER_ACCESS_TOKEN
PROJECT_LINEAR_BUILDER_ACCESS_TOKEN
PROJECT_LINEAR_REVIEWER_ACCESS_TOKEN
```

Client-credentials access tokens last about 30 days. This setup uses manual renewal unless the user chooses to add a separate token helper later.

Do not configure `grantType: client_credentials` as MCP OAuth against `https://mcp.linear.app/mcp`. That server discovers `https://mcp.linear.app/token`, which does not accept the client ID of a Linear API OAuth application and returns `Client not found`. Mint through `https://api.linear.app/oauth/token`, then pass the result to MCP as a bearer token.

## Role-isolated Pi profiles

Keep one profile per role so a session cannot accidentally select another role's MCP server:

```text
.pi/mcp-profiles/planner.json
.pi/mcp-profiles/builder.json
.pi/mcp-profiles/reviewer.json
```

Each profile exposes the same generic server name and differs only in the bearer-token environment variable. The name matters: this skill and its compatibility gate look for a server named `linear`, and downstream instructions refer to `/mcp reconnect linear`. A role-suffixed server name (`linear-builder`) leaks the role into the tool namespace, breaks those references, and invites a session to select the wrong role's server when profiles merge. Keep every other option (`lifecycle`, `directTools`, and so on) identical across the three profiles so the role token is the only difference between them:

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

Launch Pi with exactly one role profile:

```bash
pi --mcp-config .pi/mcp-profiles/planner.json
pi --mcp-config .pi/mcp-profiles/builder.json
pi --mcp-config .pi/mcp-profiles/reviewer.json
```

`--mcp-config` participates in the adapter's config merge; it does not replace the project root `.mcp.json`. Keep role identities out of the root `.mcp.json`, or they will appear in every role session and may override the generic `linear` entry. A normal Pi session without a role profile should have no role-bearing Linear connection.

Keep profiles local when they describe a personal workspace. Prefer `.git/info/exclude` for a private per-clone setup:

```gitignore
/.mcp.json
/.pi/mcp.json
/.pi/mcp-profiles/
/.pi/mcp-traces/
```

Use the repository `.gitignore` instead only when the whole project has adopted these local files as a shared convention.

## Connection checks

Bearer authentication has no interactive OAuth step. `Ctrl+A` is for OAuth and is not expected to work with these profiles. Connect or refresh with:

```text
/mcp reconnect linear
```

Then make read-only calls to verify the authenticated actor, workspace, teams, project, and issues. Before broad use, make one controlled comment and confirm that Linear attributes it to the intended app actor.

Useful failures:

- `Client not found`: client credentials were sent to the MCP OAuth issuer instead of the Linear API token endpoint, or the client ID is wrong.
- `Client does not support the client_credentials grant type`: enable client-credentials tokens on the OAuth app.
- Bearer reconnect fails after working previously: check token expiry and mint a new role token.
- The wrong app appears: stop writes and check the launched profile, root `.mcp.json`, and injected access-token name.

## Other harnesses

Keep the runtime server name `linear` and select one role identity per client session. Codex, Zed, and other clients may use different config formats, but they should preserve the same boundary: one role-bearing token is available to the session, and the authenticated actor is checked before writes.
