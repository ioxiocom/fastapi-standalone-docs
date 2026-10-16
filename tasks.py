from invoke import Exit, task


@task
def release(ctx):
    version = ctx.run("uv version --short --color never", hide=True).stdout.strip()
    print(f"Releasing {version}")
    ctx.run(f"git tag {version}", echo=True)
    ctx.run(f"git push origin {version}", echo=True)


def run_test_cmd(ctx, cmd) -> int:
    print("=" * 79)
    print(f"> {cmd}")
    return ctx.run(cmd, warn=True).exited


@task
def test(ctx):
    failed_commands = []

    if run_test_cmd(ctx, "pre-commit run --all-files"):
        failed_commands.append("Pre commit hooks")

    if run_test_cmd(ctx, "mypy"):
        failed_commands.append("Mypy")

    if run_test_cmd(ctx, "pytest"):
        failed_commands.append("Unit tests")

    # Checks the locked dependencies for known vulnerabilities
    if run_test_cmd(ctx, "uv audit --preview-features audit-command"):
        failed_commands.append("uv audit")

    if failed_commands:
        msg = "Errors: " + ", ".join(failed_commands)
        raise Exit(message=msg, code=len(failed_commands))
