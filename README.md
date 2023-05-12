# Python-file-explorer(with git) develop by OSS-TEAM-13

<p align="center">
<a href="https://fixed-borogovia-5fe.notion.site/OSS-Team-13-4df2df4655c645a8a7e49e15abbffa3c">
<img src="https://img.shields.io/badge/NOTION-team_page-green?&style=for-the-badge&logo=notion">
</a>

</p>

## 목차

- [프로젝트 소개](#프로젝트-소개)
- [설치 안내](#설치-안내)
- [기능 설계 및 설명](#기능-설계-및-설명)
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

## 기능 설계 및 설명

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
				<a href = "https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/web_login.png"><img src="/data/execution_image/rootdir.png" width="75%" height="75%">
					</a><br><br> 파일 탐색은 루트 디렉토리에서 시작
				</h4>
			</td>
			<td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_login.png"><img src="/data/execution_image/in folder.png" width="75%" height="75%"></a><br><br>현재 디렉토리에 포함된 모든 파일과 디렉토리는 아이콘, 이름, 확장자로 표현 </h4></td>
            <td width="33%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_login.png"><img src="/data/execution_image/double-click.gif" width="75%" height="75%"></a><br><br>더블 클릭을 통해 브라우징 가능 </h4></td>
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
		   		<a href="https://github.com/CAU-OSS-project-practice/OSS-file-manager/blob/develop/data/icon_file_unstaged.png?raw=true"><img src="/data/icon_file_unstaged.png" width="75%" height="75%"></a><br>unstaged(modified)된 파일 표시<br></h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file.png"><img src="/data/icon_file.png" width="75%" height="75%"></a><br><br>committed(unmodified)된 파일 표시</h4></td>
                <td width="25%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/CAU-OSS-project-practice/OSS-file-manager/develop/data/icon_file_both.png"><img src="/data/icon_file_both.png" width="75%" height="75%"></a><br><br>staged-unstaged(modified)된 파일 표시</h4></td>
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
			<td colspan=2>
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
			<td width="65%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/web_history.png"><img src="/data/execution_image/git_restore_before.png" width="100%" height="100%">
					</a><br><br>Git restore 작동 전
				</h4>
			</td>
			<td width="35%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_history.png"><img src="/data/execution_image/git_restore_after.png" width="75%" height="75%"></a><br><br>git restore 작동 후</h4></td>
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
			<td width="65%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/web_history.png"><img src="/data/execution_image/git_restore_staged_before.png" width="100%" height="100%">
					</a><br><br>Git restore 작동 modified된 파일을 committed상태로 되돌림
				</h4>
			</td>
			<td width="35%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_history.png"><img src="/data/execution_image/git_restore_staged_after.png" width="75%" height="75%"></a><br><br>git restore --staged staged된 파일을 modified 상태로 되돌림</h4></td>
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
			<td width="65%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/web_history.png"><img src="/data/execution_image/rm_after.png" width="100%" height="100%">
					</a><br><br>git rm before
				</h4>
			</td>
			<td width="35%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_history.png"><img src="/data/execution_image/rm_after.png" width="75%" height="75%"></a><br><br>git rm --cached after </h4></td>
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
			<td width="65%">
				<h4 align="center">
				<a href = "https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/web_history.png"><img src="/data/execution_image/rm _cached_before.png" width="100%" height="100%">
					</a><br><br>git rm --cached before
				</h4>
			</td>
			<td width="35%">
	   			<h4 align="center">
		   		<a href="https://raw.githubusercontent.com/osamhack2021/WEB_APP_IOT_ModuChangGo_Chang-keeper/edit/image/ui/app_history.png"><img src="/data/execution_image/rm_cached_after.png" width="75%" height="75%"></a><br><br>git rm --cached after -> 실제 디렉토리에서 삭제되진 않았지만 git repository에서 삭제됨(untracked)됨</h4></td>
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

## 팀 정보 (Team Information)

<table width="788">
<thead>
<tr>
<th width="100" align="center">사진</th>
<th width="100" align="center">성명</th>
<th width="150" align="left">담당</th>
<th width="100" align="center">깃허브</th>
<th width="175" align="center">이메일</th>
</tr> 
</thead>
<tbody>
<tr>
<td width="100" align="center"><img src="/image/박규한.jpg" width="60" height="60"></td>
<td width="100" align="center">박규한</td>
<td width="150">백엔드 개발<br>서버 환경 구축<br>데이터베이스 설계</td>
<td width="100" align="center">
	<a href="https://github.com/rbgksqkr">
		<img src="http://img.shields.io/badge/rbgksqkr-655ced?style=social&logo=github"/>
	</a>
</td>
<td width="175" align="center">
	<a href="mailto:rbgks1937@gmail.com"><img src="https://img.shields.io/static/v1?label=&message=rbgks1937@gmail.com&color=orange&style=flat-square&logo=gmail"></a>
	</td>
</tr>
<tr>
<td width="100" align="center"><img src="/image/김태한.jpg" width="60" height="60"></td>
<td width="100" align="center">최우형</td>
<td width="300">앱 개발<br>서버/프런트 간 통신 구현<br>서버 테스트<br></td>
</td>
<td width="100" align="center">
	<a href="https://github.com/TaehanKim00">
		<img src="http://img.shields.io/badge/TaehanKim00-655ced?style=social&logo=github"/>
	</a>
</td>
<td width="175" align="center">
	<a href="mailto:tk5582lm@gmail.com"><img src="https://img.shields.io/static/v1?label=&message=tk5582lm@gmail.com&color=green&style=flat-square&logo=gmail"></a>
	</td>
</tr>

<tr>
<td width="100" align="center"><img src="/image/조명근.PNG" width="60" height="60"></td>
<td width="100" align="center">조명근</td>
<td width="300">아두이노 개발<br>문서화 작업<br></td>
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
