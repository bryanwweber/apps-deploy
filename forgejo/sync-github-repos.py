#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "clientapi_forgejo",
#     "pygithub",
#     "rich",
#     "typer",
# ]
# ///
from typing import Annotated
from webbrowser import get

import clientapi_forgejo
import typer
from clientapi_forgejo.exceptions import ConflictException
from github import Auth, Github
from rich import print

app = typer.Typer()

EXTRA_REPOS = {
    "https://github.com/apprenticeharper/DeDRM_tools",
    "https://github.com/oliverphilcox/Keplers-Goat-Herd",
    "https://github.com/ddean4040/phpZoteroWebDAV",
    "https://github.com/bryanwweber/poliastro",
    "https://github.com/lorenzodifuccia/safaribooks",
}


def get_github_repo_urls(client: Github) -> set[str]:
    """Get all the repos for the authenticated user."""
    user = client.get_user()
    repos = set(
        r.clone_url.removesuffix(".git")
        for r in user.get_repos(affiliation="owner")
        if not r.fork
    )
    return repos


def get_forgejo_original_urls(client: clientapi_forgejo.ApiClient) -> set[str]:
    """Get all the repos for the authenticated user."""
    api_instance = clientapi_forgejo.UserApi(client)
    page = 1
    all_responses = []
    while True:
        api_response = api_instance.user_current_list_repos(page=page, limit=100)
        if not api_response:
            break
        all_responses.extend(api_response)
        page += 1
    return set(r.original_url for r in all_responses if r.original_url is not None)


def mirror_new_repos(
    client: clientapi_forgejo.ApiClient, new_repos: set[str], github_auth_token: str
) -> None:
    """Mirror new repos to Forgejo."""
    api_instance = clientapi_forgejo.RepositoryApi(client)
    for repo in new_repos:
        opts = clientapi_forgejo.MigrateRepoOptions(
            auth_token=github_auth_token,
            clone_addr=repo,
            issues=True,
            labels=True,
            milestones=True,
            mirror=True,
            pull_requests=True,
            releases=True,
            repo_name=repo.split("/")[-1],
            wiki=True,
        )
        try:
            response = api_instance.repo_migrate(body=opts)
            print(f"[green]Mirrored {response.full_name}")
        except ConflictException:
            print(f"[red]Conflict: {repo.split('/')[-1]} already exists")


@app.command()
def main(
    forgejo_api_key: Annotated[
        str, typer.Option(default=..., envvar="FORGEJO_API_KEY")
    ],
    github_auth_token: Annotated[
        str, typer.Option(default=..., envvar="GH_AUTH_TOKEN")
    ],
    host_url: Annotated[str, typer.Option(default=..., envvar="FORGEJO_HOST_URL")],
) -> None:
    config = clientapi_forgejo.Configuration(host=host_url)
    config.api_key["AuthorizationHeaderToken"] = forgejo_api_key
    config.api_key_prefix["AuthorizationHeaderToken"] = "Bearer"
    api_client = clientapi_forgejo.ApiClient(config)

    auth = Auth.Token(github_auth_token)
    g = Github(auth=auth)

    try:
        github_repos = get_github_repo_urls(g)
        github_repos.update(EXTRA_REPOS)
        new_repos = github_repos - get_forgejo_original_urls(api_client)
        if not new_repos:
            print("[blue]No new repos to mirror")
            return
    finally:
        g.close()

    print(f"[green]Found {len(new_repos)} new repos")
    try:
        mirror_new_repos(api_client, new_repos, github_auth_token)
    finally:
        api_client.rest_client.pool_manager.clear()


if __name__ == "__main__":
    app()
