#!/bin/sh

# Returns boolean indicates whether designated tagged-image exists.
  # arg1: repository name
  # arg2: tag name
function image_exists() {
  image=$(docker image ls -a | grep $1 | grep $2)

  if [ "$image" ]; then
    return 0;
  else
    return 1;
  fi
}


# Builds new image.
  # arg1: tag in the form like ${repository}:${tag}
  # arg2: Path to Dockerfile
function build_image() {
  docker build -t $1 -f $2 .
}

# Work on master branch
git checkout master

# Get latest master revision
revision=$(git rev-parse --short HEAD)

echo "Current master revision is ${revision}"

# Set constants
readonly repository=vinodmandli/vmcatsdogs
readonly localGitRepository=/c/quantexa/vmcatsdogs
#~/cats-dogs
readonly revised_repository=$repository:$revision
readonly path_to_dockerfile=.
readonly dockerUserName=vinodmandli

echo "

local-git-repository: ${localGitRepository}
docker-repository: ${repository}
docker-revised-repository: ${revised_repository}
path-to-dockerfile: ${path_to_dockerfile}

"

#get up to date code from git
cd $localGitRepository
git pull origin master

# Build current source if revision not exists
if image_exists $repository $revision; then
  # Do nothing.
  echo "local-revised-repository already exists. Skip build.\n"
  true;
else
  echo "Start building local-revised-repository."
  build_image $revised_repository $path_to_dockerfile;
fi

# check if docker image has been built successfully
if image_exists $repository $revision; then
  echo "docker image has been built.
  "
  # Push new image to dockerHub
  upload=$(docker push $repository:$revision | grep "unauthorized")

  if [ "$upload" ]; then
    docker login -u $dockerUserName 
  else
    echo "docker image has been uploaded to docker hub."
  fi
  
  #Deploying the image to kubernetes
  kubectl apply -f ./vmcatsdogs.yml
  #setting current image name to pods to trigger upgrade rollout
  kubectl set image statefulset/vmcatsdogs vmcatsdogsserver=$revised_repository
  #View rollout status
  kubectl rollout status statefulset/vmcatsdogs

  echo "Done.\n"
else
  echo "****ERROR while building docker image. removing docker image and Exiting..."
  docker rmi $repository:$revision
  exit "dockerImageBuildError"
fi