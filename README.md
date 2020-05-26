UNDER CONSTRUCTION

# Installing Git

There are a few options for using git to track a project. Behind all of them is the same command-based system that you're probably somewhat familiar with. Paired with a hosting option, a git-tracked project can extend those commands and its endless benefits to a team of any size. We'll be using GitHub to host ours.

There happens to be a desktop git solution made by Github and it doesn't suck, so we'll use that for now.

## [Github for Desktop](https://desktop.github.com/)

I recommend this route for now because:

- Graphical interface.
    
- We'll be using git with github specifically, and its a git app... from and for GitHub. (It's worth noting again the difference between git and git hosts like github. git is to github as porn is to pornhub. There are other options like Gitlab, Bitbucket, etc.)
    
- It's aimed at people new to git who want to do exactly what we're trying to do: open a project up to a small team for colloaboration.
    
- Eventually you might find yourself using git via commands in a terminal. When you do, you'll recognize a lot of the commands from using this app. While it combines and obscures them a little bit for ease-of-use, it does a good job of building familiarity nonetheless.
    
- Being a user-friendly git app designed to work with github, its the best possible intro to the three main topics:
    
    - Git (the system)
    - Repositories (the thing git works upon/with. We're making a repository for our mod.)
    - Remotes (hosted repositories)

# Getting Started

1. On this page, click 'Use this template' (pictured below) to start your own repository with the included tools, file-structure, and documentation to help jump-start collaboration on your mod:
![use-this-template.png](/docs/1-use-this-template.png)
* * *

2. Complete the process by filling in your details. Note the image below. Feel free to make the repo public, but it isn't neccessary. It can be private and you will still be able to collaborate with others. You can always change this setting later.
![from-template.png](/docs/2-create.png)
* * *

3. Click "Clone or download" in your new repository, and then "Open in Desktop" (If you're not using Github for Desktop and are unsure how to proceed, consider trying it for now):
![open-in-desktop.png](/docs/3-open-in-desktop.png)
* * *

4. Github for Desktop should open with the prompt shown below. The Repository URL field can be left as is. For Local Path, click "Choose..." to select a folder. (In the image below, I chose a folder called "projects". This is where the mod repo will be stored locally for you to work on):
![clone-repo.png](/docs/4-clone-repo.png)
* * *

5. Navigate to the folder you just chose. You will see a directory called "mod". Copy the contents of your mod (ex: anim, exported, scripts, modmain.lua, etc) into this folder. Then open Github for Desktop and you will notice that these additions are listed as Changes.
![clone-repo.png](/docs/5-insert-mod-see-changes.png)
* * *

6. At the bottom left, fill the summary field like below and then click 'Commit to master'. Congratulations! You've made your first commit to the repository, on the 'master' branch. 
![clone-repo.png](/docs/6-first-commit.png)
* * *

7. All thats left is to push this to Github. This last step is a moment to appreciate what git is about. It strives to capture & reflect the changes you made wherever the repo may be, while tolerating time & version discrepancies across the team. When it can't, it shines even then by recognizing it and prompting a project member to settle what it couldn't confidently. 

# Moving Forward

under construction
