# Contributing to ChatWizard

Thank you for considering to contribute to ChatWizard! Here's a guide on how you can contribute:

## Prerequisites

 - Make sure to have `Python 3.7` or above installed
 - Install the following packages: `discord` and `openai`
 - You will also need: `black>=22`, `pytest>=4.3.0` and `flake8>=3.7.8`
 
Now you're ready to get started!

## Getting Started

1. Fork the repository
2. Clone the forked repository:

   ```
   git clone https://github.com/YOUR_USERNAME/ChatWizard.git
   ```

3. Install the development dependencies:

   ```
   make develop
   ```
   
4. Create a new branch for your changes:

   ```
   git checkout -b feature/my-new-feature
   ```

## Before Opening a Pull Request

1. Make sure your code follows the project's code style by running the linter:

   ```
   make lints
   ```

   If there are any issues, you can auto-format the code by running:

   ```
   make format
   ```

2. Check for any packaging issues:

   ```
   make check
   ```

3. Run the tests to make sure everything works as expected:

   ```
   make tests
   ```

4. Commit your changes and open a pull request.

## Pull Request Process

1. Provide a clear and descriptive title for your pull request, and include a summary of your changes.
2. Make sure your pull request contains a single, logically organized set of changes. If you have made multiple unrelated changes, open separate pull requests for each of them.
3. Include any relevant issue numbers in the description of your pull request to link the issues.
4. Make sure your pull request is up-to-date with the main branch by periodically pulling the changes from the main branch:

   ```
   git fetch origin main
   git rebase origin/main
   ```

5. Once your pull request is approved and merged, you can delete your feature branch.

## Reporting Issues

If you encounter any issues or have any suggestions for improvements, please open a new issue in the repository.

## Code of Conduct

Please respect and adhere to our [Code of Conduct](https://github.com/ChatWizard/ChatWizard/blob/master/CODE_OF_CONDUCT.md) when contributing to this project.

Thank you again for your contributions, and happy coding!
