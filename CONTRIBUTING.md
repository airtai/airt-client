# How to contribute

## How to get started

Before anything else, please install the git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:
```
nbdev_install_git_hooks
```

## Did you find a bug?

* Ensure the bug was not already reported by searching on GitLab under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

* Open a new GitLab merge request with the patch.
* Ensure that your MR includes a test that fails without your patch, and pass with it.
* Ensure the MR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## MR submission guidelines

* Keep each MR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each MR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such MRs and it most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already submitted MR into your development playground. If after you submitted MR, you discovered that more work is needed - close the MR, do the required work and then submit a new MR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submitted a MR and received a request for changes, you should proceed with commits inside that MR, so that the maintainer can see the incremental fixes and won't need to review the whole MR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the MR, do the work and then submit it again. Use common sense where you'd choose one way over another.

## Do you want to contribute to the documentation?

* Docs are automatically created from the notebooks in the notebooks folder.

