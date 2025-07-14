git init mini_repo
cd mini_repo
echo "a" > a.txt
git add .
git commit -m "init"
echo "b" > b.txt
git add .
git commit -m "feature"
git checkout -b bugfix
echo "fix" > fix.txt
git add .
git commit -m "bugfix"
git checkout main
git merge bugfix -m "merge bugfix"
