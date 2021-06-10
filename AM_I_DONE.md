# When is it Time to Submit a Pull Request?

Here is an extensive, but not exhaustive list of things to check for before submitting a pull request.

### General
- [ ] Does this accomplish the issue you decided to work on?
- [ ] Does this overlap with any other issues without realizing it? If so:
    - [ ] Should they be in a separate pull request or not?

### Code
- [ ] Is this something you'd be content maintaining or can it be improved?
- [ ] Does it pass the linting tests (flake8)?
- [ ] Is there consistency and good flow from one part to the next?
- [ ] Could you explain every line you added if asked about it? Make sure you fully understand everything.

### Tests
- [ ] Have you written tests for the code? If not:
    - [ ] Did you create a blocking issue saying that this needs to be tested?
    - [ ] Could you write them yourself?
- [ ] Have you checked your code coverage to make sure most flows have been driven?

### Documentation
- [ ] Have you updated or added documentation? If not:
    - [ ] Did you create a blocking issue saying that this needs docs?
    - [ ] Could you write it yourself?
- [ ] Have you added docstrings to new functions/modules/classes?

### I've passed all of the above, it's time to submit
- [ ] Take note of all issues that your pull request addresses
- [ ] Rebase your changes onto the most current version of `devel`
- [ ] Do you need to do any last minute post-processing on your commits? (Last chance)
- [ ] Submit your pull request:
    - [ ] Specify issues to be closed
    - [ ] Reference any new issues that may be blocking
    - [ ] Give a short description of the changes made

### References
Inspiration comes from [this](https://gist.github.com/audreyr/4feef90445b9680475f2) checklist.
