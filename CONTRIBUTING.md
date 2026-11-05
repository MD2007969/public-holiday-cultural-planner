# Contributing to Group 9

Thank you for contributing to the Public Holiday & Cultural Awareness Planner.

## Team rules

1. Work on your assigned personal branch. Do not push directly to `main`.
2. Commit your own work using clear, descriptive commit messages.
3. Keep the agreed class, module, and function names unless the team agrees to a change first.
4. Test your module independently before opening a pull request.
5. Include a short summary of what changed and how you tested it in your pull request.
6. Do not commit API keys, passwords, local secrets, virtual environments, or generated personal data.
7. Communicate integration changes early. Do not silently change another member's interface.

## Suggested commit messages

- `feat: implement holiday API client`
- `feat: add cultural guide generation`
- `fix: handle invalid country codes`
- `test: add validation tests`
- `docs: update setup instructions`

## Pull request checklist

Before requesting review, confirm:

- [ ] The work is on your assigned branch.
- [ ] The module uses the agreed names and interfaces.
- [ ] The code runs without syntax errors.
- [ ] Relevant success and failure cases were tested.
- [ ] No secrets or unrelated files are included.
- [ ] The pull request explains the implementation and test steps.

Open a pull request from your branch into `main`. A pull request is for review; do not merge it until the group leader has reviewed and approved it.

## Integration

The current interface proposals are documented in [docs/INTEGRATION_CONTRACT.md](docs/INTEGRATION_CONTRACT.md). If an interface needs to change, discuss it with the affected members and update that document before merging.
