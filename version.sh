git config credential.helper store
git pull origin master
#HOSTS="$(cat /etc/hostname)"
#LOCATION="$(pwd)"

if [ "$1" = "commit" ]
then
  git add .
  git commit -m "$2"
  git push origin master

else
  echo "no argument"

fi
