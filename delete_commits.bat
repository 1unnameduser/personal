@echo off
:: https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
git checkout --orphan latest_branch
git add -A
git commit -am "bla bla"
git branch -D main
git branch -m main
git push -f origin main
pause