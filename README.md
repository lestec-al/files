# Python-file-explorer(with git) develop by OSS-TEAM-13

<p align="center">
<a href="https://fixed-borogovia-5fe.notion.site/OSS-Team-13-4df2df4655c645a8a7e49e15abbffa3c">
<img src="https://img.shields.io/badge/NOTION-team_page-green?&style=for-the-badge&logo=notion">
</a>
</p>

## Index

- [Project Description](#Project-Description)
- [Installation Guide](#Installation-Guide)
- [Function design and description(v1.0)](#Function-design-and-description(v1.0))
- [Function design and description(v2.0)](#Function-design-and-description(v2.0))
- [Team Information](#Team-information)
- [About Collaboration](#About-Collaboration)
- [Copyleft / End User License](#copyleft--end-user-license)

## Project Description

This project is a git file browser project that has been expanded by adding Git-related functions to file browsing.

Provides file browsing function by default and provides the following functions.

- `git init`
- `git add`
- `git commit`
- `git rm ` && `git rm --cached`
- `git restore` && `git restore --staged`
- `git mv`
- `git clone from github`

In branch menu we provides with GUI

- `git branch actions(create, delete, rename, checkout, merge)`
- `Commit history about current branch`

In addition to these features, it displays the file status (4 types) according to Git status as an image!

Also It displays git commit history(in branch menu) and more specific information when click commit objects.

More specific information, You can check information in <b>Function design and description</b> tab.

## Installation Guide

### Needs for running

```bash
Python 3.8+
pip (package installer for Python)
platform : mac OS
```

- Installation

```bash\
git clone https://github.com/CAU-OSS-project-practice/OSS-file-manager.git
cd OSS-file-manager
pip install -r requirements.txt
python3 files_new.py
```

- Operate in virtual environment in case of tkinter library error or python version conflict

```bash
python -m venv .venv # .venv crete
source .venv/bin/activate # Run virtual environment
```

- Disable virtual environment

```bash
deactivate
```

## Function design and description(v1.0)

> All photos can be viewed as enlarged images when clicked.😀

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>File browser function </b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rootdir.png"><img src="/data/execution_image/rootdir.png" width="100%" height="100%">
					</a><br><br> File search starts at the root directory
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/in%20folder.png"><img src="/data/execution_image/in folder.png" width="100%" height="100%"></a><br><br>All files and directories contained in the current directory are represented by icons, names, and extensions. </h4></td>
            <td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/double-click.gif"><img src="/data/execution_image/double-click.gif" width="100%" height="100%"></a><br><br>Browsing via double click </h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git init Feature </b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
<img width="804" alt="git_init_not_git_repo" src="https://github.com/rbgksqkr/react/assets/63959171/ce081f1c-5bf2-4e15-9b47-510bc62a891c">
					</a><br><br>If the directory is not a Git repository -> Activate the init button
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
                      <img width="804" alt="git_init_git_repo" src="https://github.com/rbgksqkr/react/assets/63959171/709a75ea-e70f-43dd-8165-0cbb3f49b41d">
            </a><br><br>For directories that are already Git repositories -> disable init button</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=4>
				<br>
				<b>Show file status according to Git status</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="25%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file_staged.png"><img src="/data/icon_file_staged.png" width="100%" height="100%">
					</a><br><br>Show staged files
				</h4>
			</td>
			<td width="25%">
	   			<h4 align="center">
		   		<a href="https://github.com/CAU-OSS-project-practice/OSS-file-manager/blob/develop/data/icon_file_unstaged.png?raw=true"><img src="/data/icon_file_unstaged.png" width="100%" height="100%"></a><br>Show unstaged (modified) files<br></h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file.png"><img src="/data/icon_file.png" width="100%" height="100%"></a><br><br>Show committed (unmodified) files</h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file_both.png"><img src="/data/icon_file_both.png" width="100%" height="100%"></a><br><br>Show staged-unstaged (modified) files</h4></td>
		</tr>
</tbody>
</table>
Stage is divided into 4 types.

1. Staged
2. unstaged (modified)
3. committed (unmodified)
4. staged - unstaged (when a file is changed in the staged state)

Untracked - Staged files ex) When executing the git rm --cached command, untracked is made to work as a priority.

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Git add Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
          <img width="804" alt="git_add_before" src="https://github.com/rbgksqkr/react/assets/63959171/514aaa4d-1245-4c3c-9b55-1f34f023e8d5">
					<br><br>before file selection
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
				<img width="804" alt="git_add_one" src="https://github.com/rbgksqkr/react/assets/63959171/6938733f-a031-4093-8bd8-feaff368b5f9">
					<br><br> When one file is selected, only that file can be added.
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
		   		<img width="804" alt="git_add_all" src="https://github.com/rbgksqkr/react/assets/63959171/b8b24523-a693-466e-8962-4a3d4f41daae">
            <br><br>If no files are selected, git add . movement</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git commit Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
<img width="804" alt="git_commit_show_staged_list" src="https://github.com/rbgksqkr/react/assets/63959171/487c96fb-7094-4427-af14-aa05d3cd05da">
          <br><br>shows the list of staged changes
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
<img width="804" alt="git_commit_message" src="https://github.com/rbgksqkr/react/assets/63959171/860d5f44-ff43-40c9-b30a-37d7765bef86">
            <br><br>writing commit message via GUI</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git restore Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_after.png"><img src="/data/execution_image/git_restore_after.png" width="100%" height="100%"></a><br><br>Before Git restore works (shows modified files)</h4></td>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_before.png"><img src="/data/execution_image/git_restore_before.png" width="100%" height="100%">
					</a><br><br>After git restore works (return to pre-commit state)
				</h4>
			</td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git restore --staged Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_before.png"><img src="/data/execution_image/git_restore_staged_before.png" width="100%" height="100%">
					</a><br><br>Git restore --staged before operation (staging files)
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_after.png"><img src="/data/execution_image/git_restore_staged_after.png" width="100%" height="100%"></a><br><br>git restore --staged Return staged files to modified state</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git rm Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_before.png"><img src="/data/execution_image/rm_after.png" width="100%" height="100%">
					</a><br><br>git rm before
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_after.png"><img src="/data/execution_image/rm_after.png" width="100%" height="100%"></a><br><br>git rm after(Deleted and deleted facts from directory are staged) </h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git rm --cached Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm%20_cached_before.png"><img src="/data/execution_image/rm _cached_before.png" width="100%" height="100%">
					</a><br><br>git rm --cached before
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_cached_after.png"><img src="/data/execution_image/rm_cached_after.png" width="100%" height="100%"></a><br><br>git rm --cached after -> Not deleted from real directory, but deleted (untracked) from git repository</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git mv Feature</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
  <img width="804" alt="git_mv_open_mv_window" src="https://github.com/rbgksqkr/react/assets/63959171/eb0b1047-049b-484a-9a06-e3807984fe8d">
          <br><br>Write file name to change
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
<img width="804" alt="git_mv_rename" src="https://github.com/rbgksqkr/react/assets/63959171/30fd2f03-2777-455e-80df-dfcda1f428c0">
            <br><br>file name change</h4></td>
		</tr>
</tbody>
</table>


## Function design and description(v2.0)

> All photos can be viewed as enlarged images when clicked.😀  

New Feature has updated.

1. We updated basic Git branch associated action(Create, Delete, Rename, Checkout).
2. We updated Git merge action
3. And We can also check Git commit history
3. Git clone from Github

Feature 1 , 2 and 3 can be activated through the Branch Menu button.  
Feature No. 3 was implemented by adding a button to the place where v1.0's git-related actions were gathered.  
### <b>Feature 1. Branch Associated Action </b><br>
<table><tbody>
		<tr>
			<td colspan=2>
				<b>Branch Create Feature </b><br>
                <br>it asks the user to enter a branch name and then creates a branch with the name
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://file.notion.so/f/s/0e22ab4d-c27a-4ed3-8cc5-2c094316df7d/Untitled.png?id=4812bd65-1755-48ba-9407-deee0846aa1c&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058882740&signature=xnZqRSNU1BTR6-0axEvWEomkl1YZsgKsE7FbUAtA1Dg&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/0e22ab4d-c27a-4ed3-8cc5-2c094316df7d/Untitled.png?id=4812bd65-1755-48ba-9407-deee0846aa1c&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058882740&signature=xnZqRSNU1BTR6-0axEvWEomkl1YZsgKsE7FbUAtA1Dg&downloadName=Untitled.png" width="100%" height="100%">
					</a><br><br> Ask the user to enter a branch name
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://file.notion.so/f/s/2a6f6adb-5619-4d5b-9d1b-3b08377c1a42/Untitled.png?id=ed2a5efa-ea20-4608-bc8f-3f7eaa2ba896&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058735880&signature=4G7wEtXBo4dvY805iw8VOVUG2LhIiW7QFk8yAdXI9Ho&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/2a6f6adb-5619-4d5b-9d1b-3b08377c1a42/Untitled.png?id=ed2a5efa-ea20-4608-bc8f-3f7eaa2ba896&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058735880&signature=4G7wEtXBo4dvY805iw8VOVUG2LhIiW7QFk8yAdXI9Ho&downloadName=Untitled.png" width="100%" height="100%"></a><br><br>Branch has Created in Branch List </h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Git Delete Feature </b><br>
				<br> it shows the list of branches, asks the user to select one of them, and deletes the selected one
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/2a6f6adb-5619-4d5b-9d1b-3b08377c1a42/Untitled.png?id=ed2a5efa-ea20-4608-bc8f-3f7eaa2ba896&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058735880&signature=4G7wEtXBo4dvY805iw8VOVUG2LhIiW7QFk8yAdXI9Ho&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/2a6f6adb-5619-4d5b-9d1b-3b08377c1a42/Untitled.png?id=ed2a5efa-ea20-4608-bc8f-3f7eaa2ba896&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686058735880&signature=4G7wEtXBo4dvY805iw8VOVUG2LhIiW7QFk8yAdXI9Ho&downloadName=Untitled.png" width="100%" height="100%"></a>
                <br><br>Shows the list of branches in Branch list GUI
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
                      <a href="https://file.notion.so/f/s/e5600bbe-c797-4851-b0fe-9af669c4f690/Untitled.png?id=6d765431-88d3-4b5b-8f35-ac8ab9af4b6e&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059069786&signature=EyZ8Q8OkTM3hkTsbGUJAbLwudzUpDrqt2HbaifjDYHg&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/e5600bbe-c797-4851-b0fe-9af669c4f690/Untitled.png?id=6d765431-88d3-4b5b-8f35-ac8ab9af4b6e&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059069786&signature=EyZ8Q8OkTM3hkTsbGUJAbLwudzUpDrqt2HbaifjDYHg&downloadName=Untitled.png" width="100%" height="100%"></a><br><br>Ask the user to select one of them</h4></td>
            <td width="33%">
	   			<h4 align="center">
                      <a href="https://file.notion.so/f/s/386e46fc-12bc-4d87-ac31-c66af8adecbf/Untitled.png?id=2f8df168-bfc9-4a27-b393-ee92843509ea&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059199235&signature=K5Z6SuRg9xCjBvzKEzwN-ouacHsuwGvjAGJNhQnQQdA&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/386e46fc-12bc-4d87-ac31-c66af8adecbf/Untitled.png?id=2f8df168-bfc9-4a27-b393-ee92843509ea&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059199235&signature=K5Z6SuRg9xCjBvzKEzwN-ouacHsuwGvjAGJNhQnQQdA&downloadName=Untitled.png" width="100%" height="100%"></a><br><br>branch has deleted</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Git Rename Feature </b><br>
				<br> it shows the list of branches, asks the user to select one of them and to enter a new name, and renames the branch.
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/386e46fc-12bc-4d87-ac31-c66af8adecbf/Untitled.png?id=2f8df168-bfc9-4a27-b393-ee92843509ea&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059199235&signature=K5Z6SuRg9xCjBvzKEzwN-ouacHsuwGvjAGJNhQnQQdA&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/386e46fc-12bc-4d87-ac31-c66af8adecbf/Untitled.png?id=2f8df168-bfc9-4a27-b393-ee92843509ea&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059199235&signature=K5Z6SuRg9xCjBvzKEzwN-ouacHsuwGvjAGJNhQnQQdA&downloadName=Untitled.png" width="100%" height="100%"></a>
                <br><br>Shows the list of branches in Branch list GUI
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
                      <a href="https://file.notion.so/f/s/0254bdab-2fba-4191-b9b8-911e73384dca/Untitled.png?id=0c6046c9-b509-47ee-b73a-f8bfcf0df534&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059647933&signature=bYVj81ZeC8X61Z-izQXgrRU8p00TTZVaBk9_75aMLS0&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/0254bdab-2fba-4191-b9b8-911e73384dca/Untitled.png?id=0c6046c9-b509-47ee-b73a-f8bfcf0df534&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059647933&signature=bYVj81ZeC8X61Z-izQXgrRU8p00TTZVaBk9_75aMLS0&downloadName=Untitled.png" width="100%" height="100%"></a><br><br>Ask the user selected branch to enter a new name</h4></td>
            <td width="33%">
	   			<h4 align="center">
                      <a href="https://file.notion.so/f/s/7f08e346-a7ba-4e99-82eb-c2eb5009282a/Untitled.png?id=dd14e4d3-fc0c-4e70-89a2-e03fc94d2084&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059651254&signature=W5oXQQxoVldNtIcgDBq1-nMOFHnDpVVUT4qI4vXQl64&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/7f08e346-a7ba-4e99-82eb-c2eb5009282a/Untitled.png?id=dd14e4d3-fc0c-4e70-89a2-e03fc94d2084&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686059651254&signature=W5oXQQxoVldNtIcgDBq1-nMOFHnDpVVUT4qI4vXQl64&downloadName=Untitled.png" width="100%" height="100%"></a><br><br>branch has renamed</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Git Checkout Feature</b><br>
				<br>it shows the list of branches, asks the user to select one of them, and checkout the branch.
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                 <a href="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060445261&signature=-sNhV47ByATEY4oiAd4-jAjaX-7RxCWKNwaxjPTIIwE&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060445261&signature=-sNhV47ByATEY4oiAd4-jAjaX-7RxCWKNwaxjPTIIwE&downloadName=Untitled.png" width="100%" height="100%"></a>
                <br><br>Shows the list of branches in Branch list GUI
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
				 <a href="https://file.notion.so/f/s/c1865d75-1d6a-45fd-a006-f14b7da9279d/Untitled.png?id=2968b54a-9592-4493-9c59-30d791be1a2a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060363693&signature=h3BMlQHKKTIfLRvHEHAUHURzVRmoVs08dUFZ1C1RtS0&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/c1865d75-1d6a-45fd-a006-f14b7da9279d/Untitled.png?id=2968b54a-9592-4493-9c59-30d791be1a2a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060363693&signature=h3BMlQHKKTIfLRvHEHAUHURzVRmoVs08dUFZ1C1RtS0&downloadName=Untitled.png" width="100%" height="100%"></a>
					<br><br> asks the user to select one of them
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
                <a href="https://file.notion.so/f/s/d0b3e20d-c54f-4780-97bb-2dbf9979d3c3/Untitled.png?id=2c2603b2-a1af-4db0-a960-9b31ce02a727&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060511054&signature=mjXRhDkz1sch01GabuWwU2nyKy9Bp_KFQY4SEM3vAjU&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/d0b3e20d-c54f-4780-97bb-2dbf9979d3c3/Untitled.png?id=2c2603b2-a1af-4db0-a960-9b31ce02a727&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686060511054&signature=mjXRhDkz1sch01GabuWwU2nyKy9Bp_KFQY4SEM3vAjU&downloadName=Untitled.png" width="100%" height="100%"></a>
            <br><br>checkout the branch.(You can also just double click the branch list's specific branch to checkout)</h4></td>
		</tr>
</tbody>
</table>



<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Error message windows</b><br>
				<br> If it is not possible to perform the requested action, then report an error message to the user.
                <br>We have two cases
                <br>1. When attempting to delete a current checked out branch
                <br>2. When attempting to rename a selected branch to already exists branch name<br>
                <br>3. When attempting to create a branch that same name with already exists branch
                <br><b>First Case(Try to delete current checked out branch)</b><br> 
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Current branch list(example)
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/2aaf3aa4-876c-4c63-868e-aaa831544556/Untitled.png?id=d8296999-42fe-4028-ac3e-e1f75700752d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062987091&signature=zV3OuFZZws6uarz4tLXAOseDZgd_fnR9YymA_rNogIE&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/2aaf3aa4-876c-4c63-868e-aaa831544556/Untitled.png?id=d8296999-42fe-4028-ac3e-e1f75700752d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062987091&signature=zV3OuFZZws6uarz4tLXAOseDZgd_fnR9YymA_rNogIE&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>When attempting to delete a currently checked out branch
				</h4>
			</td>
            <td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/331d99eb-3359-4ac5-8b34-d6324bba40b8/Untitled.png?id=20f2eac0-30dc-4bee-b49f-8aee2e01bbb8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063054286&signature=mjtG_d0Z6C_fDaGUvmCeqV8AaOwo2ohNTa2pULVmP0A&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/331d99eb-3359-4ac5-8b34-d6324bba40b8/Untitled.png?id=20f2eac0-30dc-4bee-b49f-8aee2e01bbb8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063054286&signature=mjtG_d0Z6C_fDaGUvmCeqV8AaOwo2ohNTa2pULVmP0A&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Error message about First case
				</h4>
			</td>
		</tr>
</tbody>
</table>


<table><tbody>
		<tr>
			<td colspan=3>
				<br>
                <br><b>Second Case(Try to rename selected branch to already exist branch)</b><br> 
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Current branch list(example)
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/62904e55-6455-4aac-83e6-503e91992a49/Untitled.png?id=526e8410-6352-427e-ad9d-f714bafc0ea1&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063460793&signature=mZfacldHkStd3XFi53Ap6j6sUrOJ6dw4VznDYbrLPHM&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/62904e55-6455-4aac-83e6-503e91992a49/Untitled.png?id=526e8410-6352-427e-ad9d-f714bafc0ea1&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063460793&signature=mZfacldHkStd3XFi53Ap6j6sUrOJ6dw4VznDYbrLPHM&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>When attempting to selected branch to already exist branch
				</h4>
			</td>
            <td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/331d99eb-3359-4ac5-8b34-d6324bba40b8/Untitled.png?id=20f2eac0-30dc-4bee-b49f-8aee2e01bbb8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063054286&signature=mjtG_d0Z6C_fDaGUvmCeqV8AaOwo2ohNTa2pULVmP0A&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/331d99eb-3359-4ac5-8b34-d6324bba40b8/Untitled.png?id=20f2eac0-30dc-4bee-b49f-8aee2e01bbb8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686063054286&signature=mjtG_d0Z6C_fDaGUvmCeqV8AaOwo2ohNTa2pULVmP0A&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Error message about Second case
				</h4>
			</td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
                <br><b>Third Case(Try to create branch that has name same with already existing branch)</b><br> 
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/8715cc91-3102-4d61-b91d-0730b3843985/Untitled.png?id=3a61a30f-b022-4ab2-9039-2fb6a78360c9&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686062900239&signature=10QNVg71__XK1imcCrIIv4UHxaQNpBQF2qBCs0DYxII&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Current branch list(example)
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/15aaa1fb-5b13-4710-bf12-ddd19f7d6564/Untitled.png?id=0cac3e0b-713b-4d04-b3ac-7dbd5619f945&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686064120341&signature=muJNyAZx0xRioMAhQHkG6Xv3uIfAIC97nsoDpz-GFvs&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/15aaa1fb-5b13-4710-bf12-ddd19f7d6564/Untitled.png?id=0cac3e0b-713b-4d04-b3ac-7dbd5619f945&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686064120341&signature=muJNyAZx0xRioMAhQHkG6Xv3uIfAIC97nsoDpz-GFvs&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>When attempting to create branch that has same with already existing branch
				</h4>
			</td>
            <td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/c2db5bcf-61ca-4209-919e-a82a20b234ca/Untitled.png?id=f29d4c08-31e6-4151-a2f2-675d945e7f77&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686064137034&signature=ogOS8Jwhwiw1R1iptfkEcUHn21aHLrNmMYV7qhGsZPs&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/c2db5bcf-61ca-4209-919e-a82a20b234ca/Untitled.png?id=f29d4c08-31e6-4151-a2f2-675d945e7f77&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686064137034&signature=ogOS8Jwhwiw1R1iptfkEcUHn21aHLrNmMYV7qhGsZPs&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Error message about Third case
				</h4>
			</td>
		</tr>
</tbody>
</table>

### <b>Feature 2. Git merge Action </b><br>
<br> We updated the Feature Git merge Action.
<br> We provides a branch list that will be merged to current branch
<br> And after that, by clicking merge button, user can do merge action
<br>There are two option
<br> 1. Fast-forward merge
<br> 2. 3-way-merge

<br> And we show Error message when some error created.

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Fast-forward merge</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/7722cbde-d98d-467d-b87b-91119b43cb1e/Untitled.png?id=3a6d7abd-0784-4e73-b96f-82ce758177d8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118476026&signature=PphxsLHgdgurWYGUA3LxebSUw4LKTGGy2vLsJrkQsH4&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/7722cbde-d98d-467d-b87b-91119b43cb1e/Untitled.png?id=3a6d7abd-0784-4e73-b96f-82ce758177d8&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118476026&signature=PphxsLHgdgurWYGUA3LxebSUw4LKTGGy2vLsJrkQsH4&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>provides a branch list that will be merged to current branch
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/2e4cf271-3e45-410a-8d52-37cc752ed782/Untitled.png?id=6e9806e8-67ea-47c0-9961-cf4edfc6633d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118120493&signature=V9FUEOKRScx4nftYnBhuS4O2PSheHwMQdI9DqQnswzM&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/2e4cf271-3e45-410a-8d52-37cc752ed782/Untitled.png?id=6e9806e8-67ea-47c0-9961-cf4edfc6633d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118120493&signature=V9FUEOKRScx4nftYnBhuS4O2PSheHwMQdI9DqQnswzM&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>select branch that will be merged and click merge
				</h4>
			</td>
            <td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/58d850a2-d45c-4d1d-b185-930ca5313593/Untitled.png?id=81c86a00-8251-4cb4-bfd2-fe280409371e&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118160116&signature=_3jK6gGXvHa9P7Tkv2GlkgyJPH6QzQmeH45HqcbUsd4&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/58d850a2-d45c-4d1d-b185-930ca5313593/Untitled.png?id=81c86a00-8251-4cb4-bfd2-fe280409371e&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118160116&signature=_3jK6gGXvHa9P7Tkv2GlkgyJPH6QzQmeH45HqcbUsd4&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Success message
				</h4>
			</td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>3-way merge</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/5f967ee7-2372-4ccd-859d-2f5dd5fb4ae6/Untitled.png?id=aea77d2e-6b23-413c-a728-8fcd14c3898d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118023236&signature=9LekeK5vz4CijrCGVnwpZ4fCA0Z2tNc7EHB_lxLvhiE&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/5f967ee7-2372-4ccd-859d-2f5dd5fb4ae6/Untitled.png?id=aea77d2e-6b23-413c-a728-8fcd14c3898d&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118023236&signature=9LekeK5vz4CijrCGVnwpZ4fCA0Z2tNc7EHB_lxLvhiE&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>provides a branch list that will be merged to current branch
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/8203ad6b-2c43-4ad3-852e-a7a78d47b2c1/Untitled.png?id=124fb83d-499e-4c96-ab12-d9b0cb7ba05a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118291773&signature=qqB23vmuujwPaFSU9uKhLx09-VgWR339Pl0Frt6FDA8&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/8203ad6b-2c43-4ad3-852e-a7a78d47b2c1/Untitled.png?id=124fb83d-499e-4c96-ab12-d9b0cb7ba05a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118291773&signature=qqB23vmuujwPaFSU9uKhLx09-VgWR339Pl0Frt6FDA8&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>select branch that will be merged and click merge
				</h4>
			</td>
            <td width="33%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/c0a7e7e9-fe0c-43a1-8db7-036376909068/Untitled.png?id=b7168f7b-1d9b-4209-80c9-e07b16293ebf&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118314459&signature=1XTP8TbISBDm1fQVZ1cwmxy_YORYXAsZZrY9cDlaXLg&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/c0a7e7e9-fe0c-43a1-8db7-036376909068/Untitled.png?id=b7168f7b-1d9b-4209-80c9-e07b16293ebf&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118314459&signature=1XTP8TbISBDm1fQVZ1cwmxy_YORYXAsZZrY9cDlaXLg&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Success message
				</h4>
			</td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=4>
				<br>
				<b>Git Merge error messages</b><br>
                <br>In 3-way merge, merge conflict can be generated.
                <br>We provides the user with an error message. and merge abort button to abort merge.
				<br>
			</td>
		</tr>
		<tr>
			<td width="25%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/a6b1a88d-bb0f-49fd-bb6e-04a0b205436d/Untitled.png?id=738435cb-e964-48a4-839e-8773ad28d28a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118632170&signature=gUL6xRawnXhl8yxkePpFv4oyHX48M6tF39SBhBdpcb4&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/a6b1a88d-bb0f-49fd-bb6e-04a0b205436d/Untitled.png?id=738435cb-e964-48a4-839e-8773ad28d28a&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118632170&signature=gUL6xRawnXhl8yxkePpFv4oyHX48M6tF39SBhBdpcb4&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Test environment. conflict exists in hi.txt
				</h4>
			</td>
			<td width="25%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/65b0b0ef-f78d-4a9b-b172-8f9a43d9e082/Untitled.png?id=381e8d31-7ba1-4f4f-85b6-eade2a14d2f6&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118832438&signature=Ls_sOiz84oOvaP1LVJ3CQz3LRm30Ux02UjMG7PbpRX4&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/65b0b0ef-f78d-4a9b-b172-8f9a43d9e082/Untitled.png?id=381e8d31-7ba1-4f4f-85b6-eade2a14d2f6&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118832438&signature=Ls_sOiz84oOvaP1LVJ3CQz3LRm30Ux02UjMG7PbpRX4&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>select branch that will be merged and click merge -> Conflict occured!!!!
				</h4>
			</td>
            <td width="25%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/c4c54576-22f6-470a-b63b-70b809bc9be5/Untitled.png?id=304e1cb7-5c02-4fe0-99db-798512f4b6a1&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118887995&signature=Da644xaa-SxiG6Yn4AUpDuV5TkLAhiVwQ_quOdNuxbY&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/c4c54576-22f6-470a-b63b-70b809bc9be5/Untitled.png?id=304e1cb7-5c02-4fe0-99db-798512f4b6a1&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686118887995&signature=Da644xaa-SxiG6Yn4AUpDuV5TkLAhiVwQ_quOdNuxbY&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>We provide abort button to abort merge
				</h4>
			</td>
            <td width="25%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/85749162-efca-486b-8bc3-4b5030b18b7d/Untitled.png?id=8a038c72-757f-49ba-84eb-1e0323c6ef29&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686119006858&signature=oktYnHZm9rsou4KUg8m-msrDqvux8Dl1K_sDnGJ8c_s&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/85749162-efca-486b-8bc3-4b5030b18b7d/Untitled.png?id=8a038c72-757f-49ba-84eb-1e0323c6ef29&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686119006858&signature=oktYnHZm9rsou4KUg8m-msrDqvux8Dl1K_sDnGJ8c_s&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Before/After click abort button
				</h4>
			</td>
		</tr>
</tbody>
</table>

### <b>Feature 3. Git Commit history with Graph </b>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
                <br><b>Git commit history with Graph</b><br> 
                <br>1. You can check the workflow of the current branch.
                <br>2. When you click commit object in graph, You can check detailed information of commit object.
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/87eaaf11-e41d-456c-bf2d-150fb9909003/Untitled.png?id=fa1f33d7-4e51-4023-9292-cf9c53d0ca03&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686065169925&signature=VBrjH1IHYzNjYJ__4sBamqLxQICguF7kV4wIoL4qmYA&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/87eaaf11-e41d-456c-bf2d-150fb9909003/Untitled.png?id=fa1f33d7-4e51-4023-9292-cf9c53d0ca03&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686065169925&signature=VBrjH1IHYzNjYJ__4sBamqLxQICguF7kV4wIoL4qmYA&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Workflow of current list(example)
				</h4>
			</td>
			<td width="50%">
				<h4 align="center">
                <a href="https://file.notion.so/f/s/bef5e3fe-7521-44ad-8900-3da88da2930b/Untitled.png?id=7125315d-5f66-46d4-8d7f-071df8717f43&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686065549325&signature=ylglTLPB84rlf-Q9wTng2sM80CPISrBiOosEIbZ_KWo&downloadName=Untitled.png"><img src="https://file.notion.so/f/s/bef5e3fe-7521-44ad-8900-3da88da2930b/Untitled.png?id=7125315d-5f66-46d4-8d7f-071df8717f43&table=block&spaceId=6b2384d5-89f7-4081-b7d5-c38398d8aee4&expirationTimestamp=1686065549325&signature=ylglTLPB84rlf-Q9wTng2sM80CPISrBiOosEIbZ_KWo&downloadName=Untitled.png" width="100%" height="100%"></a>
          <br><br>Can check commit object by click, and more complicated commit graph can be created
				</h4>
			</td>
		</tr>
</tbody>
</table>

### <b>Feature 3. Git clone from Github</b>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git clone from public repository</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm%20_cached_before.png"><img src="/data/execution_image/rm _cached_before.png" width="100%" height="100%">
					</a><br><br>git rm --cached before
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_cached_after.png"><img src="/data/execution_image/rm_cached_after.png" width="100%" height="100%"></a><br><br>git rm --cached after -> 실제 디렉토리에서 삭제되진 않았지만 git repository에서 삭제됨(untracked)됨</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git Clone from private repository</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
  <img width="804" alt="git_mv_open_mv_window" src="https://github.com/rbgksqkr/react/assets/63959171/eb0b1047-049b-484a-9a06-e3807984fe8d">
          <br><br>변경할 파일 이름 작성
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
<img width="804" alt="git_mv_rename" src="https://github.com/rbgksqkr/react/assets/63959171/30fd2f03-2777-455e-80df-dfcda1f428c0">
            <br><br>파일 이름 변경</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Saving The ID and token information should be stored somewhere for the future use.</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
  <img width="804" alt="git_mv_open_mv_window" src="https://github.com/rbgksqkr/react/assets/63959171/eb0b1047-049b-484a-9a06-e3807984fe8d">
          <br><br>변경할 파일 이름 작성
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
<img width="804" alt="git_mv_rename" src="https://github.com/rbgksqkr/react/assets/63959171/30fd2f03-2777-455e-80df-dfcda1f428c0">
            <br><br>파일 이름 변경</h4></td>
		</tr>
</tbody>
</table>

## Team Information

<table width="788">
<thead>
<tr>
<th width="100" align="center">사진</th>
<th width="100" align="center">성명</th>
<th width="150" align="center">담당</th>
<th width="100" align="center">깃허브</th>
<th width="175" align="center">이메일</th>
</tr> 
</thead>

<tbody>
<tr>
<td width="100" align="center">
  <a href="https://github.com/dn7638/dn7638/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dn7638/dn7638" />
</a>
  </td>
<td width="100" align="center">최우형</td>
<td width="150" align="center">git flow<br>status management according to git status<br>.git subdirectory control<br>test case creation<br>Git commit history Graph</td>
<td width="100" align="center">
	<a href="https://github.com/dn7638">
		<img src="http://img.shields.io/badge/dn7638-655ced?style=social&logo=github"/>
	</a>
</td>
<td width="175" align="center">
	<a href="mailto:dn7638@cau.ac.kr"><img src="https://img.shields.io/static/v1?label=&message=dn7638@cau.ac.kr&color=orange&style=flat-square&logo=gmail"></a>
	</td>
</tr>
<tr>
<td width="100" align="center"><a href="https://github.com/rbgksqkr/rbgksqkr/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=rbgksqkr/rbgksqkr" />
</a>
</a></td>
<td width="100" align="center">박규한</td>
<td width="300" align="center">git init<br>git add<br>git commit<br>git mv<br>Git clone<br>Git branch action(create,delete,rename,checkout)</td>
</td>
<td width="100" align="center">
  	<a href="https://github.com/rbgksqkr">
		<img src="http://img.shields.io/badge/rbgksqkr-655ced?style=social&logo=github"/>
	</a>
</td>
<td width="175" align="center">
	<a href="mailto:rbgks1937@gmail.com"><img src="https://img.shields.io/static/v1?label=&message=rbgks1937@gmail.com&color=green&style=flat-square&logo=gmail"></a>
	</td>
</tr>

<tr>
<td width="100" align="center"><a href="https://github.com/realisshomyang/PS/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=realisshomyang/PS" />
</a></td>
<td width="100" align="center">조명근</td>
<td width="300" align="center">git rm<br>git rm --cached<br>git restore<br>git restore --staged<br>button activation implementation according to git status of selected file<br>Git merge<br>Documentation<br>test(v2.0)</td>
</td>
<td width="100" align="center">
	<a href="https://github.com/realisshomyang">
		<img src="http://img.shields.io/badge/realisshomyang-655ced?style=social&logo=github"/>
	</a>
</td>
<td width="175" align="center">
	<a href="mailto:mgmg612@gmail.com"><img src="https://img.shields.io/static/v1?label=&message=mgmg612@gmail.com&color=green&style=flat-square&logo=gmail"></a>
	</td>
</tr>
</tr>
</tbody>
</table>

## About Collaboration

Tools used for the collaborative development

- [notion](https://bit.ly/3O3sl87)
- [github](https://github.com/CAU-OSS-project-practice/OSS-file-manager)

## Copyleft / End User License
This program is licensed under the Python Software Foundation License (PSF License).
third party softwares that may be contained in this program is referd in license.txt below.
- https://github.com/CAU-OSS-project-practice/OSS-file-manager/blob/main/license
