python setup.py build_apidoc

cd build/sphinx/html

git init
git config user.email "stooner.hoe@gmail.com"
git config user.name "kaakaa"
git add .
git commit -m "update apidoc"

echo "FETCH GITHUB REPOSITORY"
echo "GHTOKEN= ${GH_TOKEN} ="
git remote add origin https://${GH_TOKEN}@github.com/kaakaa/trac-team-task-register.git
git fetch origin

echo "CHECKOUT GH-PAGES BRANCH"
git checkout -b gh-pages origin/gh-pages
echo "MERGE NEW DOCS"
git merge master
git checkout --theirs *

echo "COMMIT NEW DOCS"
git add .
git commit -m "update apidoc"

echo "PUSH"
git push -u origin gh-pages
