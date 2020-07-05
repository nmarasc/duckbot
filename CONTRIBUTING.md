# Contributing to Duckbot

If you're here because you want to contribute to this project, whether that be new code, reporting a bug, or requesting a new feature, you've come to the right place and your desire to help is appreciated.

### Why it Matters
---
Following these guidelines, while not required, is very helpful in getting your contributions reviewed and accepted faster with less work. Help your fellow contributors help you by making their job easier and they should do the same in return.

### What Kind of Contributions are Needed
---
Currently any and all contributions are encouraged. New functionality, enhancements, bug fixes and documentation updates are just a few examples of things you can help with. Bug reports and feature suggestions will always be welcome additions.

### Things to Keep in Mind
---
Before getting into technical details it should be noted that this project has adopted the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct, which you can view [here.](CODE_OF_CONDUCT.md)
This code of conduct describes the behaviors and attitudes deemed acceptable in order to create and maintain a welcoming and encouraging environment for all. Laid out are also the repercussions for violating the code of conduct and how issues will be reported and dealt with.

Your technical responsibilities are as follows:
* Keep it simple. While sprawling and complicated modules are bound to happen and sometimes be unavoidable, it's best to separate pieces when things start to get complex or when they are no longer closely related. This will reduce the overall technical debt of the project by keeping the individual parts simple and easy to maintain for yourself and others.
* Tests are key. Make sure to write unit tests for your code before submitting it for review. If things are properly tested it will reduce the number of bugs that get through into production, which means less things you'll have to come back and fix later when you've forgotten what you wrote.
* Make use of linting tools to adhere to code and documentation style standards. This will ensure that the codebase maintains some amount of appearance continuity, which helps tremendously with readability and flow. [Flake8](https://gitlab.com/pycqa/flake8) is a code style enforcement tool that will be run during the integration pipeline, so you can save yourself a failed submission by running it yourself before putting in a pull request or installing it as a git hook.
* Are you truly done? Does your submission meet the suggested requirements for being done in [this](AM_I_DONE.md) checklist?
* While this project is primarily developed on and for Linux, platform agnostic code is key in order to maximize usability.

### How Do I Start Contributing?
---
If you made it this far you either skipped ahead (shame) or decided all of the above is acceptable and you are ready to get started. Thank you for taking interest in improving the project directly. The next thing to ask is how are you looking to contribute?

#### I Want to Code

Great, the first step is going to be deciding which item you'd like to work on. If you're new to the project or even programming in general a good place to look would be [this](https://gitlab.com/nmarasc/duckbot/issues?label_name[]=Quick+Fix) issues page. Any issue found here should be relatively simple to complete. Given that nobody is perfect, some things will be missed or labeled incorrectly, so it never hurts to ask questions if something seems easier or harder than is labeled and it can then be adjusted accordingly.

Now that a work item has been chosen your development environment needs to be set up, that process will change depending on the platform you plan to develop from.

Linux:
!!TBD!!

Windows:
!!TBD!!

Mac:
!!TBD!!

Now that your environment is set up you should be all set to start hacking away at the issue(s) you've chosen. Once you think you've finished go through things one more time with [this](AM_I_DONE.md) checklist and then open your pull request. Your work will be reviewed and run against the test suite, which should include your new tests. If everything passes review and testing then it will be merged into the devel branch and the associated issues will be closed.

A few commit tips:
* Commit early and often. A suggestion made by many people before that will make finding problems and correcting them far easier on yourself. The more checkpoints you have, the more accurately you can pin down where things went wrong.
* Include issue numbers in your commit title. Adding the issue number to the first line of your commit will help catch when your changes start to deviate from what you originally set out to do.
* Try to keep the first line of your commit message under 70 characters. This makes oneline formatting of commit messages look nicer and keeps titles concise.

If you're new to contributing to open source feel free to check out [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github) for a pretty detailed guide on a lot of the steps required. That guide is GitHub specific and not perfectly up to date, but the techniques learned there should be applicable to this project. As always, questions are welcome if things aren't clear enough.

#### I Want to Report a Bug

First and foremost if there is a defect related to security (e.g. having access to something that you're not supposed to) do not open an issue for it. Instead, contact a maintainer directly and let them know. If you aren't sure whether something is a security issue or not it is better to err on the side of caution, let a maintainer know and they will decide.

Next, check to make sure there isn't already an issue related to your discovery. Somebody may have beat you to it, but it's possible that you can fill in some information or offer new insight.

If you have determined that this is not a security issue and there is no outstanding issue then all you need to do is open a new issue, select the Bug template and then fill in as many of the fields with as much detail as you are able.

#### I Want to Suggest a Feature

The main purpose of Duckbot is to provide commands and tools to discord users and admins through a chat interface in order to create and maintain a more fun environment. All of that is an elevator pictch way of saying that the sky is the limit when it comes to new features as long as you think it would be something fun for people to have or useful to them as a tool. New suggestions for features should do their best to align with these goals. This does not mean that tangential ideas will be outright rejected but they will require more consideration and discussion.

With that in mind, if you would like to submit your feature request then you may open a new issue with the Feature template and fill out the information there.

### Code Reviews
---
Whenever a pull request is made, the code, tests, and documentation need to be reviewed for accuracy and quality. At least one maintainer will need to review and approve the changes before they can be merged, but it is encouraged that many people give their opinion on a change. While code reviews can be intimidating and, speaking from experience, a little embarassing when you leave in a simple mistake that you didn't notice, it is a crucial skill to develop on both ends of the process.

Currently, live code reviews are not being held, nor are there plans to. If the project grows or there becomes an interest in such a thing, then the idea will be entertained and explored.

Remember to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) when giving the results of your review. Belittling, making fun of, or harassing others will not be tolerated. We all make mistakes and have things that we don't fully understand. Getting things wrong and learning from them is one of the best ways to improve your abilities, so don't ruin that for others by being disrespectful.

### Community
---
For now there is no external communication platform for this project, but a Gitter community could be created should the need arise.

When a maintainer is cc'd on an issue or otherwise contacted, you should be able to expect a reply within 2-3 business days at most, but usually within 24 hours.
