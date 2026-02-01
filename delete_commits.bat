@echo off
pushd "%~dp0"
rem https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
rem GIT portable is required -- https://git-scm.com/install/windows
rem SFK is required -- https://www.stahlworks.com/
for /f %%a in ('sfk time') do set tTime=%%a
set path=%path%;C:\PortableGit\bin
git checkout --orphan latest_branch
git add -A
git commit -am "%tTime%"
git branch -D main
git branch -m main
git push -f origin main
pause
