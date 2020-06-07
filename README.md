<p align="center">
  <a href="" rel="noopener">
 <img src="img/banner/modstogether-banner.png" alt="moDSTogether"></a>
</p>



- [Installing Git](#installing-git)
  - [Github for Desktop](#github-for-desktop)
- [Getting Started](#getting-started)
- [Moving Forward](#moving-forward)
  - [Branches](#branches)
  - [Common Tasks](#common-tasks)
- [Tools](#tools)
  - [sumlua](#sumlua)
  - [modops](#modops)

## Installing Git

There are a few options for using git to track a project. Behind all of them is the same command-based system that you're probably somewhat familiar with. Paired with a hosting option, a git-tracked project can extend those commands and its endless benefits to a team of any size. We'll be using GitHub to host ours.

There happens to be a desktop git solution made by GitHub and it doesn't suck, so we'll use that for now.

### [Github for Desktop](https://desktop.github.com/)

I recommend this route for now because:

- Graphical interface.
    
- We'll be using git with Github specifically, and its a git app... from and for Gitub. (It's worth noting again the difference between git and git hosts like Github. Git is to Github as porn is to Pornhub. There are other options like Gitlab, Bitbucket, etc.)
    
- It's aimed at people new to git who want to do exactly what we're trying to do: open a project up to a small team for colloaboration.
    
- Eventually you might find yourself using git via commands in a terminal. When you do, you'll recognize a lot of the commands from using this app. While it combines and obscures them a little bit for ease-of-use, it does a good job of building familiarity nonetheless.
    
- Being a user-friendly git app designed to work with github, its the best possible intro to the three main topics:
    
    - Git (the system)
    - Repositories (the thing git works upon/with. We're making a repository for our mod.)
    - Remotes (hosted repositories)

## Getting Started

1. **Click 'Use this template'** (pictured below) to start your own repository with included tools, documentation, and file-structure to help jump-start collaboration on your mod.
   
   ![use-this-template.png](/img/gettingstarted/1-use-this-template.png)
* * *

2. **Finish creating your repository**. Note the image below. Feel free to make the repo public, but it isn't neccessary. It can be private and you will still be able to collaborate with others. You can always change this setting (as well as the name and description!) later on.

   ![from-template.png](/img/gettingstarted/2-create.png)
* * *

3. **Click "Clone or download"** in your newly generated repository, and then **"Open in Desktop"**.
    
    ![open-in-desktop.png](/img/gettingstarted/3-open-in-desktop.png)
* * *

4. **Click "Choose..." to select a folder** when Github for Desktop prompts you. In the image below, I chose a folder called *projects*. This is where the mod repo will be stored locally for you to work on.

   ![clone-repo.png](/img/gettingstarted/4-clone-repo.png)
* * *

5. **Copy the contents of your mod** (ex: anim, exported, scripts, modmain.lua, etc) into */mod*. Then open Github for Desktop and you will notice that these additions are listed as Changes.
   
   ![clone-repo.png](/img/gettingstarted/5-insert-mod-see-changes.png)
* * *

7. **Type a commit message** then click **Commit to master**. Congratulations! You've made your first commit to the repository. It contained the addition of you mod files, and it established the **master branch**.

    ![clone-repo.png](/img/gettingstarted/6-first-commit.png)
* * *

8. All thats left is to push this to Github. This last step is a moment to appreciate what git is about, and the job its being tasked with. It will strive to capture & reflect the changes you made wherever the repo may be, while tolerating time & version discrepancies across the team. When it can't, it shines even then by recognizing it and prompting a project member to settle what it couldn't confidently. 

## Moving Forward

### Branches
![](/img/branches/master-development-feature.png)

Right now, our repository is based soley in one branch: the *master* branch. We are going to use a workflow strategy based on one called Gitflow as we move forward.

In our *master* branch, we have the supporting items from moDSTogether and our mod, which idealy is in a state that reflects its most recent release. Its okay if not, but from here on the history of the *master* branch will be akin to a history of our releases to the Steam Workshop. Many commits to the repository will be made between and up to releases, but we won't be commiting them all directly to our central branch. 

We are going to create another branch immediately, based on the *master* branch called the *development* branch. When accumulative commits in this *development* branch warrant or represent a public update to the mod, it will merge back into the *master* branch, rolling in all the changes that make up the new release. This is how the *master* branch will remain symbolic of new versions in the SteamWorkshop.

To keep things simple, we could say that development is going to involve adding new features, bug-fixes, and various other miscellaneous changes. When we want to get started on one of these, like adding a cool new item to the mod, we're going branch off of *development* with a short-lived but useful branch called something like: *cool-new-item*. When the new item is finished, it will be merged back into *development* (which makes it destined for the next release).

Consider these example patchnotes:

```
v0.7 "The Cool Stuff Update"
   - added the cool new item 
   - fixed a bug where items weren't rendering as cool as intended
   - added cool new skins for the cool new item
```

The first line would mirror a node in the commit history of our *master* branch. A version update.

The items below would represent those of our *development* branch, which contains the rolled-up work completed over the lives of our splintering feature branches, like *cool-new-item*. Commits in those feature/fix/change branches are just bread-and-butter git commits, which are not symbolic of anything in particular; they just represent progress for the dev working in the branch and the dev decides their nature when they enter their **commit message** with each one.

If we only used one branch (called a centralized strategy), all commits would be like those I just described. But, in the interest of organization, project-manageability, easier collaboration and effective use of git just generally, we employed some others.


### Common Tasks


## Tools

### [modops](tools/modops/README.md)

### [sumlua](tools/sumlua/README.md)
- Simple lua --> spreadsheet converter that summarizes functions with columns for *Name*, *Parameters*, and *Scope*.
- Useful for making cheatsheets and pulling back the veil on Don't Starve Together's API.
- See output from consolecommands.lua & debugcommands.lua in /examples for good use-cases.

   **NOTE:** *consolecommands.csv & debugcommands.csv (found in tools/sumlua/examples) refer to and contain extracts of material created & owned by Klei Entertainment. No copyright infringement intended, will swiftly remove on request.*


