#!/bin/bash
#sudo -i
cd /home/pi/Bene2907.github.io/
#git status

git rm --cached $1.json
git commit -m "remove " + $1 + ".json"
git push https://Bene2907:VPFmsqjfkX5CEQxS1s6@github.com/Bene2907/Bene2907.github.io.git master


git add $1.json
git commit -m "comment"
git push https://Bene2907:VPFmsqjfkX5CEQxS1s6@github.com/Bene2907/Bene2907.github.io.git master
