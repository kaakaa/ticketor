python setup.py build_apidoc

cd build/sphinx/html

git init
git config --global user.name "kaakaa"
git config --global user.email "stooner.hoe@gmail.com"
git add .
git commit -m "update apidoc"

echo "FETCH GITHUB REPOSITORY"
git remote add origin https://${GH_TOKEN}@github.com/kaakaa/ticketor.git
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
git push --force --quiet origin gh-pages > /dev/null 2>&1
