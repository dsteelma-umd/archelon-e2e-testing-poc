# Archelon End-to-End Testing Proof-of-Concept

## Introduction

This is a proof-of-concept for using [Playwright](https://playwright.dev/) for
end-to-end tests for [Archelon](https://github.com/umd-lib/archelon).

It also discusses using the "behave" Behavior-Driven Development (BDD)
testing framework to write acceptance tests, versus simply using "pytest".

## Useful Resources

* Playwright - <https://playwright.dev/>
* pytest - <https://pytest.org>
* Gherkin syntax - <https://cucumber.io/docs/gherkin/reference/>
* behave - <https://behave.readthedocs.io/en/stable/>

## Proof-of-concept Setup (Local Workstation)

A development environment can be set up on a local workstation using the
following steps:

1) Clone the repository and switch into the directory:

    ```zsh
    $ git clone git@github.com:dsteelma-umd/archelon-e2e-testing-poc
    $ cd archelon-e2e-testing-poc
    ```

2) Set up the Python environment:

    ```zsh
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -e '.[test]'
    ```

3) Install the browsers used by Playwright:

    ```zsh
    $ playwright install
    ```

## Proof-of-concept Setup (Docker)

An alternative Docker-based environment can be set up using the following steps.

### Prerequisites

In order for the web browser to be displayed from Docker, the "XQuartz" X11
desktop environment needs to be installed on the local workstation:

Preq. 1) Install XQuartz on the host machine using Homebrew:

```zsh
$ brew install --cask xquartz
```

Preq. 2) Run XQuartz:

```zsh
$ open -a XQuartz
```

Preq. 3) In XQuartz, go to XQuartz | Preferences, then the “Security” tab,
         check the “Allow connections from network clients” to select it.

Preq. 4) Exit XQuartz and restart:

```zsh
$ open -a XQuartz
```

Preq. 5) Verify that XQuartz has opened port 6000:

```zsh
$ netstat -an | grep -F 6000
tcp4       0      0  127.0.0.1.6000         127.0.0.1.50769        ESTABLISHED
tcp4       0      0  *.6000                 *.*                    LISTEN
tcp4       0      0  127.0.0.1.50769        127.0.0.1.6000         ESTABLISHED
tcp6       0      0  *.6000                 *.*                    LISTEN
```

Preq. 6) Test that a Chrome browser can be opened from a Docker container

```zsh
$ export DISPLAY=:0
$ xhost +localhost
$ docker run --rm \
             -e DISPLAY=host.docker.internal:0 \
             -v /tmp/.X11-unix:/tmp/.X11-unix \
             mcr.microsoft.com/playwright npx -y playwright open google.com
```

### Application Setup

1) Run XQuartz, if it is not running.

2) Allow XWindow connections from localhost:

    ```zsh
    $ xhost +localhost
    ```

2) Clone the repository:

    ```zsh
    $ git clone git@github.com:dsteelma-umd/archelon-e2e-testing-poc
    $ cd fcrepo-e2e-testing
    ```

3) Open the folder containing the clone in VS Code. When prompted, reopen the
   folder in a Dev Container.

4) Run the following to install the dependencies:

    ```zsh
    $ pip install -e '.[test]'
    $ playwright install-deps
    $ playwright install
    ```

## Authentication

Archelon requires a valid CAS login to access the application.

Playwright enables the browser state from a logged-in session to be stored and
reused in the tests.

To set up the browser state:

1) Run the "create_auth_state.py" script:

```zsh
$ python create_auth_state.py
```

This will start a Chromium browser, which will go to
<https://archelon-test.lib.umd.edu> and then immediately redirect to CAS. A
"Playwright Inspector” window will also be displayed.

2) Log in to CAS. After a successful login and with the Archelon home page again
displayed, left-click the “Resume” button in the “Playwright Inspector” window
The current browser start will be stored in the `playwright/.auth` subdirectory.

## BDD Tests

Some behavior-driven development (BDD) tests, using the
"[behave](https://github.com/behave/behave)" framework have been provided.

The BDD tests are defined using the Gherkin "Given-When-Then" format in
"*.feature" files in the "features" subdirectory. Python code implementing
the actual steps in the "features/steps" subdirectory.

To run these tests:

```zsh
$ behave
```

By default, the tests run in the browser's "headless" mode, meaning that it
is not displayed.

The following custom configuration properties are available to control the
tests:

* `headed` - Displays the browser when running the tests
* `slow_mo` - Slows down browser execution by the given multiple.

For example, to run the tests and display the browser:

```zsh
$ behave -D headed
```

To slow down the execution of the tests by 500 times without the displaying the
browser:

```zsh
$ behave -D slow_mo=500
```

To slow down the execution of the tests by 500 times and display the browser:

```zsh
$ behave -D headed -D slow_mo=500
```

To focus on a particular scenario,  tag the scenario (in the ".feature" file),
with the `@wip` tag, then run the following command:

```zsh
$ behave --wip -D headed
```

