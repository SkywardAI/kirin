# Contributing Guidelines

*All forms of contribution are highly encouraged and appreciated* 

### Contents

- [Code of Conduct](#code-of-conduct)
- [Asking Questions](#asking-questions)
- [Feature Requests](#feature-requests)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Writing Commit Messages](#writing-commit-messages)
- [Code Review](#check_mark-code-review)
- [Coding Style](#care-coding-style)


> **This guide outlines the expectations for everyone involved in the project so that we can improve it together while also creating a fun and welcoming space for everyone to contribute. Following these guidelines will help make sure that everyone involed has a positive experience.**

## Code of Conduct

Please review our Code of Conduct . It is in effect at all times. We expect it to be honored by everyone contributing to the project.

## Asking questions

Please feel free to ask questions under issues or in the discussion forums. If an issue does not have a discussion open then feel free to open a new one and project members will get to it at the earliest possibility.

### Opening an Issue

Before creating an issue, check if you are using the latest version of the project. If you are not up-to-date, see if updating fixes your issue first.

### Reporting Security Issues

Review our Security Policy and please raise it with one of the project mods.

### Bug Reports and Other Issues

A great way to contribute to the project is to send a detailed issue when you encounter a problem. We always appreciate a well-written, thorough bug report.

In short, since you are most likely a developer, **provide a ticket that you would like to receive**.

- Search through existing issues to see if the issue has been raised before. We would like to avoid duplication of issues. If you encountered the same issue as someone else then please comment under it that you're facing the same issue so we'll be able to prioritize it over other issues. 

- **Please complete the provided issue template** The bug report template outlines all the information to be provided while pointing out a bug. Please be clear, concise, and descriptive. Provide as much information as you can, including steps to reproduce, stack traces, compiler errors, library versions, OS versions, and screenshots (if applicable).

- **Use [GitHub-flavored Markdown](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax).** Please put code blocks and console outputs in backticks (```). This helps enhance the readability

## Feature Requests

Feature requests are welcome! While we will consider all requests, we cannot guarantee your request will be accepted. However, you are welcome to discuss it with us and then put in a pull request!

- **Please do not open a duplicate feature requests.**. If you find your feature (or one very similar) previously requested, comment under that issue and we'll evalute it 



## Submitting Pull Requests

The format for submitting pull requests is as follows

```
**Description**

This PR fixes #

**Notes for Reviewers**


**[Signed commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)**
- [ ] Yes, I signed my commits.
 

<!--
Thank you for contributing to Meshery! 

Contributing Conventions:

1. Include descriptive PR titles with [<component-name>] prepended.
2. Build and test your changes before submitting a PR. 
3. Sign your commits

By following the community's contribution conventions upfront, the review process will 
be accelerated and your PR merged more quickly.
-->

```

 Before [forking the repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) and [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests) for non-trivial changes, please open an issue and discuss the changes or the intended approach for solving the problem in the comments for an issue that already exists.

*Note: All contributions will be licensed under the project's license.*


- **Smaller is better.** Submit **one** pull request per bug fix or feature. A pull request should focus on bug fixes pertaining to a single bug or feature implementation. Please **do not** reformat or refactor any code that is not related to your change. It is always better to **submit multiple small pull requests** rather than a single large one. 

- **Coordinate bigger changes.** for larger and more substantial changes please discuss it with the maintainers before beginning the implementation. We would love to know your plan and would not want your code and time to go to waste if the approach is not suitable for the issue. This can be done by raising an issue or opening a discussion on github

- **Prioritize understanding over cleverness.** Please write clear and concise code. Source code usually gets written only once and is read often so this means that we need to ensure that the code is clear, the purpose and logic should be obvious to a developer, please add comments to the code that explains the code. 

- **Follow existing coding style and conventions.** Please maintain consistence with the code style, formatting and conventions used in the rest of the codebase. Consistency ensures that its easy to review and helps making modification easier in the future.

- **Include test coverage.** Please add unit or UI tests wherever possible. Please follow existing patterns for implementing tests.

- **Add documentation.**

- **Update the CHANGELOG** for all changes and bug fixes please make an entry to the changelog and add the ID with your github Username (example: "- Fixed crash in profile view. #123 @githubUsername")

- **Use the repo's default branch.** Branch from and [submit your pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to the repo's default branch.

- **[Resolve any merge conflicts](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-on-github)** that occur.

- **Promptly address any CI failures**. If your pull request fails to build or pass tests, please push another commit to fix it. 

- When writing comments, use properly constructed sentences, including punctuation.



## Writing Commit Messages

Please write a great commit message.

1. Separate the subject from the body using a blank line
1. Subject line shouldn't be more than 50 characters
1. Use the imperative mood in the subject line (example: "Fix networking issue")
1. Wrap the body at about 72 characters
1. Use the body to explain your process of why you've done what you did.
1. If applicable, prefix the title with the relevant component name. (examples: "[Docs] Fix typo", "[Profile] Fix missing avatar")

```
[Tag] Short summary of changes in less than 50 characters

Add a more detailed explanation here if necessary. Please provide us 
some information about the issue that is being fixed. The body can be
multiple paragraphs.

Wrap this up in under 72 characters. You may chose to avoid the body
if the subject is self explanatory but please put in a blank line after
the subject to show where the body has begun.

Explain the problem that this commit solves. Focus on why the changes
are being made, this will help reviewers and yourself read the patch
and understand why a solution was implemented. Please mention if there
are any side effects or other consequences of this change.

- Bullet points are okay as well. Please use a hyphen to denote a bullet
point followed by a space with a blank line between each point to be able
to distinguish between them

Note the fixed or relevant GitHub issues at the end:

Resolves: #123
See also: #456, #789
```

## Code Review

- **Review the code, not the author.** Suggest improvements without disparaging or insulting the author, the feedback should be constructive and actionable while also explaining your reasoning.

- **You are not your code.** Please do not take code reviews personally. When your code is critiqued, questioned, or constructively criticized, remember that you are not your code, only methods to make it more efficient are being proposed. 

- **Always do your best.** No one writes bugs on purpose. Do your best, and learn from your mistakes.

## Coding Style

Consistency is the most important. Please follow the existing style, formatting and naming conventions of the file being modified and of the project as a whole. Not following this would result in prolonges review processes that will have to focus on updating the formatting of the code over improvements to its functionality and performance.

If in doubt, please ask or search the codebase for something similar.

When possible, style and format will be enforced with a linter.