git config credential.helper store
git pull origin master
#HOSTS="$(cat /etc/hostname)"
#LOCATION="$(pwd)"

if [ "$1" = "commit" ]
then
  git add .
  git commit -m "$2"
  git push origin master

elif [ "$1" = "Project_Skeleton" ]
then
  cd Project/skeleton/
  python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. skeleton.proto


else
  echo "no argument"

fi