Running with the "--wip" flag also enables the interactive Python debugger to
be accessed simply by placing a `breakpoint()` in the relevant step.

## BDD Test Status

The BDD tests run against the Archelon test server
(<https://archelon-test.lib.umd.edu/>), and so are reliant on it being in an
expected configuration. When running the BDD tests using "behave" all the
features should pass, with the following summary output:

```text
2 features passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 2 skipped
21 steps passed, 0 failed, 2 skipped, 0 undefined
```

Two of the scenarios are marked as "skipped" because they both rely on the step
`'the item appears in OAI-PMH queries'` in
`features/steps/test_publish_workflow.py` that could not be implemented because
the "digital-test.lib.umd.edu" server does not provide an OAI-PMH server.

This ability to "skip" steps illustrates that "behave" can be used to specify
tests prior to development, with the "skipped" results providing an objective
measure of progress toward completion.

## Non-BDD pytest tests using Playwright

Some tests using Playwright from within pytest are in the "tests" subdirectory.

To run these tests:

```zsh
$ pytest
```

By default, the tests run in the browser's "headless" mode, meaning that it
is not displayed.

The following custom configuration properties are available to control the
tests:

* `headed` - Displays the browser when running the tests
* `slow_mo` - Slows down browser execution by the given multiple.

For example, to run the tests and display the browser:

```zsh
$ pytest -headed
```

To slow down the execution of the tests by 500 times:

```zsh
$ pytest -slow_mo=500
```

To slow down the execution of the tests by 500 times and display the browser:

```zsh
$ pytest -headed -slow_mo=500
```

## pytest Test Status

The pytest tests run against the Archelon test server
(<https://archelon-test.lib.umd.edu/>), and so are reliant on it being in an
expected configuration.

All the tests should pass.

## Goal of End-to-End Testing

For purposes of this evaluation, the main goal of end-to-end testing is to be
able to verify that the system in a production (or production-like) environment
is working as expected, at least for those aspects that are of most concern to
stakeholders.

End-to-end tests are not intended to replace lower-lever unit or integration
tests. Instead, end-to-end tests provide "black-box" testing of an application
through its user interface.

The maximalist goal (likely not achievable, but worthwhile as a thought
experiment) would be to have enough automated tests (unit, integration and
end-to-end) so that an application could be deployed to production based solely
on passing all automated tests.

Some more modest goals would be:

* Provide some level of regression testing, to verify that behavior of existing
  functionality
* Alleviate/mitigate some of the manual testing that is done for each production
  release

## Areas of Evaluation

Two main areas of evaluation were performed:

1) Testing the viability of the "Playwright" tool for end-to-end testing
2) Using Behavior-Driven Development (BDD), particularly the "Given-When-Then"
   syntax for describing end-to-end tests, and the "behave" testing framework.

These areas are "orthogonal" to one another, in that each can be used
separately from the other, or in combination.

## Evaluation Thoughts

### General Issues

1) Logging in to a CAS-enabled application is a manual process.

   Because UMD DIT requires multi-factor authentication (MFA) on all CAS
   accounts, creating the browser state with appropriate authentication
   credentials is a manual process (and needs to use a particular user's
   credentials).

   A support request is in with DIT to see it if is possible to have test
   accounts without the MFA requirements, to enable automated execution of the
   tests, such as through a continuous integration system such as Jenkins.

2) For testing, probably want a deterministic fcrepo setup, i.e., one in which
   the UUIDs for particular records are stable. Otherwise there may be a lot of
   extra work finding the "correct" page when setting up and running tests.

   Also want a reproducible environment, because some of the end-to-end tests we
   want to do may add or delete items from fcrepo.

   Need additional investigation on how to setup an fcrepo test environment
   that:

    * Can be easily updated as development progresses
    * Provides "stable" UUIDs to make accessing specific items simpler

3) "Destructive" operations that change the state of an item are not necessarily
   trivial to reverse. When unit testing, we can usually just wrap the test in
   a database transaction, and then roll back the transaction at the end of it.
   With end-to-end testing, that is not a option, so need to be careful to
   revert the affects of a test at the end (or design the tests in such a way
   that the changes don't matter to other tests, such as by using different
   items for different tests).

4) End-to-end tests are traditionally slow, fragile (may fail due to
   non-obvious changes to the application), brittle (can be difficult to
   change), and difficult to set up. This is all still largely true, somewhat
   mitigated by the following:

   * Playwright seems fairly fast, especially when running in "headless" mode
   * Playwright can be run parallel (requires the use of the "pytest-xdist"
     plugin). This was not tested as part of this evaluation. Parallel execution
     would impact on how the tests are designed so the timing and order of
     execution doesn't impact th results.
   * Careful use of Playwright locators may help with the dealing with changes
     to the application GUI. However, we might be limited here by the underlying
     Blacklight application on which Archelon in built.
   * Playwright can be used with the Python breakpoint() to provide am
     interactive console for debugging failing tests.

