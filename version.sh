git config credential.helper store
git pull origin master
#HOSTS="$(cat /etc/hostname)"
#LOCATION="$(pwd)"

if [ "$1" = "commit" ]
then
  git add .
  git commit -m "$2"
  git push origin master

elif [ "$1" = "grpc" ]
then
  if [ "$2" = "helloworld" ]
  then
    cd grpc/helloworld
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. helloworld.proto

  elif [ "$2" = "route_guide" ]
  then
    cd grpc/route_guide
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. route_guide.proto
  fi

elif [ "$1" = "skeleton" ]
then
    cd skeleton
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. skeleton.proto


#elif [ "$1" = "Project_Skeleton" ]
#then
#  cd Project/skeleton/
#  python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. example.proto
#
#elif [ "$1" = "Project_Example" ]
#then
#  cd Project/example/
#  python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. example.proto

else
  echo "no argument"

fi
