python setup.py build_apidoc

cd build/sphinx/html

git init
git add .
git commit -m "update apidoc"

git remote add origin https://${GH_TOKEN}github.com/kaakaa/trac-team-task-register.git
git fetch origin

git checkout -b gh-pages origin/gh-pages
git merge master
git checkout --theirs *

git add .
git commit -m "update apidoc"

git push -u origin gh-pages