### Playwright

Playwright is fairly straightforward to use, once you have a few examples in
place to guide you. Playwright has a number of nice features:

* Can handle file downloads
* Has a "recorder" functionality
* Integrates nicely with Python breakpoint()
* Fairly easy to set up
* Downloads its own set of browsers, so is "batteries included"

## Behavior-Driven Development (BDD)

From [Wikipedia](https://en.wikipedia.org/wiki/Behavior-driven_development):

> BDD is a process by which DSL structured natural language statements are
> converted to executable tests. The result are tests that read like acceptance
> criteria for a given function.

The BDD concept of having executable implementation-agnostic descriptions of
application functionality is very attractive for two reasons:

* It is "living" documentation, in non-technical language, of the application
  functionality.
* In theory, the "Given-When-Then" feature files can be written by non-technical
  stakeholders, ideally in advance of development.

For proponents, the emphasis is not on using BDD as a testing tool. Instead,
the main benefit from using BDD comes from the conversations it engenders
between the different stakeholders, and the codifying of decisions that are
made into executable form, that can then be easily reviewed.

### Python and BDD

Both of the major Python BDD testing frameworks ("behave" and "pytest-bdd")
separate the separate each "Given-When-Then" step in a feature file into
individual functions. This is intended to promote reuse of
steps across tests, but has the following issues:

* The sheer number of individual functions may feel overwhelming, and difficult
  to comprehend in the context of a particular test, especially when the steps
  are not neatly presented as a linear list of steps in the file.

* The sharing of context between steps can be opaque, especially as steps are
  reused in multiple tests. For example, the "behave" framework passes a
  "context" dictionary between steps, which any value can be added to, as
  needed. However,  unless you trace the execution through every step, it is not
  clear what the   contents of the "context" dictionary might be (and code
  completion can't help).

* Enabling the reuse of steps across tests requires a fairly rigid/formal way
  of writing the feature files, which may be unnatural for non-technical
  writers.

### behave BDD Framework

The biggest issue with "behave" is that it is a completely separate testing
framework from pytest, so there is sometimes a cognitive dissonance when
writing the tests.

Additionally, the separation of the Gherkin "Given-When-Then" steps into
separate functions, which is intended to promote reuse, takes some getting
used to, as does the fact that all the "state" for the particular test must be
passed through the "context" object, so naming things is important. That you
can't get source code completion for custom keys in the context object is
significant.

The VS Code "Cucumber" plugin (cucumberopen.cucumber-official) can help
with the initial test step setup (i.e., mapping a "Given-When-Then" in a
feature file to a Python function), but there are occasional hiccups, such
as when generating steps that have single quotes in them -- "behave" does not
always recognize the generated steps.

## Evaluation Conclusions

### End-to-end Testing

Manual execution of end-to-end tests is feasible, and potentially
extremely valuable for projects like Archelon, which have so many moving parts,
that must work in combination.

Current major blockers:

* Setting up a reproducible Archelon test environment with stable UUIDs
* Identifying which functionality is best tested using end-to-end tests, versus
  less expensive methods such as unit or integration tests.

Automated execution of end-to-end tests, such as via a continuous integration
platform, is currently blocked by the issue of user credentials and CAS.

### Use of Playwright

Playwright seems fairly easy to use (especially with code completion), and has
many useful features. Setup of the tool in a local development environment (or
local Docker-based environment) is straightforward.

Setting up the tool in a continuous integration (Docker) environment can also
likely be done without too much difficulty, at least for "headless" runs.
Enabling "headed" runs, or runs where screenshots/videos are produced may be
slightly more difficult.

If we want to pursue end-to-end testing, Playwright seems like a good web
automation tool to facilitate that.

### Behavior-Driven Development

The behavior-driven development process provides the most benefit when used to
facilitate collaboration, rather than as a mere testing tool. Ideally, this
means that:

* the "Given-When-Then" feature files are mainly written and "owned" by
  the Scrum Lead or Product Owner
* Are written *before* a feature is implemented by developers
* Contains sufficient detail to capture all the expected workflows, in an
  implementation-agnostic description

Some of the obstacles:

* Writing good feature files is an art form, and may not come naturally
* The feature files would need to be periodically reviewed and updated by the
  Scrum Lead or Product Owner (especially if developers have been modifying them
  to better fit into existing test steps).
* End-to-end tests are traditionally the most expensive kind of tests to write,
  run, and maintain, so we may wish to be circumspect about how many we create.
  If something can be implemented reliably as a lower-level unit or integration
  test, that should be preferred.

Recommendation would be to *not* use Behavior-Driven Development at this point
in time, as the overhead may simply be too high.

One possible path toward BDD, without committing us unduly, would be to try to
rewrite the existing acceptance testing documentation in Confluence using the
"Given-When-Then" format, and then use those to facilitate writing acceptance
tests using Playwright and pytest. This may provide enough experience to
demonstrate whether going to a full BDD process using a framework like
"behave" is worthwhile.
