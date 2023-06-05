# Python-file-explorer(with git) develop by OSS-TEAM-13

<p align="center">
<a href="https://fixed-borogovia-5fe.notion.site/OSS-Team-13-4df2df4655c645a8a7e49e15abbffa3c">
<img src="https://img.shields.io/badge/NOTION-team_page-green?&style=for-the-badge&logo=notion">
</a>
</p>

## 목차

- [프로젝트 소개](#프로젝트-소개)
- [설치 안내](#설치-안내)
- [기능 설계 및 설명(v1.0)](#기능-설계-및-설명(v1.0))
- [기능 설계 및 설명(v2.0)](#기능-설계-및-설명(v2.0))
- [팀 정보 (Team Information)](#팀-정보-team-information)
- [협업 과정](#협업과정)
- [저작권 및 사용권 정보(Copyleft / End User License)](#저작권-및-사용권-정보-copyleft--end-user-license)

## 프로젝트 소개

이 프로젝트는 파일 브라우징에 Git에 관련한 기능을 넣어 확장시킨 git file browser 프로젝트입니다. <br/>
기본적으로 파일 브라우징 기능을 제공하고 아래의 기능을 제공합니다

- `git init`
- `git add`
- `git commit`
- `git rm ` && `git rm --cached`
- `git restore` && `git restore --staged`
- `git mv`

이런 기능뿐 아니라 Git status에 따른 파일 상태(4가지)를 이미지로 표시합니다!

## 설치 안내

### Needs for running

```bash
Python 3.8+
pip (package installer for Python)
platform : mac OS
```

- 설치 순서

```bash\
git clone https://github.com/CAU-OSS-project-practice/OSS-file-manager.git
cd OSS-file-manager
pip install -r requirements.txt
python3 files_new.py
```

- tkinter 라이브러리 오류 또는 파이썬 버전 충돌 시 가상환경에서 동작

```bash
python -m venv .venv # .venv 생성
source .venv/bin/activate # 가상환경 실행
```

- 가상환경 비활성화

```bash
deactivate
```

## 기능 설계 및 설명(v1.0)

> 모든 사진은 클릭 시 확대 된 이미지로 확인할 수 있습니다.😀

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>파일 브라우저 기능 </b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rootdir.png"><img src="/data/execution_image/rootdir.png" width="100%" height="100%">
					</a><br><br> 파일 탐색은 루트 디렉토리에서 시작
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/in%20folder.png"><img src="/data/execution_image/in folder.png" width="100%" height="100%"></a><br><br>현재 디렉토리에 포함된 모든 파일과 디렉토리는 아이콘, 이름, 확장자로 표현 </h4></td>
            <td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/double-click.gif"><img src="/data/execution_image/double-click.gif" width="100%" height="100%"></a><br><br>더블 클릭을 통해 브라우징 가능 </h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git init 기능 </b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
<img width="804" alt="git_init_not_git_repo" src="https://github.com/rbgksqkr/react/assets/63959171/ce081f1c-5bf2-4e15-9b47-510bc62a891c">
					</a><br><br>Git repository가 아닌 디렉토리인 경우 -> init 버튼 활성화
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
                      <img width="804" alt="git_init_git_repo" src="https://github.com/rbgksqkr/react/assets/63959171/709a75ea-e70f-43dd-8165-0cbb3f49b41d">
            </a><br><br>이미 Git repository인 디렉토리의 경우 -> init 버튼 비활성화</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=4>
				<br>
				<b>Git status에 따른 파일 상태 표시</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="25%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file_staged.png"><img src="/data/icon_file_staged.png" width="100%" height="100%">
					</a><br><br>staging된 파일 표시
				</h4>
			</td>
			<td width="25%">
	   			<h4 align="center">
		   		<a href="https://github.com/CAU-OSS-project-practice/OSS-file-manager/blob/develop/data/icon_file_unstaged.png?raw=true"><img src="/data/icon_file_unstaged.png" width="100%" height="100%"></a><br>unstaged(modified)된 파일 표시<br></h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file.png"><img src="/data/icon_file.png" width="100%" height="100%"></a><br><br>committed(unmodified)된 파일 표시</h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file_both.png"><img src="/data/icon_file_both.png" width="100%" height="100%"></a><br><br>staged-unstaged(modified)된 파일 표시</h4></td>
		</tr>
</tbody>
</table>
Stage를 4가지로 나눴습니다.

1. Staged
2. unstaged(modified)
3. committed(unmodified)
4. staged - unstaged(staging된 상태에서 파일을 변경한 경우)

untracked - staged 된 파일 ex) git rm --cached 명령어 실행 시에는 untracked를 우선순위로 동작하게 만들었습니다.

<table><tbody>
		<tr>
			<td colspan=3>
				<br>
				<b>Git add 기능</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="33%">
				<h4 align="center">
          <img width="804" alt="git_add_before" src="https://github.com/rbgksqkr/react/assets/63959171/514aaa4d-1245-4c3c-9b55-1f34f023e8d5">
					<br><br> 파일 선택 전 
				</h4>
			</td>
			<td width="33%">
				<h4 align="center">
				<img width="804" alt="git_add_one" src="https://github.com/rbgksqkr/react/assets/63959171/6938733f-a031-4093-8bd8-feaff368b5f9">
					<br><br> 한 파일 선택시 그 파일만 add 가능
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
		   		<img width="804" alt="git_add_all" src="https://github.com/rbgksqkr/react/assets/63959171/b8b24523-a693-466e-8962-4a3d4f41daae">
            <br><br>선택된 파일이 없을 시에는 git add . 동작</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git commit 기능</b><br>
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
            <br><br>commit message 작성</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git restore 기능</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_after.png"><img src="/data/execution_image/git_restore_after.png" width="100%" height="100%"></a><br><br>Git restore 작동 전(modified된 파일 표시)</h4></td>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_before.png"><img src="/data/execution_image/git_restore_before.png" width="100%" height="100%">
					</a><br><br>git restore 작동 후(commit전 상태로 되돌아옴)
				</h4>
			</td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git restore --staged 기능</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_before.png"><img src="/data/execution_image/git_restore_staged_before.png" width="100%" height="100%">
					</a><br><br>Git restore --staged작동 전(파일을 staging)
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_after.png"><img src="/data/execution_image/git_restore_staged_after.png" width="100%" height="100%"></a><br><br>git restore --staged staged된 파일을 modified 상태로 되돌림</h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git rm 기능</b><br>
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
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_after.png"><img src="/data/execution_image/rm_after.png" width="100%" height="100%"></a><br><br>git rm after(디렉토리에서 삭제 및 삭제된 사실이 staging됨) </h4></td>
		</tr>
</tbody>
</table>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git rm --cached 기능</b><br>
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
				<b>Git mv 기능</b><br>
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


## Function design and description(v2.0)

> All photos can be viewed as enlarged images when clicked.😀  

New Feature has updated.

1. We updated Git branch associated action(Create, Delete, Rename, Checkout, Merge).
2. And We can also check Git commit history
3. Git clone from Github

Feature 1 and 2 can be activated through the Branch Menu button.  
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

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git Merge error messages</b><br>
				<br>
			</td>
		</tr>
		<tr>
			<td width="50%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_before.png"><img src="/data/execution_image/git_restore_staged_before.png" width="100%" height="100%">
					</a><br><br>Git restore --staged작동 전(파일을 staging)
				</h4>
			</td>
			<td width="50%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/git_restore_staged_after.png"><img src="/data/execution_image/git_restore_staged_after.png" width="100%" height="100%"></a><br><br>git restore --staged staged된 파일을 modified 상태로 되돌림</h4></td>
		</tr>
</tbody>
</table>

### <b>Feature 2. Git Commit history with Graph </b>

<table><tbody>
		<tr>
			<td colspan=2>
				<br>
				<b>Git commit history with Graph</b><br>
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
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/execution_image/rm_after.png"><img src="/data/execution_image/rm_after.png" width="100%" height="100%"></a><br><br>git rm after(디렉토리에서 삭제 및 삭제된 사실이 staging됨) </h4></td>
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

## 팀 정보 (Team Information)

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
<td width="150" align="center">git flow<br>git status에 따른 상태관리<br>.git 서브디렉토리 제어<br>테스트케이스 작성<br></td>
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
<td width="300" align="center">git init<br>git add<br>git commit<br>git mv<br></td>
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
<td width="300" align="center">git rm<br>git rm --cached<br>git restore<br>git restore --staged<br>select된 파일의 git status에 따른 버튼 활성화 구현<br></td>
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

## 협업과정

Tools used for the collaborative development

- [notion](https://bit.ly/3O3sl87)
- [github](https://github.com/CAU-OSS-project-practice/OSS-file-manager)

## 저작권 및 사용권 정보 (Copyleft / End User License)
This program is licensed under the Python Software Foundation License (PSF License).
third party softwares that may be contained in this program is referd in license.txt below.
- https://github.com/CAU-OSS-project-practice/OSS-file-manager/blob/main/license
